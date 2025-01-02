from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Exceptions.parserError import ParserError

'''
var IDENTIFIER [":" IDENTIFIER] "=" EXPRESSION ";" 
'''
class FunctionDeclarationCommand:
    def __init__(self):
        pass

    def execute(parser: DrawScriptParser):
        line_num = parser.current_token()["line"]
        parser.consume('KEYWORD', 'function')
        func_name = parser.consume('IDENTIFIER')
        parser.consume('DELIMITER', '(')
        # parse paramètres (optionnels)
        param_list = []
        if not parser.match('DELIMITER', ')'):
            param_list = parser.parse_parameter_list()
        parser.consume('DELIMITER', ')')
        func_body = parser.parse_block()
        return {
            "node_type": "function_declaration",
            "name": func_name["value"],
            "params": param_list,
            "body": func_body,
            "line": line_num
        }