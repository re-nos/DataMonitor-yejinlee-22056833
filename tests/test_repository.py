from data_monitor.models import Order, OrderStatus, Sample
from data_monitor.repository import InMemoryRepository, build_dummy_repository


class TestInMemoryRepository:
    def test_list_samples_returns_all_samples(self):
        sample = Sample(
            sample_id="S1",
            name="Wafer-A",
            avg_production_time=2.0,
            yield_rate=0.9,
            stock=10,
            standard_stock=20,
        )
        repo = InMemoryRepository(samples=[sample], orders=[])
        assert repo.list_samples() == [sample]

    def test_list_orders_returns_all_orders(self):
        order = Order(order_id="O1", sample_id="S1", customer_name="Acme", quantity=5)
        repo = InMemoryRepository(samples=[], orders=[order])
        assert repo.list_orders() == [order]

    def test_get_sample_returns_none_when_missing(self):
        repo = InMemoryRepository(samples=[], orders=[])
        assert repo.get_sample("unknown") is None

    def test_get_sample_returns_matching_sample(self):
        sample = Sample(
            sample_id="S1",
            name="Wafer-A",
            avg_production_time=2.0,
            yield_rate=0.9,
            stock=10,
            standard_stock=20,
        )
        repo = InMemoryRepository(samples=[sample], orders=[])
        assert repo.get_sample("S1") is sample


class TestBuildDummyRepository:
    def test_includes_all_order_statuses(self):
        repo = build_dummy_repository()
        statuses = {order.status for order in repo.list_orders()}
        assert statuses == set(OrderStatus)

    def test_includes_at_least_one_sample(self):
        repo = build_dummy_repository()
        assert len(repo.list_samples()) >= 1
