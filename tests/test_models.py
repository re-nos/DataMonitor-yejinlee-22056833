import pytest

from data_monitor.models import Order, OrderStatus, Sample


class TestSample:
    def test_creates_with_valid_values(self):
        sample = Sample(
            sample_id="S1",
            name="Wafer-A",
            avg_production_time=2.5,
            yield_rate=0.9,
            stock=10,
            standard_stock=20,
        )
        assert sample.sample_id == "S1"
        assert sample.stock == 10

    @pytest.mark.parametrize("yield_rate", [0, -0.1, 1.1])
    def test_rejects_invalid_yield_rate(self, yield_rate):
        with pytest.raises(ValueError):
            Sample(
                sample_id="S1",
                name="Wafer-A",
                avg_production_time=2.5,
                yield_rate=yield_rate,
                stock=10,
                standard_stock=20,
            )

    def test_rejects_non_positive_production_time(self):
        with pytest.raises(ValueError):
            Sample(
                sample_id="S1",
                name="Wafer-A",
                avg_production_time=0,
                yield_rate=0.9,
                stock=10,
                standard_stock=20,
            )

    def test_rejects_negative_stock(self):
        with pytest.raises(ValueError):
            Sample(
                sample_id="S1",
                name="Wafer-A",
                avg_production_time=2.5,
                yield_rate=0.9,
                stock=-1,
                standard_stock=20,
            )

    def test_rejects_non_positive_standard_stock(self):
        with pytest.raises(ValueError):
            Sample(
                sample_id="S1",
                name="Wafer-A",
                avg_production_time=2.5,
                yield_rate=0.9,
                stock=10,
                standard_stock=0,
            )


class TestOrder:
    def test_defaults_to_reserved_status(self):
        order = Order(order_id="O1", sample_id="S1", customer_name="Acme", quantity=5)
        assert order.status == OrderStatus.RESERVED

    def test_rejects_non_positive_quantity(self):
        with pytest.raises(ValueError):
            Order(order_id="O1", sample_id="S1", customer_name="Acme", quantity=0)

    def test_accepts_explicit_status(self):
        order = Order(
            order_id="O1",
            sample_id="S1",
            customer_name="Acme",
            quantity=5,
            status=OrderStatus.CONFIRMED,
        )
        assert order.status == OrderStatus.CONFIRMED
