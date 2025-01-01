from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

"""
equality_expr ::= relational_expr
                | equality_expr ("==" | "!=") relational_expr
"""
class EquilityLogicalCheck:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        left = parser.parse_relational_expr()

        while not parser.is_at_end():
            # On teste si on a "==" ou "!="
            if parser.match('OPERATOR', '=='):
                parser.consume('OPERATOR', '==')
                right = parser.parse_relational_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "==",
                    "left": left,
                    "right": right
                }
            elif parser.match('OPERATOR', '!='):
                parser.consume('OPERATOR', '!=')
                right = parser.parse_relational_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "!=",
                    "left": left,
                    "right": right
                }
            else:
                break  # on sort de la boucle

        return left