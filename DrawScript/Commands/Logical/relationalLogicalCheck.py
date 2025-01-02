from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

"""
relational_expr ::= additive_expr
                | relational_expr ("<" | "<=" | ">" | ">=") additive_expr
"""
class RelationalLogicalCheck:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        left = parser.parse_additive_expr()

        while not parser.is_at_end():
            if parser.match('OPERATOR', '<'):
                parser.consume('OPERATOR', '<')
                right = parser.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "<",
                    "left": left,
                    "right": right
                }
            elif parser.match('OPERATOR', '<='):
                parser.consume('OPERATOR', '<=')
                right = parser.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "<=",
                    "left": left,
                    "right": right
                }
            elif parser.match('OPERATOR', '>'):
                parser.consume('OPERATOR', '>')
                right = parser.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": ">",
                    "left": left,
                    "right": right
                }
            elif parser.match('OPERATOR', '>='):
                parser.consume('OPERATOR', '>=')
                right = parser.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": ">=",
                    "left": left,
                    "right": right
                }
            else:
                break

        return left