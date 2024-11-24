class DrawScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  # Index du jeton courant
        self.errors = []  # Liste des erreurs syntaxiques détectées

    def parse(self):
        """
        Méthode principale du parseur qui commence l'analyse des tokens.
        Elle parcourt tous les tokens et appelle la méthode 'statement' pour chaque instruction.
        """
        try:
            while self.current < len(self.tokens):
                self.statement()
                # print(self.current)  # Ligne de débogage (peut être supprimée)
        except Exception as e:
            pass  # Ignorer les exceptions pour continuer l'analyse
        return self.tokens, self.errors

    def statement(self):
        """
        Analyse une instruction en fonction du type de jeton courant.
        Elle détermine le type d'instruction et appelle la méthode appropriée.
        """
        if self.match('KEYWORD', 'var'):
            self.variable_declaration()
        elif self.match('IDENTIFIER'):
            if self.lookahead(1) and self.lookahead(1)['type'] == 'OPERATOR' and self.lookahead(1)['value'] == '.':
                # Appel à une méthode du curseur
                self.cursor_method_call_statement()
            else:
                # Affectation ou appel de fonction
                self.assignment_or_function_call()
        elif self.match('KEYWORD', 'function'):
            self.function_definition()
        elif self.match('KEYWORD', 'if'):
            self.if_statement()
        elif self.match('KEYWORD', 'while'):
            self.while_loop()
        elif self.match('KEYWORD', 'for'):
            self.for_loop()
        elif self.match('KEYWORD', 'copy'):
            self.copy_paste_statement()
        elif self.match('KEYWORD', 'animate'):
            self.animation_block()
        elif self.match('KEYWORD', 'cursor'):
            self.cursor_statement()
        elif self.match('KEYWORD', 'return'):
            self.return_statement()
        elif self.match('COMMENT'):
            # Ignorer les commentaires
            self.advance()
        else:
            # Si aucun des cas précédents ne correspond, enregistrer une erreur
            self.record_error("Unexpected token in statement")

    def return_statement(self):
        """
        Analyse une instruction 'return'.
        """
        self.consume('KEYWORD', 'return')
        self.expression()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def variable_declaration(self, expect_semicolon=True):
        """
        Analyse une déclaration de variable.
        Si 'expect_semicolon' est True, attend un point-virgule à la fin.
        """
        self.consume('KEYWORD', 'var')
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if self.match('DELIMITER', ':'):
            self.advance()
            if not (self.consume('IDENTIFIER') or self.consume('KEYWORD')):
                self.record_error('TYPE')
                return
        if self.match('OPERATOR', '='):
            self.advance()
            self.expression()
        if expect_semicolon:
            if not self.consume('DELIMITER', ';'):
                self.record_error('DELIMITER')

    def assignment_or_function_call(self):
        """
        Détermine si l'instruction est une affectation ou un appel de fonction.
        """
        self.consume('IDENTIFIER')
        if self.match('OPERATOR', '='):
            # Affectation
            self.advance()
            self.expression()
            if not self.consume('DELIMITER', ';'):
                self.record_error('DELIMITER')
        elif self.match('DELIMITER', '('):
            # Appel de fonction
            self.function_call()
        else:
            self.record_error('OPERATOR or DELIMITER')

    def function_definition(self):
        """
        Analyse la définition d'une fonction.
        """
        self.consume('KEYWORD', 'function')
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ')'):
            # Paramètres de la fonction
            self.parameter_list()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        # Corps de la fonction
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def function_call(self):
        """
        Analyse un appel de fonction.
        """
        self.consume('DELIMITER', '(')
        if not self.match('DELIMITER', ')'):
            # Arguments de la fonction
            self.argument_list()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def if_statement(self):
        """
        Analyse une instruction 'if' avec une clause optionnelle 'else'.
        """
        self.consume('KEYWORD', 'if')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        self.expression()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        # Bloc 'if'
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')
            return
        if self.match('KEYWORD', 'else'):
            # Bloc 'else' optionnel
            self.advance()
            if not self.consume('DELIMITER', '{'):
                self.record_error('DELIMITER')
                return
            while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
                self.statement()
            if not self.consume('DELIMITER', '}'):
                self.record_error('DELIMITER')

    def while_loop(self):
        """
        Analyse une boucle 'while'.
        """
        self.consume('KEYWORD', 'while')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        self.expression()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        # Corps de la boucle
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def for_loop(self):
        """
        Analyse une boucle 'for'.
        """
        self.consume('KEYWORD', 'for')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ';'):
            # Initialisation
            self.initialization()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')
            return
        # Condition
        self.expression()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ')'):
            # Incrémentation
            self.iteration()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        # Corps de la boucle
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def copy_paste_statement(self):
        """
        Analyse une instruction 'copy' avec 'to'.
        """
        self.consume('KEYWORD', 'copy')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        # Coordonnées source
        self.coordinate_pair()
        if not self.consume('DELIMITER', ','):
            self.record_error('DELIMITER')
            return
        self.coordinate_pair()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('KEYWORD', 'to'):
            self.record_error('KEYWORD')
            return
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        # Coordonnées destination
        self.coordinate_pair()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def animation_block(self):
        """
        Analyse un bloc 'animate'.
        """
        self.consume('KEYWORD', 'animate')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('DELIMITER', ','):
            self.record_error('DELIMITER')
            return
        # Durée de l'animation
        self.expression()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        # Corps du bloc d'animation
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def cursor_statement(self):
        """
        Analyse une instruction 'cursor'.
        """
        self.consume('KEYWORD', 'cursor')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        # Coordonnées du curseur
        self.coordinate_pair()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def lookahead(self, n):
        """
        Regarde le 'n'-ième jeton à venir sans avancer le pointeur 'current'.
        """
        if self.current + n < len(self.tokens):
            return self.tokens[self.current + n]
        else:
            return None

    def coordinate_pair(self):
        """
        Analyse une paire de coordonnées (expression, expression).
        """
        self.expression()
        if not self.consume('DELIMITER', ','):
            self.record_error('DELIMITER')
            return
        self.expression()

    def initialization(self):
        """
        Analyse l'initialisation dans une boucle 'for'.
        """
        if self.match('KEYWORD', 'var'):
            self.variable_declaration(expect_semicolon=False)
        else:
            self.assignment()

    def iteration(self):
        """
        Analyse l'incrémentation dans une boucle 'for'.
        """
        self.assignment()

    def assignment(self):
        """
        Analyse une affectation.
        """
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('OPERATOR', '='):
            self.record_error('OPERATOR')
            return
        self.expression()

    def parameter_list(self):
        """
        Analyse une liste de paramètres dans une définition de fonction.
        """
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        while self.match('DELIMITER', ','):
            self.advance()
            if not self.consume('IDENTIFIER'):
                self.record_error('IDENTIFIER')
                return

    def argument_list(self):
        """
        Analyse une liste d'arguments dans un appel de fonction.
        """
        self.expression()
        while self.match('DELIMITER', ','):
            self.advance()
            self.expression()

    def expression(self):
        """
        Analyse une expression.
        """
        self.logical_or_expression()

    def logical_or_expression(self):
        """
        Analyse une expression logique avec l'opérateur '||'.
        """
        self.logical_and_expression()
        while self.match('OPERATOR', '||'):
            self.advance()
            self.logical_and_expression()

    def logical_and_expression(self):
        """
        Analyse une expression logique avec l'opérateur '&&'.
        """
        self.equality_expression()
        while self.match('OPERATOR', '&&'):
            self.advance()
            self.equality_expression()

    def equality_expression(self):
        """
        Analyse une expression d'égalité '==' ou de différence '!='.
        """
        self.relational_expression()
        while self.match('OPERATOR', '==') or self.match('OPERATOR', '!='):
            self.advance()
            self.relational_expression()

    def relational_expression(self):
        """
        Analyse une expression relationnelle ('<', '>', '<=', '>=').
        """
        self.additive_expression()
        while self.match('OPERATOR', '<') or self.match('OPERATOR', '>') or \
              self.match('OPERATOR', '<=') or self.match('OPERATOR', '>='):
            self.advance()
            self.additive_expression()

    def additive_expression(self):
        """
        Analyse une expression additive ('+' ou '-').
        """
        self.multiplicative_expression()
        while self.match('OPERATOR', '+') or self.match('OPERATOR', '-'):
            self.advance()
            self.multiplicative_expression()

    def multiplicative_expression(self):
        """
        Analyse une expression multiplicative ('*', '/', '%').
        """
        self.unary_expression()
        while self.match('OPERATOR', '*') or self.match('OPERATOR', '/') or self.match('OPERATOR', '%'):
            self.advance()
            self.unary_expression()

    def unary_expression(self):
        """
        Analyse une expression unaire ('+', '-', '!').
        """
        if self.match('OPERATOR', '+') or self.match('OPERATOR', '-') or self.match('OPERATOR', '!'):
            self.advance()
        self.primary_expression()

    def primary_expression(self):
        """
        Analyse une expression primaire (nombre, chaîne, identifiant, ou expression entre parenthèses).
        """
        if self.match('NUMBER') or self.match('STRING') or self.match('BOOLEAN'):
            self.advance()
        elif self.match('KEYWORD', 'true') or self.match('KEYWORD', 'false') or self.match('KEYWORD', 'cursor'):
            self.advance()
            if self.match('DELIMITER', '('):
                self.function_call_expression()
        elif self.match('IDENTIFIER'):
            self.advance()
            if self.match('DELIMITER', '('):
                self.function_call_expression()
        elif self.match('DELIMITER', '('):
            self.advance()
            self.expression()
            if not self.consume('DELIMITER', ')'):
                self.record_error('DELIMITER')
        else:
            self.record_error("NUMBER, STRING, BOOLEAN, IDENTIFIER or '('")

    def function_call_expression(self):
        """
        Analyse un appel de fonction dans une expression.
        """
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ')'):
            self.argument_list()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')

    def cursor_method_call_statement(self):
        """
        Analyse un appel à une méthode du curseur.
        """
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('OPERATOR', '.'):
            self.record_error('.')
            return
        self.cursor_method_call()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def cursor_method_call(self):
        """
        Analyse les différentes méthodes disponibles pour un curseur.
        """
        if self.match('IDENTIFIER', 'moveTo'):
            self.advance()
            self.consume('DELIMITER', '(')
            self.expression()
            self.consume('DELIMITER', ',')
            self.expression()
            self.consume('DELIMITER', ')')
        elif self.match('IDENTIFIER', 'rotate'):
            self.advance()
            self.consume('DELIMITER', '(')
            self.expression()
            self.consume('DELIMITER', ')')
        elif self.match('IDENTIFIER', 'drawLine'):
            self.advance()
            self.consume('DELIMITER', '(')
            self.expression()
            self.consume('DELIMITER', ',')
            self.expression()
            self.consume('DELIMITER', ')')
        elif self.match('IDENTIFIER', 'drawCircle'):
            self.advance()
            self.consume('DELIMITER', '(')
            self.expression()
            self.consume('DELIMITER', ')')
        elif self.match('IDENTIFIER', 'drawRectangle'):
            self.advance()
            self.consume('DELIMITER', '(')
            self.expression()
            self.consume('DELIMITER', ',')
            self.expression()
            self.consume('DELIMITER', ')')
        else:
            self.record_error('Cursor method')

    # Fonctions utilitaires

    def match(self, token_type, value=None):
        """
        Vérifie si le jeton courant correspond au type et à la valeur donnés.
        """
        if self.current >= len(self.tokens):
            return False
        token = self.tokens[self.current]
        if token['type'] != token_type:
            return False
        if value is not None and token['value'] != value:
            return False
        return True

    def consume(self, token_type, value=None):
        """
        Consomme le jeton courant s'il correspond au type et à la valeur donnés.
        """
        if self.match(token_type, value):
            self.advance()
            return True
        else:
            return False

    def advance(self):
        """
        Avance le pointeur 'current' pour passer au jeton suivant.
        """
        self.current += 1

    def record_error(self, expected):
        """
        Enregistre une erreur syntaxique avec les informations du jeton courant.
        """
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            error_info = {
                'TOKEN_INCORRECT': token['value'],
                'TYPE_DU_TOKEN_INCORRECT': token['type'],
                'SUGGESTION_TOKEN_CORRECT': expected,
                'line': token['line']
            }
            self.errors.append(error_info)
            self.advance()
        else:
            # S'il n'y a plus de jetons, on ajoute une erreur à la fin
            error_info = {
                'TOKEN_INCORRECT': 'EOF',
                'TYPE_DU_TOKEN_INCORRECT': 'EOF',
                'SUGGESTION_TOKEN_CORRECT': expected,
                'line': self.tokens[-1]['line'] if self.tokens else 0
            }
            self.errors.append(error_info)
            # Ajouter un token EOF pour éviter les erreurs d'index
            self.tokens.append({'type': 'EOF', 'value': '', 'line': self.tokens[-1]['line'] if self.tokens else 0})




