class ParserError(Exception):
    pass

class DrawScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []

    def parse(self):
        """
        Méthode principale du parseur qui parcourt tous les tokens
        et parse 'statement' jusqu'à la fin.
        Retourne une liste de nœuds AST (ou None si erreur fatale).
        """
        ast_nodes = []
        # Tant qu'on n'a pas atteint la fin
        while not self.is_at_end():
            stmt = self.parse_statement()  # tente de parser un statement
            if stmt is not None:
                ast_nodes.append(stmt)
        return ast_nodes, self.errors

    # ----------------- Méthodes utilitaires -------------------
    def advance(self):
        if not self.is_at_end():
            self.current_token_index += 1

    def current_token(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current_token_index]

    def previous_token(self):
        if self.current_token_index == 0:
            return None
        return self.tokens[self.current_token_index - 1]

    def is_at_end(self):
        return self.current_token_index >= len(self.tokens)

    def match(self, expected_type, expected_value=None):
        if self.is_at_end():
            return False
        token = self.current_token()
        if token["type"] != expected_type:
            return False
        if expected_value is not None and token["value"] != expected_value:
            return False
        return True

    def consume(self, expected_type, expected_value=None):
        """
        Consume le token courant s'il correspond (type, value).
        Sinon, lève une ParserError.
        """
        if self.is_at_end():
            raise ParserError(
                f"Fin de fichier inattendue (attendu '{expected_type}' / '{expected_value}')."
            )
        token = self.current_token()
        if token["type"] != expected_type:
            raise ParserError(
                f"Type de token inattendu à la ligne {token['line']}. "
                f"Attendu '{expected_type}', reçu '{token['type']}' (valeur='{token['value']}')."
            )
        if expected_value is not None and token["value"] != expected_value:
            raise ParserError(
                f"Valeur de token inattendue à la ligne {token['line']}. "
                f"Attendu '{expected_value}', reçu '{token['value']}'."
            )
        self.advance()
        return token

    def synchronize(self):
        """
        Sauter des tokens jusqu'à trouver un délimiteur fiable
        pour reprendre (par ex: ';' ou '}' etc.).
        """
        while not self.is_at_end():
            prev = self.previous_token()
            if prev and prev["value"] == ";":
                return
            curr = self.current_token()
            if curr["type"] == "DELIMITER" and curr["value"] in ("}",):
                return
            self.advance()

    # ----------------- Parsing statements -------------------
    def parse_statement(self):
        """
        Parse un statement en fonction du token courant
        """
        try:
            return self._parse_statement_internal()
        except ParserError as e:
            # On stocke l'erreur et on sync
            line = self.current_token()['line'] if not self.is_at_end() else -1
            self.errors.append({"message": str(e), "line": line})
            self.synchronize()
            return None

    def _parse_statement_internal(self):
        """
        Logique interne qui peut lever ParserError.
        """
        if self.match('KEYWORD', 'var'):
            return self.parse_var_declaration()
        
        # if statement
        if self.match('KEYWORD', 'if'):
            return self.parse_if_statement()
        
        if self.match('IDENTIFIER'):
            return self.parse_var_declaration()

        # etc. si 'for', 'while', ...
        
        # Sinon, c'est potentiellement une expression statement
        return self.parse_expression_statement()

    def parse_var_declaration(self):
        '''
        var IDENTIFIER [":" IDENTIFIER] "=" EXPRESSION ";" 
        '''
        # 1) On s'attend impérativement à un mot-clé 'var'
        if not self.match('KEYWORD', 'var'):
            raise ParserError("Déclaration de variable invalide : mot-clé 'var' attendu avant ton identificateur.")
        self.consume('KEYWORD', 'var')

        # 2) On s'attend à un identifiant après 'var'
        if not self.match('IDENTIFIER'):
            raise ParserError("Déclaration de variable invalide : identifiant attendu après 'var'.")
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        var_type = None

        # 3)Condition Bonus, type de phrase non vérifié dans le parseur, Vérifie si on a ':' pour un typage optionnel
        '''if self.match('DELIMITER', ':'):
            self.consume('DELIMITER', ':')
            if not self.match('IDENTIFIER'):
                raise ParserError(f"Typage invalide pour la variable '{var_name}': nom de type attendu.")
            type_token = self.consume('IDENTIFIER')
            var_type = type_token['value']
        '''
        # 4) On s'attend à un '=' (token ASSIGN)
        if not self.match('ASSIGN', '='):
            raise ParserError(f"Déclaration invalide pour '{var_name}' : signe '=' attendu.")
        self.consume('ASSIGN', '=')

        # 5) Parse l'expression qui suit le '='
        expr = self.parse_expression()

        # 6) On s'attend à un point-virgule final
        if not self.match('DELIMITER', ';'):
            raise ParserError(f"Point-virgule manquant après la déclaration de '{var_name}'.")
        self.consume('DELIMITER', ';')

        return {
            "node_type": "var_declaration",
            "name": var_name,
            "type": var_type,
            "expression": expr
        }


    def parse_if_statement(self):
        """
        if "(" EXPRESSION ")" BLOCK [ "else" BLOCK ]
        """
        if not self.match('KEYWORD', 'if'):
            raise ParserError("Instruction 'if' invalide : mot-clé 'if' attendu.")
        self.consume('KEYWORD', 'if')

        if not self.match('DELIMITER', '('):
            raise ParserError("Syntaxe 'if' invalide : '(' attendu après 'if'.")
        self.consume('DELIMITER', '(')

        # Parse l'expression dans les parenthèses
        condition = self.parse_expression()

        if not self.match('DELIMITER', ')'):
            raise ParserError("Syntaxe 'if' invalide : ')' manquant après la condition.")
        self.consume('DELIMITER', ')')

        # Parse le bloc suivant
        then_block = self.parse_block()

        # Si on a un 'else', on parse un second bloc
        else_block = None
        if self.match('KEYWORD', 'else'):
            self.consume('KEYWORD', 'else')
            else_block = self.parse_block()

        return {
            "node_type": "if_statement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block
        }


    def parse_block(self):
        """
        "{" { statement } "}"
        """
        self.consume('DELIMITER', '{')
        statements = []
        while not self.is_at_end() and not self.match('DELIMITER', '}'):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.consume('DELIMITER', '}')
        return {
            "node_type": "block",
            "statements": statements
        }

    def parse_expression_statement(self):
        """
        EXPR ";"
        """
        expr = self.parse_expression()
        self.consume('DELIMITER', ';')
        return {
            "node_type": "expression_statement",
            "expression": expr
        }

    def parse_expression(self):
        """
        Pour l'exemple, on va juste consommer un IDENTIFIER ou un NUMBER...
        (À toi de l'implémenter selon la grammaire)
        """
        if self.match('IDENTIFIER'):
            token = self.consume('IDENTIFIER')
            return {"node_type": "identifier", "value": token["value"]}

        if self.match('NUMBER'):
            token = self.consume('NUMBER')
            return {"node_type": "number", "value": token["value"]}

        # etc. Gérer OPERATOR, parenthèses, etc.
        raise ParserError("Expression invalide.")









