"""S-Semi 시료/주문 도메인 모델."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderStatus(str, Enum):
    """주문 상태. REJECTED는 정상 흐름 외 상태로 모니터링에서 제외된다."""

    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"


MONITORED_STATUSES = (
    OrderStatus.RESERVED,
    OrderStatus.PRODUCING,
    OrderStatus.CONFIRMED,
    OrderStatus.RELEASE,
)


@dataclass
class Sample:
    """시료 정보.

    standard_stock은 재고 잔여율(현재고 / 기준 재고) 계산을 위한 기준 재고량이다.
    """

    sample_id: str
    name: str
    avg_production_time: float
    yield_rate: float
    stock: int
    standard_stock: int

    def __post_init__(self) -> None:
        if not 0 < self.yield_rate <= 1:
            raise ValueError(f"수율은 0 초과 1 이하여야 합니다: {self.yield_rate}")
        if self.avg_production_time <= 0:
            raise ValueError(f"평균 생산시간은 0보다 커야 합니다: {self.avg_production_time}")
        if self.stock < 0:
            raise ValueError(f"재고는 0 이상이어야 합니다: {self.stock}")
        if self.standard_stock <= 0:
            raise ValueError(f"기준 재고량은 0보다 커야 합니다: {self.standard_stock}")


@dataclass
class Order:
    """고객 주문 정보."""

    order_id: str
    sample_id: str
    customer_name: str
    quantity: int
    status: OrderStatus = OrderStatus.RESERVED

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"주문 수량은 0보다 커야 합니다: {self.quantity}")
