from DrawScript.Core.drawScriptParser import DrawScriptParser

"""
if "(" EXPRESSION ")" BLOCK [ "else" BLOCK ]
"""
class IfStatementCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):

        # On récupère la ligne du token 'if'
        line_num = parser.current_token()["line"]
        parser.consume('KEYWORD', 'if')

        parser.consume('DELIMITER', '(')
        condition = parser.parse_expression()
        parser.consume('DELIMITER', ')')
        then_block = parser.parse_block()

        else_block = None
        if parser.match('KEYWORD', 'else'):
            parser.consume('KEYWORD', 'else')
            else_block = parser.parse_block()

        return {
            "node_type": "if_statement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block,
            "line": line_num
        }