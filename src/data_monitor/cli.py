"""Data Monitor 콘솔 진입점.

담당자가 메뉴에서 조회를 반복 실행하며 최신 주문/재고 현황을
확인할 수 있는 콘솔 루프를 제공한다.
"""

from __future__ import annotations

from data_monitor.monitor import build_stock_reports, count_orders_by_status
from data_monitor.repository import InMemoryRepository, build_dummy_repository
from data_monitor.view import render_order_summary, render_stock_report

MENU = """
[Data Monitor]
1. 주문 현황 조회
2. 재고 현황 조회
3. 전체 조회
0. 종료
> """


def show_order_summary(repository: InMemoryRepository) -> str:
    counts = count_orders_by_status(repository.list_orders())
    return render_order_summary(counts)


def show_stock_report(repository: InMemoryRepository) -> str:
    reports = build_stock_reports(repository.list_samples())
    return render_stock_report(reports)


def main() -> None:
    repository = build_dummy_repository()

    while True:
        choice = input(MENU).strip()
        if choice == "1":
            print(show_order_summary(repository))
        elif choice == "2":
            print(show_stock_report(repository))
        elif choice == "3":
            print(show_order_summary(repository))
            print(show_stock_report(repository))
        elif choice == "0":
            print("Data Monitor를 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
