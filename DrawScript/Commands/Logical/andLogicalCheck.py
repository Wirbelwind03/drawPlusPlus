from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

"""
logical_and_expr ::= equality_expr
                | logical_and_expr "&&" equality_expr
"""
class AndLogicalCheck:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        left = parser.parse_equality_expr()

        while parser.match('OPERATOR', '&&'):
            op_token = parser.consume('OPERATOR', '&&')
            right = parser.parse_equality_expr()
            left = {
                "node_type": "binary_op",
                "op": "&&",
                "left": left,
                "right": right
            }

        return left