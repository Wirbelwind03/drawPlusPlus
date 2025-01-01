from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

class ForStatementCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        line_num = parser.current_token()["line"]
        parser.consume('KEYWORD', 'for')
        parser.consume('DELIMITER', '(')
        init_node = parser.parse_for_init()
        parser.consume('DELIMITER', ';')
        # parse expression (condition)
        condition_node = parser.parse_expression()
        parser.consume('DELIMITER', ';')
        # parse l'incrément (on passe par une assignation en premier donc c'est bon)
        increment_node = parser.parse_expression()
        parser.consume('DELIMITER', ')')
        # parse le block { ... }
        body_node = parser.parse_block()
        return {
            "node_type": "for_statement",
            "init": init_node,
            "condition": condition_node,
            "increment": increment_node,
            "body": body_node,
            "line": line_num
        }