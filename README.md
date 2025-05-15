# 🧠 SNK Quiz API

Python 3.9.6 기반의 FastAPI 프로젝트로, 관리자/사용자 기반 **퀴즈 응시 서비스 API**를 구현했습니다.

---
## ⚙️ 기술 스택

| 항목         | 사용 기술                |
|--------------|--------------------------|
| 언어         | Python 3.9.6             |
| 웹 프레임워크| FastAPI                  |
| ORM          | SQLAlchemy               |
| DB           | PostgreSQL               |
| 마이그레이션 | Alembic                  |
| 테스트       | Pytest                   |
| 컨테이너     | Docker, Docker Compose   |
| 문서화       | Swagger (`/docs`)        |

---

## 🗂️ 디렉토리 구조

```
app/
├── core/                # DB 연결, 공통 의존성
├── quiz/                # 퀴즈 도메인
│   ├── application/     # 서비스, DTO
│   ├── domain/          # 모델 정의
│   └── interface/       # 라우터 정의
├── user/                # 사용자 도메인
└── main.py              # FastAPI 엔트리포인트
```

---

## 🚀 실행 방법

```bash
# 도커 빌드 및 실행
docker-compose build --no-cache
docker-compose up
```

---

## 🧪 테스트

```bash
# 테스트 실행 (미완성)
docker-compose exec web poetry run pytest -x
```

---

## 🔐 인증 방식

- 모든 요청은 `X-User-Id` 헤더 필수
- `1`번 유저는 관리자
- `2~4`번 유저는 일반 사용자

---

## 🧾 Swagger API 문서 테스트 팁

- 주소: [`http://localhost:8000/docs`](http://localhost:8000/docs)

---

## 🧑‍💼 시드 데이터

| ID | 이메일             | 관리자 여부 |
|----|--------------------|------------|
| 1  | admin@example.com  | ✅         |
| 2  | user1@example.com  | ❌         |
| 3  | user2@example.com  | ❌         |
| 4  | user3@example.com  | ❌         |

---

## ✅ 예시 퀴즈 생성 요청

```json
{
  "title": "예시 퀴즈",
  "question_count": 2,
  "is_question_order_random": true,
  "is_option_order_random": true,
  "questions": [
    {
      "text": "질문 1",
      "options": [
        {"text": "A", "is_correct": true},
        {"text": "B", "is_correct": false},
        {"text": "C", "is_correct": false}
      ]
    },
    {
      "text": "질문 2",
      "options": [
        {"text": "1", "is_correct": false},
        {"text": "2", "is_correct": false},
        {"text": "3", "is_correct": true}
      ]
    }
  ]
}
```

---
