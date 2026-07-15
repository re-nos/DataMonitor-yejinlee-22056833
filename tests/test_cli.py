from data_monitor.cli import show_order_summary, show_stock_report
from data_monitor.repository import build_dummy_repository


class TestCliRenderHelpers:
    def test_show_order_summary_uses_repository_data(self):
        repository = build_dummy_repository()
        output = show_order_summary(repository)
        assert "주문 현황" in output

    def test_show_stock_report_uses_repository_data(self):
        repository = build_dummy_repository()
        output = show_stock_report(repository)
        assert "시료 재고 현황" in output
        assert "SMP-001" in output
