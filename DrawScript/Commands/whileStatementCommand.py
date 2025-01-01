from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

class WhileStatementCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):

        line_num = parser.current_token()["line"]
        parser.consume('KEYWORD', 'while')
        parser.consume('DELIMITER', '(')
        condition_node = parser.parse_expression()
        parser.consume('DELIMITER', ')')
        body_node = parser.parse_block()

        return {
            "node_type": "while_statement",
            "condition": condition_node,
            "body": body_node,
            "line": line_num
        }