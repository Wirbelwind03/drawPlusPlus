from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

"""
logical_or_expr ::= logical_and_expr
                | logical_or_expr "||" logical_and_expr
"""
class OrLogicalCheck:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):

        left = parser.parse_logical_and_expr()

        # Tant qu'on trouve l’opérateur "||" (type='OPERATOR', value='||'), on enchaîne
        while parser.match('OPERATOR', '||'):
            op_token = parser.consume('OPERATOR', '||')
            right = parser.parse_logical_and_expr()
            left = {
                "node_type": "binary_op",
                "op": "||",
                "left": left,
                "right": right
            }

        return left