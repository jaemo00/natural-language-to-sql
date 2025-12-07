# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.parser import parse_korean_query
from app.sql_builder import build_sql
from app.executor import execute_query, execute_non_query
from app.llm_local import generate_sql_from_nl_ollama


app = FastAPI()

# static 폴더를 /static 경로로 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")


class QueryRequest(BaseModel):
    table: str
    columns: str | None = None
    conditions: str | None = None

class NLRequest(BaseModel):
    message: str

class UserCreate(BaseModel):
    name: str
    age: int | None = None
    city: str | None = None

class OrderCreate(BaseModel):
    user_id: int
    product: str
    price: int


@app.get("/", response_class=HTMLResponse)
async def index():
    # templates/index.html 파일 내용을 그대로 읽어서 반환
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/api/users")
async def get_users():
    rows = execute_query(
        "SELECT id, name, age, city, created_at FROM users ORDER BY id"
    )
    return {"rows": rows}


@app.post("/api/users")
async def create_user(body: UserCreate):
    try:
        affected = execute_non_query(
            "INSERT INTO users (name, age, city) VALUES (%s, %s, %s)",
            (body.name, body.age, body.city),
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
        )

    rows = execute_query("SELECT LAST_INSERT_ID() AS id")
    new_id = rows[0]["id"] if rows else None

    return {"id": new_id, "affected": affected}

@app.post("/api/orders")
async def add_order(order: OrderCreate):
    try:
        sql = """
        INSERT INTO orders (user_id, product, price)
        VALUES (%s, %s, %s)
        """
        params = (order.user_id, order.product, order.price)
        execute_non_query(sql, params)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
        )

    # 성공 응답
    return {"message": "주문 추가 완료!"}

@app.post("/api/query")
async def run_query(body: QueryRequest):
    pq = parse_korean_query(body.table, body.columns or "", body.conditions or "")
    sql = build_sql(pq)

    try:
        rows = execute_query(sql)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"sql": sql, "error": str(e), "rows": []},
        )

    return {"sql": sql, "rows": rows}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    """
    id 기준으로 users 테이블에서 한 행 삭제.
    """
    try:
        affected = execute_non_query(
            "DELETE FROM users WHERE id = %s",
            (user_id,),
        )
    except Exception as e:
        # 예: 외래키 제약(orders.user_id가 참조 중이면 삭제 실패)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
        )

    if affected == 0:
        # 삭제된 행이 없으면 ID가 없는 것
        return JSONResponse(
            status_code=404,
            content={"error": "해당 ID 사용자가 없습니다."},
        )

    return {"id": user_id, "affected": affected}

@app.get("/api/orders")
async def get_orders():
    """
    orders 전체 + user 이름 조인해서 보여주기
    """
    rows = execute_query("""
        SELECT
            o.id,
            o.user_id,
            u.name AS user_name,
            o.product,
            o.price,
            o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.id
    """)
    return {"rows": rows}


@app.delete("/api/orders/{order_id}")
async def delete_order(order_id: int):
    """
    해당 order 한 건 삭제
    """
    try:
        affected = execute_non_query(
            "DELETE FROM orders WHERE id = %s",
            (order_id,),
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
        )

    if affected == 0:
        return JSONResponse(
            status_code=404,
            content={"error": "해당 주문이 없습니다."},
        )

    return {"id": order_id, "affected": affected}


@app.post("/api/nl2sql")
async def nl2sql_endpoint(body: NLRequest):
    # 1) LLM에게 자연어 → SQL 생성 요청
    try:
        sql = generate_sql_from_nl_ollama(body.message)
        sql = sql.replace("= ' ", "= '").replace(" ='", " = '").replace("  ", " ")
        sql = sql.strip()

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"LLM 호출 실패: {str(e)}"},
        )

    # 2) 생성된 SQL을 MySQL에 실행
    try:
        rows = execute_query(sql)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"SQL 실행 에러: {str(e)}",
                "sql": sql,
            },
        )

    return {"sql": sql, "rows": rows}