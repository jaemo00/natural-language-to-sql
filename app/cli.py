# Simple CLI interface (skeleton)


from .parser import parse_korean_query
from .sql_builder import build_sql
from .executor import execute_query

def main():
    print("=== NL → SQL Assistant ===")
    table = input("table 입력: ")
    columns= input("columns 입력 (쉼표로 구분): ")
    conditions = input("conditions 입력 (쉼표로 구분): ")

    pq = parse_korean_query(table,columns,conditions)
    sql = build_sql(pq)

    print("\n[생성된 SQL]")
    print(sql)

    print("\n[결과]")
    rows = execute_query(sql)

    # 예쁘게 출력
    if not rows:
        print("(결과 없음)")
    else:
        for row in rows:
            print(row)

    # print("\n[결과]")
    # rows = execute_query(sql)
    # print(rows)

if __name__ == "__main__":
    main()