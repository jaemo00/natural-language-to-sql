# app/executor.py

import pymysql
from .config import DB_CONFIG


def _get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
        cursorclass=pymysql.cursors.DictCursor,  # dict 형태로 결과 받기
    )


def execute_query(sql: str, params: tuple | None = None):
    """
    SELECT용 함수: 결과를 rows 리스트로 반환.
    """
    conn = _get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return rows
    finally:
        conn.close()


def execute_non_query(sql: str, params: tuple | None = None) -> int:
    """
    INSERT / UPDATE / DELETE용 함수.
    - 영향 받은 row 개수를 반환.
    """
    conn = _get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
