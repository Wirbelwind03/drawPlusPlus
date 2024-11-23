class DrawScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  # Index du jeton courant
        self.errors = [0] * len(tokens)  # 0 si pas d'erreur, sinon nom du type attendu

    def parse(self):
        try:
            while self.current < len(self.tokens):
                self.statement()
                print(self.current)
        except Exception as e:
            pass  # Ignorer les exceptions pour continuer l'analyse
        return self.tokens, self.errors

    def statement(self):
        if self.match('KEYWORD', 'var'):
            self.variable_declaration()
        elif self.match('IDENTIFIER'):
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
        elif self.match('COMMENT'):
            self.advance()
        else:
            self.record_error("Unexpected token in statement")

    def variable_declaration(self):
        # 'var' IDENTIFIER [ '=' expression ] ';'
        self.consume('KEYWORD', 'var')
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if self.match('OPERATOR', '='):
            self.advance()
            self.expression()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def assignment_or_function_call(self):
        # IDENTIFIER '=' expression ';' | IDENTIFIER '(' [ argument_list ] ')' ';'
        self.consume('IDENTIFIER')
        if self.match('OPERATOR', '='):
            self.advance()
            self.expression()
            if not self.consume('DELIMITER', ';'):
                self.record_error('DELIMITER')
        elif self.match('DELIMITER', '('):
            self.function_call()
        else:
            self.record_error('OPERATOR or DELIMITER')

    def function_definition(self):
        # 'function' IDENTIFIER '(' [ parameter_list ] ')' '{' { statement } '}'
        self.consume('KEYWORD', 'function')
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ')'):
            self.parameter_list()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def function_call(self):
        # IDENTIFIER '(' [ argument_list ] ')' ';'
        self.consume('DELIMITER', '(')
        if not self.match('DELIMITER', ')'):
            self.argument_list()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def if_statement(self):
        # 'if' '(' expression ')' '{' { statement } '}' [ 'else' '{' { statement } '}' ]
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
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')
            return
        if self.match('KEYWORD', 'else'):
            self.advance()
            if not self.consume('DELIMITER', '{'):
                self.record_error('DELIMITER')
                return
            while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
                self.statement()
            if not self.consume('DELIMITER', '}'):
                self.record_error('DELIMITER')

    def while_loop(self):
        # 'while' '(' expression ')' '{' { statement } '}'
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
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def for_loop(self):
        # 'for' '(' [ initialization ] ';' expression ';' [ iteration ] ')' '{' { statement } '}'
        self.consume('KEYWORD', 'for')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ';'):
            self.initialization()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')
            return
        self.expression()
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')
            return
        if not self.match('DELIMITER', ')'):
            self.iteration()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def copy_paste_statement(self):
        # 'copy' '(' coordinate_pair ',' coordinate_pair ')' 'to' '(' coordinate_pair ')' ';'
        self.consume('KEYWORD', 'copy')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
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
        self.coordinate_pair()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def animation_block(self):
        # 'animate' '(' IDENTIFIER ',' duration ')' '{' { statement } '}'
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
        self.expression()  # Duration
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', '{'):
            self.record_error('DELIMITER')
            return
        while not self.match('DELIMITER', '}') and self.current < len(self.tokens):
            self.statement()
        if not self.consume('DELIMITER', '}'):
            self.record_error('DELIMITER')

    def cursor_statement(self):
        # 'cursor' '(' coordinate_pair ')' ';'
        self.consume('KEYWORD', 'cursor')
        if not self.consume('DELIMITER', '('):
            self.record_error('DELIMITER')
            return
        self.coordinate_pair()
        if not self.consume('DELIMITER', ')'):
            self.record_error('DELIMITER')
            return
        if not self.consume('DELIMITER', ';'):
            self.record_error('DELIMITER')

    def coordinate_pair(self):
        self.expression()
        if not self.consume('DELIMITER', ','):
            self.record_error('DELIMITER')
            return
        self.expression()

    def initialization(self):
        if self.match('KEYWORD', 'var'):
            self.variable_declaration()
        else:
            self.assignment()

    def iteration(self):
        self.assignment()

    def assignment(self):
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        if not self.consume('OPERATOR', '='):
            self.record_error('OPERATOR')
            return
        self.expression()

    def parameter_list(self):
        if not self.consume('IDENTIFIER'):
            self.record_error('IDENTIFIER')
            return
        while self.match('DELIMITER', ','):
            self.advance()
            if not self.consume('IDENTIFIER'):
                self.record_error('IDENTIFIER')
                return

    def argument_list(self):
        self.expression()
        while self.match('DELIMITER', ','):
            self.advance()
            self.expression()

    def expression(self):
        # Simplification pour l'expression
        self.logical_or_expression()

    def logical_or_expression(self):
        self.logical_and_expression()
        while self.match('OPERATOR', '||'):
            self.advance()
            self.logical_and_expression()

    def logical_and_expression(self):
        self.equality_expression()
        while self.match('OPERATOR', '&&'):
            self.advance()
            self.equality_expression()

    def equality_expression(self):
        self.relational_expression()
        while self.match('OPERATOR', '==' ) or self.match('OPERATOR', '!='):
            self.advance()
            self.relational_expression()

    def relational_expression(self):
        self.additive_expression()
        while self.match('OPERATOR', '<') or self.match('OPERATOR', '>') or \
              self.match('OPERATOR', '<=') or self.match('OPERATOR', '>='):
            self.advance()
            self.additive_expression()

    def additive_expression(self):
        self.multiplicative_expression()
        while self.match('OPERATOR', '+') or self.match('OPERATOR', '-'):
            self.advance()
            self.multiplicative_expression()

    def multiplicative_expression(self):
        self.unary_expression()
        while self.match('OPERATOR', '*') or self.match('OPERATOR', '/') or self.match('OPERATOR', '%'):
            self.advance()
            self.unary_expression()

    def unary_expression(self):
        if self.match('OPERATOR', '+') or self.match('OPERATOR', '-') or self.match('OPERATOR', '!'):
            self.advance()
        self.primary_expression()

    def primary_expression(self):
        if self.match('NUMBER') or self.match('STRING') or self.match('IDENTIFIER'):
            self.advance()
        elif self.match('DELIMITER', '('):
            self.advance()
            self.expression()
            if not self.consume('DELIMITER', ')'):
                self.record_error('DELIMITER')
        else:
            self.record_error('NUMBER, STRING, IDENTIFIER or \'(\'')

    # Fonctions utilitaires

    def match(self, token_type, value=None):
        if self.current >= len(self.tokens):
            return False
        token = self.tokens[self.current]
        if token['type'] != token_type:
            return False
        if value is not None and token['value'] != value:
            return False
        return True

    def consume(self, token_type, value=None):
        if self.match(token_type, value):
            self.advance()
            return True
        else:
            return False

    def advance(self):
        self.current += 1

    def record_error(self, expected):
        if self.current < len(self.tokens):
            self.errors[self.current] = expected
            self.advance()
        else:
            # S'il n'y a plus de jetons, on ajoute une erreur à la fin
            self.errors.append(expected)
            self.tokens.append({'type': 'EOF', 'value': '', 'line': self.tokens[-1]['line'] if self.tokens else 0})
