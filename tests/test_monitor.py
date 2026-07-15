import pytest

from data_monitor.models import Order, OrderStatus, Sample
from data_monitor.monitor import (
    StockStatus,
    build_stock_report,
    build_stock_reports,
    count_orders_by_status,
)


def make_order(status: OrderStatus, order_id: str = "O1") -> Order:
    return Order(order_id=order_id, sample_id="S1", customer_name="Acme", quantity=1, status=status)


class TestCountOrdersByStatus:
    def test_excludes_rejected_orders(self):
        orders = [make_order(OrderStatus.REJECTED)]
        counts = count_orders_by_status(orders)
        assert OrderStatus.REJECTED not in counts

    def test_counts_each_monitored_status(self):
        orders = [
            make_order(OrderStatus.RESERVED, "O1"),
            make_order(OrderStatus.RESERVED, "O2"),
            make_order(OrderStatus.CONFIRMED, "O3"),
            make_order(OrderStatus.PRODUCING, "O4"),
            make_order(OrderStatus.RELEASE, "O5"),
        ]
        counts = count_orders_by_status(orders)
        assert counts[OrderStatus.RESERVED] == 2
        assert counts[OrderStatus.CONFIRMED] == 1
        assert counts[OrderStatus.PRODUCING] == 1
        assert counts[OrderStatus.RELEASE] == 1

    def test_includes_zero_count_for_missing_status(self):
        counts = count_orders_by_status([])
        assert counts[OrderStatus.RESERVED] == 0
        assert counts[OrderStatus.CONFIRMED] == 0
        assert counts[OrderStatus.PRODUCING] == 0
        assert counts[OrderStatus.RELEASE] == 0


def make_sample(stock: int, standard_stock: int = 100) -> Sample:
    return Sample(
        sample_id="S1",
        name="Wafer-A",
        avg_production_time=2.0,
        yield_rate=0.9,
        stock=stock,
        standard_stock=standard_stock,
    )


class TestBuildStockReport:
    def test_zero_stock_is_depleted(self):
        report = build_stock_report(make_sample(stock=0))
        assert report.status == StockStatus.DEPLETED

    def test_below_threshold_is_low(self):
        report = build_stock_report(make_sample(stock=29, standard_stock=100))
        assert report.status == StockStatus.LOW
        assert report.remaining_rate == pytest.approx(0.29)

    def test_at_threshold_is_sufficient(self):
        report = build_stock_report(make_sample(stock=30, standard_stock=100))
        assert report.status == StockStatus.SUFFICIENT

    def test_above_threshold_is_sufficient(self):
        report = build_stock_report(make_sample(stock=80, standard_stock=100))
        assert report.status == StockStatus.SUFFICIENT
        assert report.remaining_rate == pytest.approx(0.8)


class TestBuildStockReports:
    def test_builds_one_report_per_sample(self):
        samples = [make_sample(stock=10), make_sample(stock=0)]
        reports = build_stock_reports(samples)
        assert len(reports) == 2
        assert reports[1].status == StockStatus.DEPLETED
