# Data Monitor PoC

S-Semi 반도체 시료 생산주문관리 시스템의 **데이터 모니터링 Tool** PoC 입니다.
상태별 주문 건수(REJECTED 제외)와 시료별 재고 현황(여유/부족/고갈, 잔여율)을 콘솔에서 조회할 수 있습니다.

이 저장소는 독립 PoC이므로, 실제 DataPersistence 저장소를 참조하지 않고
자체 인메모리 더미 데이터로 동작을 검증합니다.

## 요구 사항

- Python 3.10 이상

## 설치

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 의존성 설치 (pytest 포함)
pip install -e ".[dev]"
```

## 실행

```bash
python -m data_monitor.cli
```

메뉴에서 번호를 입력해 조회합니다.

```
[Data Monitor]
1. 주문 현황 조회
2. 재고 현황 조회
3. 전체 조회
0. 종료
>
```

- `1`: 상태별 주문 건수 조회 (RESERVED / PRODUCING / CONFIRMED / RELEASE, REJECTED 제외)
- `2`: 시료별 재고 수량, 잔여율, 상태(여유/부족/고갈) 조회
- `3`: 주문 현황과 재고 현황을 함께 조회
- `0`: 프로그램 종료

## 테스트

```bash
pytest
```

가상환경을 활성화하지 않아도 `pyproject.toml`의 `pythonpath = ["src"]` 설정 덕분에
`data_monitor` 패키지를 정상적으로 임포트해 테스트를 실행할 수 있습니다.

## 프로젝트 구조

```
src/data_monitor/
├── models.py       # Sample, Order, OrderStatus 도메인 모델
├── repository.py   # 인메모리 더미 데이터 저장소
├── monitor.py       # 주문량/재고 현황 집계 로직
├── view.py          # 콘솔 출력 포맷팅
└── cli.py           # 메뉴 기반 콘솔 진입점

tests/               # 각 모듈에 대응하는 pytest 테스트
```

## 재고 상태 판정 기준

잔여율 = 현재 재고 / 기준 재고(`standard_stock`)

| 상태 | 조건 |
| --- | --- |
| 고갈 | 재고 0개 |
| 부족 | 잔여율 30% 미만 |
| 여유 | 그 외 |