"""
----------------------------------------------------------------------------------------------------------------------
TEST DU PARSER AVEC UN CODE "REEL"
----------------------------------------------------------------------------------------------------------------------
"""
#tokens corrects : 

correct_tokens = [
{'type': 'KEYWORD', 'value': 'var', 'line': 8},
{'type': 'IDENTIFIER', 'value': 'centerX', 'line': 8},
{'type': 'ASSIGN', 'value': '=', 'line': 8},
{'type': 'NUMBER', 'value': 300.0, 'line': 8},
{'type': 'DELIMITER', 'value': ';', 'line': 8},
{'type': 'KEYWORD', 'value': 'var', 'line': 9},
{'type': 'IDENTIFIER', 'value': 'centerY', 'line': 9},
{'type': 'ASSIGN', 'value': '=', 'line': 9},
{'type': 'NUMBER', 'value': 300.0, 'line': 9},
{'type': 'DELIMITER', 'value': ';', 'line': 9},
{'type': 'KEYWORD', 'value': 'var', 'line': 10},
{'type': 'IDENTIFIER', 'value': 'radius', 'line': 10},
{'type': 'ASSIGN', 'value': '=', 'line': 10},
{'type': 'NUMBER', 'value': 50.0, 'line': 10},
{'type': 'DELIMITER', 'value': ';', 'line': 10}
    # il manque des tokens donc il y aura une erreur EOF
]


#tokens incorrects : 

