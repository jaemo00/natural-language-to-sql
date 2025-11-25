# Build SQL from ParsedQuery (skeleton)

from .parser import ParsedQuery

def build_sql(parsed: ParsedQuery) -> str:
    sql = f"SELECT {', '.join(parsed.columns)} FROM {parsed.table}"
    if parsed.conditions:
        cond_str = " AND ".join(parsed.conditions)
        sql += f" WHERE {cond_str}"
    return sql + ";"