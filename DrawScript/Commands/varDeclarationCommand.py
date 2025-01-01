from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

'''
var IDENTIFIER [":" IDENTIFIER] "=" EXPRESSION ";" 
'''
class VarDeclarationCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):

        line_num = parser.current_token()["line"]
        if not parser.match('KEYWORD', 'var'):
            raise ParserError("Déclaration de variable invalide : mot-clé 'var' attendu avant ton identificateur.")
        parser.consume('KEYWORD', 'var')
        if not parser.match('IDENTIFIER'):
            raise ParserError("Déclaration de variable invalide : identifiant attendu après 'var'.")
        id_token = parser.consume('IDENTIFIER')
        var_name = id_token['value']
        var_type = None

        if parser.match('DELIMITER', ':'):
            parser.consume('DELIMITER', ':')
            # On attend un identifiant pour le type
            # (et tu peux exiger qu’il soit "cursor", ou pas)
            type_token = parser.consume('IDENTIFIER')
            var_type = type_token['value']  # ex. "cursor"

        # 4) On s'attend à un '=' (token ASSIGN)
        if not parser.match('ASSIGN', '='):
            raise ParserError(f"Déclaration invalide pour '{var_name}' : signe '=' attendu.")
        parser.consume('ASSIGN', '=')

        # 5) Parse l'expression qui suit le '='
        expr = parser.parse_expression()

        # 6) On s'attend à un point-virgule final
        if not parser.match('DELIMITER', ';'):
            raise ParserError(f"Point-virgule manquant après la déclaration de '{var_name}'.")
        parser.consume('DELIMITER', ';')

        return {
            "node_type": "var_declaration",
            "name": var_name,
            "type": var_type,
            "expression": expr,
            "line": line_num  
        }