incorrect_tokens = [
    {'type': 'KEYWORD', 'value': 'var', 'line': 9},
    {'type': 'IDENTIFIER', 'value': 'canvasWidth', 'line': 9},
    {'type': 'OPERATOR', 'value': '=', 'line': 9},
    {'type': 'NUMBER', 'value': 800.0, 'line': 9},
    # Manque le point-virgule ici (ligne 9)
    {'type': 'KEYWORD', 'value': 'var', 'line': 10},
    {'type': 'IDENTIFIER', 'value': 'canvasHeight', 'line': 10},
    {'type': 'OPERATOR', 'value': '=', 'line': 10},
    {'type': 'NUMBER', 'value': 600.0, 'line': 10},
    {'type': 'DELIMITER', 'value': ';', 'line': 10},
    {'type': 'KEYWORD', 'value': 'var', 'line': 11},
    {'type': 'IDENTIFIER', 'value': 'centerX', 'line': 11},
    {'type': 'OPERATOR', 'value': '=', 'line': 11},
    {'type': 'IDENTIFIER', 'value': 'canvasWidth', 'line': 11},
    {'type': 'OPERATOR', 'value': '/', 'line': 11},
    {'type': 'NUMBER', 'value': 2.0, 'line': 11},
    {'type': 'DELIMITER', 'value': ';', 'line': 11},
    {'type': 'KEYWORD', 'value': 'var', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'centerY', 'line': 12},
    {'type': 'OPERATOR', 'value': '=', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'canvasHeight', 'line': 12},
    {'type': 'OPERATOR', 'value': '/', 'line': 12},
    {'type': 'NUMBER', 'value': 2.0, 'line': 12},
    {'type': 'DELIMITER', 'value': ';', 'line': 12},
    {'type': 'KEYWORD', 'value': 'var', 'line': 13},
    {'type': 'IDENTIFIER', 'value': 'radius', 'line': 13},
    {'type': 'OPERATOR', 'value': '=', 'line': 13},
    {'type': 'NUMBER', 'value': 50.0, 'line': 13},
    {'type': 'DELIMITER', 'value': ';', 'line': 13},
    {'type': 'KEYWORD', 'value': 'var', 'line': 14},
    {'type': 'IDENTIFIER', 'value': 'numShapes', 'line': 14},
    {'type': 'OPERATOR', 'value': '=', 'line': 14},
    {'type': 'NUMBER', 'value': 10.0, 'line': 14},
    {'type': 'DELIMITER', 'value': ';', 'line': 14},
    {'type': 'KEYWORD', 'value': 'var', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'angle', 'line': 15},
    {'type': 'OPERATOR', 'value': '=', 'line': 15},
    {'type': 'NUMBER', 'value': 0.0, 'line': 15},
    {'type': 'DELIMITER', 'value': ';', 'line': 15},
    {'type': 'KEYWORD', 'value': 'var', 'line': 16},
    {'type': 'IDENTIFIER', 'value': 'speed', 'line': 16},
    {'type': 'OPERATOR', 'value': '=', 'line': 16},
    {'type': 'NUMBER', 'value': 0.1, 'line': 16},
    {'type': 'DELIMITER', 'value': ';', 'line': 16},
    {'type': 'KEYWORD', 'value': 'var', 'line': 17},
    {'type': 'IDENTIFIER', 'value': 'isAnimating', 'line': 17},
    {'type': 'OPERATOR', 'value': '=', 'line': 17},
    {'type': 'KEYWORD', 'value': 'true', 'line': 17},
    # Manque le point-virgule ici (ligne 17)
    # Erreur dans la déclaration du curseur (ligne 20)
    {'type': 'KEYWORD', 'value': 'var', 'line': 20},
    {'type': 'IDENTIFIER', 'value': 'myCursor', 'line': 20},
    {'type': 'DELIMITER', 'value': ':', 'line': 20},
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 20},
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 20},
    {'type': 'DELIMITER', 'value': '(', 'line': 20},
    {'type': 'IDENTIFIER', 'value': 'centerX', 'line': 20},
    {'type': 'DELIMITER', 'value': ',', 'line': 20},
    {'type': 'IDENTIFIER', 'value': 'centerY', 'line': 20},
    {'type': 'DELIMITER', 'value': ')', 'line': 20},
    {'type': 'DELIMITER', 'value': ';', 'line': 20},
    # Erreur dans la définition de la fonction (ligne 23)
    {'type': 'KEYWORD', 'value': 'function', 'line': 23},
    {'type': 'IDENTIFIER', 'value': 'drawCustomShape', 'line': 23},
    {'type': 'DELIMITER', 'value': '(', 'line': 23},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 23},
    {'type': 'DELIMITER', 'value': ',', 'line': 23},
    {'type': 'IDENTIFIER', 'value': 'y', 'line': 23},
    {'type': 'DELIMITER', 'value': ',', 'line': 23},
    {'type': 'IDENTIFIER', 'value': 'size', 'line': 23},
    {'type': 'DELIMITER', 'value': '{', 'line': 23},  # Manque la parenthèse fermante ')'
    # Corps de la fonction...
    # Le reste des tokens suit le même format, incluant les erreurs syntaxiques.
    # N'oubliez pas de copier tous les tokens restants ici pour votre test.
]



#script de test des tokens 

if __name__ == "__main__":
    # Pour tester le code correct
    parser = DrawScriptParser(correct_tokens)
    parsed_correct_tokens, correct_errors = parser.parse()

    # Afficher les erreurs du code correct (devrait être vide s'il n'y a pas d'erreurs)
    print("Erreurs dans le code correct:")
    for error in correct_errors:
        print(error)
    print("")
    print("Fin analyse erreur dans correct_tokens")
    # Pour tester le code avec des erreurs
    # parser = DrawScriptParser(incorrect_tokens)
    # parsed_incorrect_tokens, incorrect_errors = parser.parse()

    # Afficher les erreurs du code incorrect
    # print("Erreurs dans le code incorrect:")
    # for error in incorrect_errors:
    #    print(error)


