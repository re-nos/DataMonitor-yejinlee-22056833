from data_monitor.models import OrderStatus
from data_monitor.monitor import SampleStockReport, StockStatus
from data_monitor.view import render_order_summary, render_stock_report


class TestRenderOrderSummary:
    def test_includes_all_monitored_statuses(self):
        counts = {
            OrderStatus.RESERVED: 2,
            OrderStatus.PRODUCING: 1,
            OrderStatus.CONFIRMED: 0,
            OrderStatus.RELEASE: 3,
        }
        output = render_order_summary(counts)
        assert "RESERVED" in output
        assert "PRODUCING" in output
        assert "CONFIRMED" in output
        assert "RELEASE" in output
        assert OrderStatus.REJECTED.value not in output.split("\n", 1)[1]

    def test_shows_counts(self):
        counts = {OrderStatus.RESERVED: 7}
        output = render_order_summary(counts)
        assert "7건" in output


class TestRenderStockReport:
    def test_shows_sample_and_status(self):
        reports = [
            SampleStockReport(
                sample_id="S1",
                name="Wafer-A",
                stock=80,
                standard_stock=100,
                remaining_rate=0.8,
                status=StockStatus.SUFFICIENT,
            )
        ]
        output = render_stock_report(reports)
        assert "S1" in output
        assert "Wafer-A" in output
        assert "80.0%" in output
        assert StockStatus.SUFFICIENT.value in output

    def test_handles_empty_reports(self):
        output = render_stock_report([])
        assert "등록된 시료가 없습니다" in output
