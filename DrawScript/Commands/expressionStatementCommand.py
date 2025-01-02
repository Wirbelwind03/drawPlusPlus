from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

class ExpressionStatementCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        line_num = -1
        if not parser.is_at_end():
            line_num = parser.current_token()["line"]

        expr = parser.parse_expression()
        parser.consume('DELIMITER', ';')
        return {
            "node_type": "expression_statement",
            "expression": expr,
            "line": line_num
        }