"""주문량 및 재고 현황 모니터링 로직.

PRD CHAPTER 2-D 모니터링 요구사항:
- 주문량: RESERVED/CONFIRMED/PRODUCING/RELEASE 상태별 건수 (REJECTED 제외)
- 재고량: 시료별 재고 수량, 상태(여유/부족/고갈), 잔여율
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from data_monitor.models import MONITORED_STATUSES, Order, OrderStatus, Sample

LOW_STOCK_THRESHOLD = 0.3
"""잔여율이 이 값 미만이면 '부족'으로 판정한다."""


class StockStatus(str, Enum):
    SUFFICIENT = "여유"
    LOW = "부족"
    DEPLETED = "고갈"


@dataclass(frozen=True)
class SampleStockReport:
    """시료 하나의 재고 현황."""

    sample_id: str
    name: str
    stock: int
    standard_stock: int
    remaining_rate: float
    status: StockStatus


def count_orders_by_status(orders: list[Order]) -> dict[OrderStatus, int]:
    """REJECTED를 제외한 상태별 주문 건수를 반환한다.

    모니터링 대상 상태는 항상 결과에 포함되며, 해당 상태의 주문이
    없으면 0으로 표시된다.
    """

    counts = {status: 0 for status in MONITORED_STATUSES}
    for order in orders:
        if order.status in counts:
            counts[order.status] += 1
    return counts


def _classify_stock(remaining_rate: float, stock: int) -> StockStatus:
    if stock == 0:
        return StockStatus.DEPLETED
    if remaining_rate < LOW_STOCK_THRESHOLD:
        return StockStatus.LOW
    return StockStatus.SUFFICIENT


def build_stock_report(sample: Sample) -> SampleStockReport:
    """시료 하나의 재고 현황 리포트를 생성한다."""

    remaining_rate = sample.stock / sample.standard_stock
    status = _classify_stock(remaining_rate, sample.stock)
    return SampleStockReport(
        sample_id=sample.sample_id,
        name=sample.name,
        stock=sample.stock,
        standard_stock=sample.standard_stock,
        remaining_rate=remaining_rate,
        status=status,
    )


def build_stock_reports(samples: list[Sample]) -> list[SampleStockReport]:
    """모든 시료에 대한 재고 현황 리포트 목록을 생성한다."""

    return [build_stock_report(sample) for sample in samples]
