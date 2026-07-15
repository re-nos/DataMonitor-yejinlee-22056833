# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 참고하는 가이드입니다.

## 커밋 컨벤션

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 형식을 따릅니다.

```
<type>(<scope>): <subject>

<body>

<footer>
```

### type

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등 (동작에 영향 없는 변경)
- `refactor`: 기능 변경 없는 코드 리팩토링
- `perf`: 성능 개선
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드 설정, 패키지 매니저 설정 등 기타 변경
- `ci`: CI 설정 파일 및 스크립트 변경

### scope (선택)

변경 범위를 나타냅니다. 예: `monitor`, `parser`, `config` 등 모듈/기능 단위.

### subject

- 50자 이내로 간결하게 작성
- 현재형, 명령형으로 작성 (예: "추가한다" (X) → "추가" (O), "add" (O) → "added" (X))
- 마침표 없이 작성

### body (선택)

- 변경한 이유(why)를 중심으로 작성, 무엇을(what) 했는지는 코드로 충분히 설명되는 경우 생략
- 한 줄 72자 내외로 줄바꿈

### footer (선택)

- 이슈 트래커 참조: `Refs: #123`
- Breaking Change 명시: `BREAKING CHANGE: <설명>`

### 예시

```
feat(monitor): 데이터 수집 주기 설정 기능 추가

기존에는 수집 주기가 고정되어 있어 부하가 큰 환경에서
조정이 불가능했다. 설정 파일에서 주기를 지정할 수 있도록 변경.

Refs: #12
```

```
fix(parser): 빈 응답 처리 시 발생하는 예외 수정
```
