from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

"""
parse_empty_statement ::= ";"
"""
class EmptyStatementCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        # On consomme le point-virgule
        parser.consume('DELIMITER', ';')
        # On renvoie un nœud vide (ou un dict indiquant un empty statement)
        return {
            "node_type": "empty_statement"
        }