'''
----------------------------------------------------------------------------------------------------------------------
TEST DU PARSER AVEC UN CODE "REEL"
----------------------------------------------------------------------------------------------------------------------
''' 
#tokens corrects : 
'''
correct_tokens = [
    {'type': 'KEYWORD', 'value': 'var', 'line': 3},
    {'type': 'IDENTIFIER', 'value': 'centerX', 'line': 3},
    {'type': 'OPERATOR', 'value': '=', 'line': 3},
    {'type': 'NUMBER', 'value': 300.0, 'line': 3},
    {'type': 'DELIMITER', 'value': ';', 'line': 3},
    {'type': 'KEYWORD', 'value': 'var', 'line': 4},
    {'type': 'IDENTIFIER', 'value': 'centerY', 'line': 4},
    {'type': 'OPERATOR', 'value': '=', 'line': 4},
    {'type': 'NUMBER', 'value': 300.0, 'line': 4},
    {'type': 'DELIMITER', 'value': ';', 'line': 4},
    {'type': 'KEYWORD', 'value': 'var', 'line': 5},
    {'type': 'IDENTIFIER', 'value': 'radius', 'line': 5},
    {'type': 'OPERATOR', 'value': '=', 'line': 5},
    {'type': 'NUMBER', 'value': 50.0, 'line': 5},
    {'type': 'DELIMITER', 'value': ';', 'line': 5},
    {'type': 'KEYWORD', 'value': 'var', 'line': 6},
    {'type': 'IDENTIFIER', 'value': 'numCircles', 'line': 6},
    {'type': 'OPERATOR', 'value': '=', 'line': 6},
    {'type': 'NUMBER', 'value': 5.0, 'line': 6},
    {'type': 'DELIMITER', 'value': ';', 'line': 6},
    {'type': 'KEYWORD', 'value': 'var', 'line': 7},
    {'type': 'IDENTIFIER', 'value': 'angle', 'line': 7},
    {'type': 'OPERATOR', 'value': '=', 'line': 7},
    {'type': 'NUMBER', 'value': 0.0, 'line': 7},
    {'type': 'DELIMITER', 'value': ';', 'line': 7},
    {'type': 'KEYWORD', 'value': 'var', 'line': 8},
    {'type': 'IDENTIFIER', 'value': 'speed', 'line': 8},
    {'type': 'OPERATOR', 'value': '=', 'line': 8},
    {'type': 'NUMBER', 'value': 0.05, 'line': 8},
    {'type': 'DELIMITER', 'value': ';', 'line': 8},
    {'type': 'KEYWORD', 'value': 'var', 'line': 9},
    {'type': 'IDENTIFIER', 'value': 'isAnimating', 'line': 9},
    {'type': 'OPERATOR', 'value': '=', 'line': 9},
    {'type': 'KEYWORD', 'value': 'true', 'line': 9},
    {'type': 'DELIMITER', 'value': ';', 'line': 9},
    # Déclaration du curseur (ligne 12)
    {'type': 'KEYWORD', 'value': 'var', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'myCursor', 'line': 12},
    {'type': 'DELIMITER', 'value': ':', 'line': 12},
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 12},
    {'type': 'OPERATOR', 'value': '=', 'line': 12},
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 12},
    {'type': 'DELIMITER', 'value': '(', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'centerX', 'line': 12},
    {'type': 'DELIMITER', 'value': ',', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'centerY', 'line': 12},
    {'type': 'DELIMITER', 'value': ')', 'line': 12},
    {'type': 'DELIMITER', 'value': ';', 'line': 12},
    # Définition de la fonction 'drawCircle' (ligne 15)
    {'type': 'KEYWORD', 'value': 'function', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'drawCircle', 'line': 15},
    {'type': 'DELIMITER', 'value': '(', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 15},
    {'type': 'DELIMITER', 'value': ',', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'y', 'line': 15},
    {'type': 'DELIMITER', 'value': ',', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'r', 'line': 15},
    {'type': 'DELIMITER', 'value': ')', 'line': 15},
    {'type': 'DELIMITER', 'value': '{', 'line': 15},
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

    # Pour tester le code avec des erreurs
    parser = DrawScriptParser(incorrect_tokens)
    parsed_incorrect_tokens, incorrect_errors = parser.parse()

    # Afficher les erreurs du code incorrect
    print("Erreurs dans le code incorrect:")
    for error in incorrect_errors:
        print(error)

'''
