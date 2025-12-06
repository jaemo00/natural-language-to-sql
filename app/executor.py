# app/executor.py

import pymysql
from .config import DB_CONFIG


def execute_query(sql: str):
    """
    주어진 SQL 문자열을 MySQL에 보내고 결과를 반환한다.
    - 주로 SELECT 문을 실행한다고 가정하고 설계.
    - 결과는 (튜플) 리스트로 반환됨.
    """
    # DB 연결 열기
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
        cursorclass=pymysql.cursors.DictCursor,  # 결과를 dict 형태로 받기 위해
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            # SELECT 문이라고 가정하고 결과 가져오기
            rows = cursor.fetchall()
            return rows
    finally:
        conn.close()
