# Natural language → ParsedQuery (skeleton)

class ParsedQuery:
    def __init__(self, table="users", columns=None, conditions=None):
        self.table = table
        self.columns = columns or ["*"]
        self.conditions = conditions or []

def parse_korean_query(table:str,columns:str,conditions:str) -> ParsedQuery:
    #1.1 ,로 구분된 문자열을 리스트로 변환
    columns= columns.split(",") if columns else ["*"]
    conditions= conditions.split(",") if conditions else []
    return ParsedQuery(table,columns,conditions)