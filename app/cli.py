# Simple CLI interface (skeleton)

from .parser import parse_korean_query
from .sql_builder import build_sql
from .executor import execute_query

def main():
    print("=== NL → SQL Assistant ===")
    text = input("자연어 입력: ")

    pq = parse_korean_query(text)
    sql = build_sql(pq)

    print("\n[생성된 SQL]")
    print(sql)

    print("\n[결과]")
    rows = execute_query(sql)
    print(rows)

if __name__ == "__main__":
    main()