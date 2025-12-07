# app/llm_local.py

import json
import requests

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"  


SYSTEM_PROMPT = """
You are an assistant that converts Korean natural language into MySQL SELECT queries.

The database schema is:

TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    city VARCHAR(50),
    created_at DATETIME
);

TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product VARCHAR(100),
    price INT,
    created_at DATETIME
);

Rules:
- Only use these tables and columns.
- Generate exactly ONE MySQL SELECT query.
- Do NOT include explanation.
- Do NOT wrap the SQL with backticks.
- If the question is ambiguous, choose a reasonable interpretation and still output one SELECT.
- The output MUST be only SQL text.
- 문자열 상수 양쪽에는 불필요한 공백을 넣지 마세요. 예) city = 'Seoul' (O), city = ' Seoul' (X), city = 'Seoul ' (X)

""".strip()


def generate_sql_from_nl_ollama(nl: str) -> str:
    """
    Ollama 로컬 LLM을 호출해서 자연어 → SQL 문자열로 변환.
    Ollama의 /api/generate는 스트리밍 응답(JSONL)을 반환하므로
    이를 이어 붙여서 최종 텍스트를 만든다.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser: {nl}\nAssistant:",
        "stream": True,  # 스트리밍으로 조금씩 받기
    }

   
    response = requests.post(url, json=payload, stream=True)
    response.raise_for_status()

    full_text = ""

    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        # {"response": "...", "done": false/true, ...}
        part = data.get("response", "")
        full_text += part
        if data.get("done"):
            break

    sql = full_text.strip()
    return sql
