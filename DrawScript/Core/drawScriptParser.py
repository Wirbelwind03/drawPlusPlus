from config import DEBUG
from DrawScript.Exceptions.parserError import ParserError

class DrawScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []
        self.context_stack = []


    @property
    def currentToken(self):
        if (self.tokens == []):
            return None
        return self.tokens[self.current_token_index]

    def parse(self):
        """
        Main method of the parser that iterates through all tokens
        and parses 'statement' to the end.
        Returns a flat list of nodes (or None on fatal error).
        """
        ast_nodes = []
        max_iterations = len(self.tokens) + 1000  # Ajouter une limite
        iterations = 0
        while not self.is_at_end():
            # On a un "garde fou" sur le nombre d'itérations
            if iterations > max_iterations:
                if self.context_stack:
                    last_ctx = self.context_stack[-1]
                    msg = (
                        f"La structure '{last_ctx['type']}' commencée à la ligne {last_ctx['line']} "
                        f"n'est pas correctement fermée (accolade manquante ?)."
                    )
                    # On enregistre l’erreur dans self.errors
                    self.errors.append({
                        "message": msg,
                        "line": last_ctx['line']
                    })
                    # Puis on quitte la boucle parse
                    break
                else:
                    # Même chose, on ajoute un message plus générique
                    self.errors.append({
                        "message": "Boucle infinie détectée ou code invalide",
                        "line": -1
                    })
                    break            
            iterations += 1

            stmt = self.parse_statement()
            if DEBUG:
                print(stmt)
            if stmt is not None:
                ast_nodes.append(stmt)
        return ast_nodes, self.errors


    # ----------------- Utilitary Methods -------------------
    def advance(self): #simply increments the current_token_index to move to the next token
        if not self.is_at_end():
            self.current_token_index += 1


    def current_token(self): #returns the current token without using the currentToken property
        if self.is_at_end():
            return None
        return self.tokens[self.current_token_index]

    def previous_token(self): #returns the token located just before the current index, or None if we are already at the very beginning
        if self.current_token_index == 0:
            return None
        return self.tokens[self.current_token_index - 1]

    def is_at_end(self): #indicates whether the current index has exceeded or reached the end of the token list
        return self.current_token_index >= len(self.tokens)

    def match(self, expected_type, expected_value=None): #checks that the current token matches a given type (and possibly a value), without consuming this token
        if self.is_at_end():
            return False
        token = self.current_token()
        if token["type"] != expected_type:
            return False
        if expected_value is not None and token["value"] != expected_value:
            return False
        return True


    def consume(self, expected_type, expected_value=None): #checks that the current token matches an expected type (and/or value), then “consumes” it by advancing the index
        """
        Consumes the current token if it matches (type, value).
        Otherwise, raises a ParserError.
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

    def synchronize(self): #is used to "resynchronize" the parser in case of error, by advancing through the tokens until a reliable delimiter is encountered (often ; or }).
        while not self.is_at_end():
            prev = self.previous_token()
            if prev and prev["value"] == ";":
                return
            curr = self.current_token()
            if curr["type"] == "DELIMITER" and curr["value"] in ("}",):
                return
            self.advance()

    def pushContext(self, ctx_type, line): #stacks a new context (eg for, if, block, etc) with the corresponding line
        self.context_stack.append({"type": ctx_type, "line": line})

    def popContext(self): #Inverse of pushContext, it removes the last context added to the stack
        """
        Pops the last context.
        To be called when the corresponding structure is finished.
        """
        if self.context_stack:
            self.context_stack.pop()


    # ----------------- Parsing statements -------------------
    def parse_statement(self): #attempts to parse a statement from the current token (variable, if, for, etc.).
        start_line = self.current_token()['line'] if not self.is_at_end() else -1
        start_index = self.current_token_index  # <-- We memorize the starting index

        try:
            return self._parse_statement_internal()
        except ParserError as e:
            # The error is recorded
            self.errors.append({
                "message": str(e),
                "line": start_line
            })
            # We call synchronization
            self.synchronize()

            # If we have not advanced at all, we advance one token
            # to avoid repeating the same mistake over and over again
            if self.current_token_index == start_index and not self.is_at_end():
                self.advance()

            return None


    def _parse_statement_internal(self): #internal part of the statement parser, where the logic is to identify each type of statement and form the nodes
        
        if self.match('KEYWORD', 'var'):
            return self.parse_var_declaration()

        if self.match('KEYWORD', 'Cursor'):
            return self.parse_cursor_declaration()

        if self.match('KEYWORD', 'if'):
            return self.parse_if_statement()

        if self.match('KEYWORD', 'for'):
            return self.parse_for_statement()

        if self.match('KEYWORD', 'while'):
            return self.parse_while_statement()

        if self.match('KEYWORD', 'do'):
            return self.parse_do_while_statement()

        if self.match('KEYWORD', 'function'):
            return self.parse_function_declaration()

        if self.match('KEYWORD', 'return'):
            return self.parse_return_statement()

        if self.match('KEYWORD', 'copy'):
            return self.parse_copy_statement()

        if self.match('KEYWORD', 'animate'):
            return self.parse_animate_statement()

        if self.match('DELIMITER', ';'):
            return self.parse_empty_statement()

        if self.looks_like_cursor_method():
            return self.parse_cursor_method_statement()

        # Otherwise => expression statement
        return self.parse_expression_statement()



# ------------------------------------------ different statements (more utility like loops etc) -----------------------------------

    def parse_var_declaration(self): #handles the syntax of a variable declaration, for example var x = 10;
        '''
        var IDENTIFIER [":" IDENTIFIER] "=" EXPRESSION ";" 
        '''
        line_num = self.current_token()["line"]
        if not self.match('KEYWORD', 'var'):
            raise ParserError("Déclaration de variable invalide : mot-clé 'var' attendu avant ton identificateur.")
        self.consume('KEYWORD', 'var')
        if not self.match('IDENTIFIER'):
            raise ParserError("Déclaration de variable invalide : identifiant attendu après 'var'.")
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        var_type = None

        if self.match('DELIMITER', ':'):
            self.consume('DELIMITER', ':')
            # An identifier is expected for the type
            # (and you can require it to be "cursor", or not)
            type_token = self.consume('IDENTIFIER')
            var_type = type_token['value']  # ex. "cursor"

        # Expecting an '=' (ASSIGN token)
        if not self.match('ASSIGN', '='):
            raise ParserError(f"Déclaration invalide pour '{var_name}' : signe '=' attendu.")
        self.consume('ASSIGN', '=')

        #Parse the expression following the '='
        expr = self.parse_expression()
        # Assign variable typing
        if expr["node_type"] == "number":
            # See if it is a float or an int
            var_type = "int" if isinstance(expr["value"], int) else "float" 
        elif expr["node_type"] == "bool_literal":
            var_type = "bool"

        #A trailing semicolon is expected
        if not self.match('DELIMITER', ';'):
            raise ParserError(f"Point-virgule manquant après la déclaration de '{var_name}'.")
        self.consume('DELIMITER', ';')

        return {
            "node_type": "var_declaration",
            "name": var_name,
            "type": var_type,
            "expression": expr,
            "line": line_num  
        }


    def parse_if_statement(self): #  parse a structure if(...) { ... } [else { ... }].
        line_num = self.current_token()["line"]
        
        self.pushContext("if", line_num)

        self.consume('KEYWORD', 'if')
        self.consume('DELIMITER', '(')
        condition = self.parse_expression()
        self.consume('DELIMITER', ')')
        then_block = self.parse_block()

        else_block = None
        if self.match('KEYWORD', 'else'):
            self.consume('KEYWORD', 'else')
            else_block = self.parse_block()

        # end of if 
        self.popContext()

        return {
            "node_type": "if_statement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block,
            "line": line_num
        }



    def parse_for_statement(self): #analyzes the structure of a for(...) { ... } loop that includes an initialization, a condition, and an increment.
        line_num = self.current_token()["line"]
        
        # Stack "for"
        self.pushContext("for", line_num)

        self.consume('KEYWORD', 'for')
        self.consume('DELIMITER', '(')
        init_node = self.parse_for_init()
        self.consume('DELIMITER', ';')
        condition_node = self.parse_expression()
        self.consume('DELIMITER', ';')
        increment_node = self.parse_expression()
        self.consume('DELIMITER', ')')

        body_node = self.parse_block()

        # We arrive here => we have successfully parsed the 'for' + block => we unstack
        self.popContext()

        return {
            "node_type": "for_statement",
            "init": init_node,
            "condition": condition_node,
            "increment": increment_node,
            "body": body_node,
            "line": line_num
        }


    def parse_while_statement(self): #parse a while(...) { ... } loop, checking for parentheses, a condition, and a block
        line_num = self.current_token()["line"]
        
        self.pushContext("while", line_num)

        self.consume('KEYWORD', 'while')
        self.consume('DELIMITER', '(')
        condition_node = self.parse_expression()
        self.consume('DELIMITER', ')')
        body_node = self.parse_block()

        self.popContext()

        return {
            "node_type": "while_statement",
            "condition": condition_node,
            "body": body_node,
            "line": line_num
        }


    def parse_do_while_statement(self): # handles the do { ... } while(...); loop whose syntax requires the block to precede the condition.
        line_num = self.current_token()["line"]
        
        self.pushContext("do-while", line_num)

        self.consume('KEYWORD', 'do')
        body_node = self.parse_block()
        self.consume('KEYWORD', 'while')
        self.consume('DELIMITER', '(')
        condition_node = self.parse_expression()
        self.consume('DELIMITER', ')')
        self.consume('DELIMITER', ';')

        self.popContext()

        return {
            "node_type": "do_while_statement",
            "condition": condition_node,
            "body": body_node,
            "line": line_num
        }


    def parse_function_declaration(self): # parse a function declaration of type function name(...) { ... }.

        line_num = self.current_token()["line"]
        self.pushContext("function", line_num)

        self.consume('KEYWORD', 'function')
        func_name = self.consume('IDENTIFIER')
        self.consume('DELIMITER', '(')
        # etc.
        self.consume('DELIMITER', ')')
        func_body = self.parse_block()

        self.popContext()

        return {
            "node_type": "function_declaration",
            "name": func_name["value"],
            "params": ...,
            "body": func_body,
            "line": line_num
        }




        
        

    def parse_block(self): # expects an opening brace {, then parses multiple statements until the closing brace }.
        line_num = self.current_token()["line"]
        
        self.pushContext("block", line_num)
        self.consume('DELIMITER', '{')
        statements = []
        while not self.is_at_end() and not self.match('DELIMITER', '}'):
            stmt = self.parse_statement()
            if DEBUG:
                print(stmt)
            if stmt:
                statements.append(stmt)
        self.consume('DELIMITER', '}')
        # We found the '}', we can unstack the context
        self.popContext()
        return {
            "node_type": "block",
            "statements": statements,
            "line": line_num
        }


    def parse_expression_statement(self): # parses a simple expression followed by a semicolon, which forms a statement like x + 3;.
        line_num = -1
        if not self.is_at_end():
            line_num = self.current_token()["line"]

        expr = self.parse_expression()
        self.consume('DELIMITER', ';')
        return {
            "node_type": "expression_statement",
            "expression": expr,
            "line": line_num
        }



    def parse_empty_statement(self): #handles the case of an isolated semicolon ;, which represents an empty statement.
        """
        parse_empty_statement ::= ";"
        """
        # Consume a semi-colon
        self.consume('DELIMITER', ';')
        # An empty node is returned (or a dict indicating an empty statement)
        return {
            "node_type": "empty_statement"
        }



# ----------------------------------- Expressions and hierarchy of expressions ---------------------------- #




#A general expression 
    def parse_expression(self): # invokes parse_simple_assignment_expr to parse expressions.
        """
        parse_expression ::= parse_assignment_expr()
        """
        return self.parse_simple_assignment_expr() #

# Assignment expression 
    def parse_simple_assignment_expr(self): #first handles a logical expression (logical_or_expr).
        """
        assignment_expr ::= logical_or_expr
                        | IDENTIFIER '=' assignment_expr
        (or more formal: left = right)

        We base ourselves on a schema:
            - We first parse a left = parse_logical_or_expr()
            - If we see an '=', we consume and parse the rest as assignment_expr()
            - Otherwise we return left
        """
        left = self.parse_logical_or_expr()

        # Regarde si c'est un =
        if self.match('ASSIGN', '='):
            self.consume('ASSIGN', '=')
            right = self.parse_simple_assignment_expr() #takes into account all the expressions x = y + 1, or even x = y = z + 2
            return {
                "node_type": "binary_op",
                "op": "=",
                "left": left,
                "right": right
            }

        return left


# logical expression "OR" ||
    def parse_logical_or_expr(self): #analyzes the structure of an operation of type expr || expr.
        """
        logical_or_expr ::= logical_and_expr
                        | logical_or_expr "||" logical_and_expr
        """
        left = self.parse_logical_and_expr()

        # As long as we find the operator "||" (type='OPERATOR', value='||'), we continue
        while self.match('OPERATOR', '||'):
            op_token = self.consume('OPERATOR', '||')
            right = self.parse_logical_and_expr()
            left = {
                "node_type": "binary_op",
                "op": "||",
                "left": left,
                "right": right
            }

        return left

#logical expression "AND" &&
    def parse_logical_and_expr(self): # is very similar to parse_logical_or_expr but for && operations.
        """
        logical_and_expr ::= equality_expr
                        | logical_and_expr "&&" equality_expr
        """
        left = self.parse_equality_expr()

        while self.match('OPERATOR', '&&'):
            op_token = self.consume('OPERATOR', '&&')
            right = self.parse_equality_expr()
            left = {
                "node_type": "binary_op",
                "op": "&&",
                "left": left,
                "right": right
            }

        return left

# logical expression equal or NOT equal "==" "!="    
    def parse_equality_expr(self): #checks for the presence of equality operators == or != between relational expressions.
        """
        equality_expr ::= relational_expr
                        | equality_expr ("==" | "!=") relational_expr
        """
        left = self.parse_relational_expr()

        while not self.is_at_end():
            # We test if we have "==" or "!="
            if self.match('OPERATOR', '=='):
                self.consume('OPERATOR', '==')
                right = self.parse_relational_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "==",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '!='):
                self.consume('OPERATOR', '!=')
                right = self.parse_relational_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "!=",
                    "left": left,
                    "right": right
                }
            else:
                break  # we get out of the loop

        return left

# logical comparison expression
    def parse_relational_expr(self): # handles comparison operators <, <=, >, >= between additive expressions.
        """
        relational_expr ::= additive_expr
                        | relational_expr ("<" | "<=" | ">" | ">=") additive_expr
        """
        left = self.parse_additive_expr()

        while not self.is_at_end():
            if self.match('OPERATOR', '<'):
                self.consume('OPERATOR', '<')
                right = self.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "<",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '<='):
                self.consume('OPERATOR', '<=')
                right = self.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "<=",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '>'):
                self.consume('OPERATOR', '>')
                right = self.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": ">",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '>='):
                self.consume('OPERATOR', '>=')
                right = self.parse_additive_expr()
                left = {
                    "node_type": "binary_op",
                    "op": ">=",
                    "left": left,
                    "right": right
                }
            else:
                break

        return left

# logical expression of addition or subtraction
    def parse_additive_expr(self): # handles addition and subtraction, so the + and - operators. After calling parse_multiplicative_expr, it continues as long as it sees + or -
        """
        additive_expr ::= multiplicative_expr
                        | additive_expr ("+" | "-") multiplicative_expr
        """
        left = self.parse_multiplicative_expr()

        while not self.is_at_end():
            if self.match('OPERATOR', '+'):
                self.consume('OPERATOR', '+')
                right = self.parse_multiplicative_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "+",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '-'):
                self.consume('OPERATOR', '-')
                right = self.parse_multiplicative_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "-",
                    "left": left,
                    "right": right
                }
            else:
                break

        return left

# logical multiplication expression
    def parse_multiplicative_expr(self): #parses multiplications, divisions and modulos (*, /, %).
        """
        multiplicative_expr ::= unary_expr
                            | multiplicative_expr ("*" | "/" | "%") unary_expr
        """
        left = self.parse_unary_expr()

        while not self.is_at_end():
            if self.match('OPERATOR', '*'):
                self.consume('OPERATOR', '*')
                right = self.parse_unary_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "*",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '/'):
                self.consume('OPERATOR', '/')
                right = self.parse_unary_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "/",
                    "left": left,
                    "right": right
                }
            elif self.match('OPERATOR', '%'):
                self.consume('OPERATOR', '%')
                right = self.parse_unary_expr()
                left = {
                    "node_type": "binary_op",
                    "op": "%",
                    "left": left,
                    "right": right
                }
            else:
                break

        return left

#
    def parse_unary_expr(self): # detects unary operators !, + and - placed before an expression as a priority.
# If a unary operator is found, it consumes that token, then recursively parses the rest.

        """
        unary_expr ::= ("!" | "+" | "-") unary_expr
                    | primary_expr
        """
        if not self.is_at_end():
            # Ex: !someVar
            if self.match('OPERATOR', '!'):
                self.consume('OPERATOR', '!')
                expr = self.parse_unary_expr()
                return {
                    "node_type": "unary_op",
                    "op": "!",
                    "expr": expr
                }
            elif self.match('OPERATOR', '+'):
                self.consume('OPERATOR', '+')
                expr = self.parse_unary_expr()
                return {
                    "node_type": "unary_op",
                    "op": "+",
                    "expr": expr
                }
            elif self.match('OPERATOR', '-'):
                self.consume('OPERATOR', '-')
                expr = self.parse_unary_expr()
                return {
                    "node_type": "unary_op",
                    "op": "-",
                    "expr": expr
                }

        # Otherwise, we come across the parse_primary_expr function
        return self.parse_primary_expr()

#
    def parse_primary_expr(self):# handles literals (number, boolean, string) as well as identifiers and parenthesized expressions.
#If the expression is an identifier followed by (, it assumes it is a function call and then parses the arguments.
        """
        primary_expr ::= NUMBER
                    | STRING
                    | BOOLEAN
                    | IDENTIFIER [ ( DELIMITER("(") argument_list DELIMITER(")") )? ]
                    | "(" expression ")"
        """
        # 1) Parentheses
        if self.match('DELIMITER', '('):
            self.consume('DELIMITER', '(')
            expr = self.parse_expression()
            self.consume('DELIMITER', ')')
            return expr

        # 2) NUMBER
        if self.match('NUMBER'):
            token = self.consume('NUMBER')
            return {
                "node_type": "number",
                "value": token["value"]
            }

        # 3) BOOLEAN ("BOOLEAN" => true/false)
        #    or KEYWORD("true"/"false"), 
        if self.match('BOOLEAN', 'true'):
            self.consume('BOOLEAN', 'true')
            return {"node_type": "bool_literal", "value": "true"}
        if self.match('BOOLEAN', 'false'):
            self.consume('BOOLEAN', 'false')
            return {"node_type": "bool_literal", "value": "false"}

        # 4) STRING
        if self.match('STRING'):
            token = self.consume('STRING')
            return {
                "node_type": "string",
                "value": token["value"]
            }

        # 5) IDENTIFIER (variable or potential function call)
        if self.match('IDENTIFIER'):
            id_token = self.consume('IDENTIFIER')
            node = {
                "node_type": "identifier",
                "value": id_token["value"]
            }

            # Optional: if we see "(", then it is a function call
            # ex: drawCircle(...)
            if self.match('DELIMITER', '('):
                self.consume('DELIMITER', '(')
                args = []
                if not self.match('DELIMITER', ')'):
                    args = self.parse_argument_list()
                self.consume('DELIMITER', ')')
                # We build a call node
                node = {
                    "node_type": "call_expr",
                    "callee": id_token["value"],
                    "arguments": args
                }

            return node

        # Otherwise, error
        raise ParserError("Expression primaire invalide.")


#-------------------------        Arguments of the for, if etc functions.   --------------------------------------------------------

    #Initialization
    def parse_for_init(self): # parses the "init" part of a for loop, which can be a var declaration, an assignment, or nothing at all.
        """
        for_init ::= var_declaration_no_semi
                | assignment_expr
                | (empty)
        """
        # If we have a 'var', we parse a declaration *without consuming the ';'
        if self.match('KEYWORD', 'var'):
            return self.parse_var_declaration_no_semi()

        # Otherwise, if we have an IDENTIFIER -> potentially an assignment
        # as i = 0
        if self.match('IDENTIFIER'):
            return self.parse_simple_assignment()

        # Otherwise, it's empty (nothing)
        return None

    #Initialization in case of already existing variable (no declaration of var variable)
    def parse_var_declaration_no_semi(self):#is similar to parse_var_declaration, except that it does not consume the trailing semicolon.
# It is used in the for(...) syntax for initialization, which does not always end with ; in the parenthesis.
        """
        var IDENTIFIER [":" TYPE] "=" EXPRESSION
        (Not to be confused with the 'parse_var_declaration' version which consumes the ';')
        """
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'var')

        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        var_type = None

        # Optional: if you handle typing ex: var x : int
        # if self.match('DELIMITER', ':'):
        #     self.consume('DELIMITER', ':')
        #     type_token = self.consume('IDENTIFIER')
        #     var_type = type_token['value']

        self.consume('ASSIGN', '=')
        expr = self.parse_expression()

        return {
            "node_type": "var_declaration_no_semi",
            "name": var_name,
            "type": var_type,
            "expression": expr,
            "line": line_num
        }

    # Increment
    def parse_assignment_expr(self): #handles the identifier = expression form without worrying about other assignment operators like += or -=.
        """
        assignment_expr ::= IDENTIFIER '=' expression
        (in some languages, we also manage +=, -=, etc.
        but here we limit ourselves to '=')
        """
        # An identifier is expected
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        line_num = id_token["line"]
        # Expected '='
        self.consume('ASSIGN', '=')
        # We parse the expression
        expr = self.parse_expression()
        return {
            "node_type": "assignment_expr",
            "target": var_name,
            "value": expr,
            "line": line_num
        }

    # For function creation
    def parse_parameter_list(self): #reads a parameter list consisting of multiple identifiers separated by commas.
        """
        parameter_list ::= IDENTIFIER { ',' IDENTIFIER }
        """
        params = []

    # We first expect an IDENTIFIER
        first_param = self.consume('IDENTIFIER')
        params.append(first_param["value"])


    # As long as we see a comma, we consume the comma and expect an ident
        while self.match('DELIMITER', ','):
            self.consume('DELIMITER', ',')
            param_token = self.consume('IDENTIFIER')
            params.append(param_token["value"])

        return params

    def parse_argument_list(self): #parses a list of arguments, that is, several expressions separated by commas.
        """
        argument_list ::= expression { ',' expression }
        """
        args = []
        first_expr = self.parse_expression()
        args.append(first_expr)

        while self.match('DELIMITER', ','):
            self.consume('DELIMITER', ',')
            expr = self.parse_expression()
            args.append(expr)

        return args

# The return of a function 
    def parse_return_statement(self): #handles the return syntax optionally followed by an expression and a semicolon ;.
        """
        return_statement ::= 'return' [expression] ';'
        """
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'return')

    # Check if we have a direct semicolon or not
        if self.match('DELIMITER', ';'):
            self.consume('DELIMITER', ';')
            return {
                "node_type": "return_statement",
                "expression": None,
                "line": line_num
            }
        else:
            expr = self.parse_expression()
            self.consume('DELIMITER', ';')
            return {
                "node_type": "return_statement",
                "expression": expr,
                "line": line_num
            }



#-------------------------        "Real" drawing functions.   --------------------------------------------------------

    def parse_copy_statement(self): #parse the copy(expr, expr, expr, expr) to (expr, expr); instruction, used to copy something from one point to another.
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'copy')
        self.consume('DELIMITER', '(')
        #Read 4 expressions (separated by commas)
        #    => ARG_LIST_4 = expr, expr, expr, expr
        expr1 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr2 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr3 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr4 = self.parse_expression()

        # consume ')'
        self.consume('DELIMITER', ')')

        # consume keyword 'to'
        self.consume('KEYWORD', 'to')

        # consume '('
        self.consume('DELIMITER', '(')

        # Read 2 expressions (separated by a comma)
        #    => ARG_LIST_2 = expr, expr
        expr5 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr6 = self.parse_expression()

        # consume ')'
        self.consume('DELIMITER', ')')        
        self.consume('DELIMITER', ';')

        return {
            "node_type": "copy_statement",
            "source": [expr1, expr2, expr3, expr4],
            "destination": [expr5, expr6],
            "line": line_num
        }

    def parse_animate_statement(self): # deals with the syntax animate(expr, expr) { ... }, which allows you to animate an object or property.
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'animate')
        self.consume('DELIMITER', '(')
        expr1 = self.parse_expression()
        # Consume the comma
        self.consume('DELIMITER', ',')
        # Second expression (eg 10)
        expr2 = self.parse_expression()
        # Consume ')'
        self.consume('DELIMITER', ')')        
        body_node = self.parse_block()
        return {
            "node_type": "animate_statement",
            "obj_or_expr1": expr1,
            "expr2": expr2,
            "body": body_node,
            "line": line_num
        }

#████████████████████████████████████████████ CURSORS ████████████████████████████████████████████

# Cursor declaration
    def parse_cursor_declaration(self): #  handles the declaration of a cursor via Cursor myCursor = Cursor(...);.
        """
        cursor_declaration ::= 'cursor' IDENTIFIER '=' 'cursor' '(' [ argument_list ] ')' ';'
        """
        line_num = self.current_token()["line"]
        
        # 1) We consume the keyword 'cursor'
        self.consume('KEYWORD', 'Cursor')
        
        # 2) We are waiting for an identifier (eg: myCursor)
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        
        # 3) We are waiting for '='
        self.consume('ASSIGN', '=')
        
        # 4) We are waiting for the keyword 'cursor' to call the "constructor"
        if not self.match('KEYWORD', 'Cursor'):
            raise ParserError("Initialisation de curseur invalide : 'cursor(...)' attendu.")
        self.consume('KEYWORD', 'Cursor')
        
        # 5) We consume '('
        self.consume('DELIMITER', '(')

        # 6) We parse the arguments (optional or not)
        args = []
        if not self.match('DELIMITER', ')'):
            args = self.parse_argument_list()
        
        # 7) We consume ')'
        self.consume('DELIMITER', ')')
        
        # 8) We consume the ';'
        self.consume('DELIMITER', ';')
        
        # 9) We build the AST node
        return {
            "node_type": "cursor_declaration",
            "name": var_name,
            "constructor_args": args,
            "line": line_num
        }

    def looks_like_cursor_method(self): #  inspects the following tokens to determine if there is a pattern of type identifier . identifier (.
        # Check that there are enough tokens
        if self.is_at_end():
            return False
        # We want at least 4 tokens available
        if self.current_token_index + 3 >= len(self.tokens):
            return False
        
        t1 = self.tokens[self.current_token_index]     # IDENTIFIER ?
        t2 = self.tokens[self.current_token_index + 1] # '.' ?
        t3 = self.tokens[self.current_token_index + 2] # IDENTIFIER ?
        t4 = self.tokens[self.current_token_index + 3] # '(' ?

        if t1["type"] == "IDENTIFIER" \
        and t2["type"] == "ACCESS_OPERATOR" and t2["value"] == "." \
        and t3["type"] == "IDENTIFIER" \
        and t4["type"] == "DELIMITER" and t4["value"] == "(":
            return True
        return False

    def parse_cursor_method_statement(self): #handles method calls on a cursor, for example myCursor.moveTo(100, 200);.
        """
        Pattern: IDENTIFIER '.' IDENTIFIER '(' [argument_list] ')' ';'
        """
        line_num = self.current_token()["line"]
        
        # 1) Consume the object (eg: myCursor)
        obj_token = self.consume('IDENTIFIER')
        cursor_name = obj_token['value']

        # 2) Consume the '.'
        self.consume('ACCESS_OPERATOR', '.')

        # 3) Consume the method name (eg: moveTo)
        method_token = self.consume('IDENTIFIER')
        method_name = method_token['value']

        # 4) Consume '('
        self.consume('DELIMITER', '(')

        # 5) Parse the argument_list
        args = []
        if not self.match('DELIMITER', ')'):
            args = self.parse_argument_list()

        # 6) Consume ')'
        self.consume('DELIMITER', ')')

        # 7) Consume the ';'
        self.consume('DELIMITER', ';')

        return {
            "node_type": "cursor_method",
            "cursor_name": cursor_name,
            "method": method_name,
            "arguments": args,
            "line": line_num
        }