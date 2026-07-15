"""모니터링 결과를 콘솔에 출력하기 위한 포맷팅 함수.

각 함수는 화면에 그대로 출력할 문자열을 반환한다. stdout에 직접
쓰지 않으므로 테스트에서 문자열 내용을 손쉽게 검증할 수 있다.
"""

from __future__ import annotations

from data_monitor.models import OrderStatus
from data_monitor.monitor import SampleStockReport

_ORDER_STATUS_LABELS = {
    OrderStatus.RESERVED: "주문 접수",
    OrderStatus.PRODUCING: "생산 중",
    OrderStatus.CONFIRMED: "출고 대기",
    OrderStatus.RELEASE: "출고 완료",
}


def render_order_summary(counts: dict[OrderStatus, int]) -> str:
    """상태별 주문 건수를 표 형태의 문자열로 렌더링한다."""

    lines = ["=== 주문 현황 (REJECTED 제외) ==="]
    for status, count in counts.items():
        label = _ORDER_STATUS_LABELS.get(status, status.value)
        lines.append(f"  {status.value:<10} ({label:<6}) : {count:>4}건")
    return "\n".join(lines)


def render_stock_report(reports: list[SampleStockReport]) -> str:
    """시료별 재고 현황을 표 형태의 문자열로 렌더링한다."""

    lines = ["=== 시료 재고 현황 ==="]
    for report in reports:
        rate_pct = report.remaining_rate * 100
        lines.append(
            f"  [{report.sample_id}] {report.name:<10} "
            f"재고 {report.stock:>4}/{report.standard_stock:<4} "
            f"(잔여율 {rate_pct:5.1f}%) - {report.status.value}"
        )
    if not reports:
        lines.append("  등록된 시료가 없습니다.")
    return "\n".join(lines)
