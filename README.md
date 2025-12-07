#  NL2SQL MySQL Assistant  
자연어 → MySQL SELECT 쿼리 자동 변환 서비스  
(Natural Language to SQL Converter with MySQL + FastAPI + Local LLM)

---

## ✨ 프로젝트 소개

> 사용자가 한국어로 질의하면, MySQL 데이터베이스에 맞는 SQL을 자동으로 생성하고 실행하는 오픈소스입니다.

이 프로젝트는 **두 가지 SQL 생성 모드**를 제공합니다.

| 기능 | 설명 |
|------|------|
| 📝 수동 SQL 생성 | table / columns / conditions 직접 입력 → SQL 생성 & 실행 |
| 💬 LLM 기반 자동 SQL 생성 | 자연어 입력 → 로컬 LLM(Ollama) → SQL 자동 생성 & 실행 |

또한 웹 화면에서
- users / orders 데이터 삽입
- DB 데이터 실시간 조회
- 데이터 삭제  
기능도 제공합니다.

---

## 🎬 데모 (Demo)

> 아래 GIF는 프로젝트 실행 화면을 시연한 모습입니다.

(📌 TODO: 시연 GIF 파일 추가 후 경로 작성)

```md
![NL2SQL Demo](./demo/demo_nl2sql.gif)


## 실행 방법

```bash
python -m app.cli
