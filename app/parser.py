# Natural language → ParsedQuery (skeleton)

class ParsedQuery:
    def __init__(self, table="users", columns=None, conditions=None):
        self.table = table
        self.columns = columns or ["*"]
        self.conditions = conditions or []

def parse_korean_query(text: str) -> ParsedQuery:
    # TODO: Implement real parsing rules here
    return ParsedQuery()