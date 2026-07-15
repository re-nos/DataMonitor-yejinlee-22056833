"""모니터링 대상 데이터를 제공하는 인메모리 저장소.

이 PoC는 별도의 DataPersistence 저장소를 참조하지 않으므로,
모니터링 로직 검증을 위한 더미 데이터를 자체적으로 생성한다.
"""

from __future__ import annotations

from data_monitor.models import Order, OrderStatus, Sample


class InMemoryRepository:
    """시료/주문 데이터를 메모리에 보관하는 저장소."""

    def __init__(self, samples: list[Sample], orders: list[Order]) -> None:
        self._samples = {sample.sample_id: sample for sample in samples}
        self._orders = list(orders)

    def list_samples(self) -> list[Sample]:
        return list(self._samples.values())

    def list_orders(self) -> list[Order]:
        return list(self._orders)

    def get_sample(self, sample_id: str) -> Sample | None:
        return self._samples.get(sample_id)


def build_dummy_repository() -> InMemoryRepository:
    """모니터링 화면 검증용 더미 시료/주문 데이터를 생성한다.

    시료별로 여유/부족/고갈 재고 상태를 각각 하나 이상 포함하고,
    주문은 REJECTED를 포함한 모든 상태를 포함하도록 구성한다.
    """

    samples = [
        Sample(
            sample_id="SMP-001",
            name="Wafer-A",
            avg_production_time=2.0,
            yield_rate=0.9,
            stock=80,
            standard_stock=100,
        ),
        Sample(
            sample_id="SMP-002",
            name="Wafer-B",
            avg_production_time=3.5,
            yield_rate=0.75,
            stock=20,
            standard_stock=100,
        ),
        Sample(
            sample_id="SMP-003",
            name="Wafer-C",
            avg_production_time=1.5,
            yield_rate=0.95,
            stock=0,
            standard_stock=50,
        ),
    ]

    orders = [
        Order(order_id="ORD-001", sample_id="SMP-001", customer_name="KAIST", quantity=10, status=OrderStatus.RESERVED),
        Order(order_id="ORD-002", sample_id="SMP-002", customer_name="Fabless Inc", quantity=30, status=OrderStatus.PRODUCING),
        Order(order_id="ORD-003", sample_id="SMP-001", customer_name="POSTECH", quantity=5, status=OrderStatus.CONFIRMED),
        Order(order_id="ORD-004", sample_id="SMP-003", customer_name="ETRI", quantity=15, status=OrderStatus.RELEASE),
        Order(order_id="ORD-005", sample_id="SMP-002", customer_name="SNU", quantity=8, status=OrderStatus.REJECTED),
    ]

    return InMemoryRepository(samples=samples, orders=orders)
