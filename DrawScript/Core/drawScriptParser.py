from config import DEBUG
from DrawScript.Exceptions.parserError import ParserError

class DrawScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []

    @property
    def currentToken(self):
        if (self.tokens == []):
            return None
        return self.tokens[self.current_token_index]

    def parse(self):
        """
        Méthode principale du parseur qui parcourt tous les tokens
        et parse 'statement' jusqu'à la fin.
        Retourne une liste de nœuds AST (ou None si erreur fatale).
        """
        ast_nodes = []
        max_iterations = len(self.tokens) + 1000  # Ajouter une limite
        iterations = 0
        while not self.is_at_end():
            if iterations > max_iterations:
                raise RuntimeError("Boucle infinie détectée dans `parse`")
            iterations += 1

            stmt = self.parse_statement()
            if DEBUG:
                print(stmt)
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

        # Sinon => expression statement
        return self.parse_expression_statement()



# ------------------------------------------ différents statements (plus utilitaires de type boucles etc) -----------------------------------

    def parse_var_declaration(self):
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
            # On attend un identifiant pour le type
            # (et tu peux exiger qu’il soit "cursor", ou pas)
            type_token = self.consume('IDENTIFIER')
            var_type = type_token['value']  # ex. "cursor"

        # 4) On s'attend à un '=' (token ASSIGN)
        if not self.match('ASSIGN', '='):
            raise ParserError(f"Déclaration invalide pour '{var_name}' : signe '=' attendu.")
        self.consume('ASSIGN', '=')

        # 5) Parse l'expression qui suit le '='
        expr = self.parse_expression()
        # Assigner le typage de la variable
        if expr["node_type"] == "number":
            # Voir si c'est un float ou un int
            var_type = "int" if isinstance(expr["value"], int) else "float" 
        elif expr["node_type"] == "bool_literal":
            var_type = "bool"

        # 6) On s'attend à un point-virgule final
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


    def parse_if_statement(self):
        """
        if "(" EXPRESSION ")" BLOCK [ "else" BLOCK ]
        """
        # On récupère la ligne du token 'if'
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'if')

        self.consume('DELIMITER', '(')
        condition = self.parse_expression()
        self.consume('DELIMITER', ')')
        then_block = self.parse_block()

        else_block = None
        if self.match('KEYWORD', 'else'):
            self.consume('KEYWORD', 'else')
            else_block = self.parse_block()

        return {
            "node_type": "if_statement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block,
            "line": line_num
        }


    def parse_for_statement(self):
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'for')
        self.consume('DELIMITER', '(')
        init_node = self.parse_for_init()
        self.consume('DELIMITER', ';')
        # parse expression (condition)
        condition_node = self.parse_expression()
        self.consume('DELIMITER', ';')
        # parse l'incrément (on passe par une assignation en premier donc c'est bon)
        increment_node = self.parse_expression()
        self.consume('DELIMITER', ')')
        # parse le block { ... }
        body_node = self.parse_block()
        return {
            "node_type": "for_statement",
            "init": init_node,
            "condition": condition_node,
            "increment": increment_node,
            "body": body_node,
            "line": line_num
        }

    def parse_while_statement(self):
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'while')
        self.consume('DELIMITER', '(')
        condition_node = self.parse_expression()
        self.consume('DELIMITER', ')')
        body_node = self.parse_block()

        return {
            "node_type": "while_statement",
            "condition": condition_node,
            "body": body_node,
            "line": line_num
        }


    def parse_function_declaration(self):
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'function')
        func_name = self.consume('IDENTIFIER')
        self.consume('DELIMITER', '(')
        # parse paramètres (optionnels)
        param_list = []
        if not self.match('DELIMITER', ')'):
            param_list = self.parse_parameter_list()
        self.consume('DELIMITER', ')')
        func_body = self.parse_block()
        return {
            "node_type": "function_declaration",
            "name": func_name["value"],
            "params": param_list,
            "body": func_body,
            "line": line_num
        }



        
        

    def parse_block(self):
        line_num = self.current_token()["line"]
        self.consume('DELIMITER', '{')
        statements = []
        while not self.is_at_end() and not self.match('DELIMITER', '}'):
            stmt = self.parse_statement()
            if DEBUG:
                print(stmt)
            if stmt:
                statements.append(stmt)
        self.consume('DELIMITER', '}')
        return {
            "node_type": "block",
            "statements": statements,
            "line": line_num
        }


    def parse_expression_statement(self):
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



    def parse_empty_statement(self):
        """
        parse_empty_statement ::= ";"
        """
        # On consomme le point-virgule
        self.consume('DELIMITER', ';')
        # On renvoie un nœud vide (ou un dict indiquant un empty statement)
        return {
            "node_type": "empty_statement"
        }



# ----------------------------------- Expressions et hiérarchie des expressions ---------------------------- #




#Une expression générale 
    def parse_expression(self):
        """
        parse_expression ::= parse_assignment_expr()
        """
        return self.parse_simple_assignment_expr() #Modifs Paul car la fonction parse_assignment_expr(self) est trop rigide (à supprimer pour l'instant)

# Expression d'assignation 
    def parse_simple_assignment_expr(self): #Modifs Paul car deux fois le même nom de fonction plus strict
        """
        assignment_expr ::= logical_or_expr
                        | IDENTIFIER '=' assignment_expr
        (ou plus formel: left = right)

        On se base sur un schéma:
            - On parse d'abord un left = parse_logical_or_expr()
            - Si on voit un '=', on consomme et parse la suite comme assignment_expr()
            - Sinon on retourne left
        """
        left = self.parse_logical_or_expr()

        # Regarde si c'est un =
        if self.match('ASSIGN', '='):
            self.consume('ASSIGN', '=')
            right = self.parse_simple_assignment_expr() #Modifs Paul pour prendre en compte bien toute les expressions x = y + 1, ou même x = y = z + 2
            return {
                "node_type": "binary_op",
                "op": "=",
                "left": left,
                "right": right
            }

        return left


# expression logique "OU" ||
    def parse_logical_or_expr(self):
        """
        logical_or_expr ::= logical_and_expr
                        | logical_or_expr "||" logical_and_expr
        """
        left = self.parse_logical_and_expr()

        # Tant qu'on trouve l’opérateur "||" (type='OPERATOR', value='||'), on enchaîne
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

#expression logique "ET" &&
    def parse_logical_and_expr(self):
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

# expression logique égal ou PAS égal "==" "!="
    def parse_equality_expr(self):
        """
        equality_expr ::= relational_expr
                        | equality_expr ("==" | "!=") relational_expr
        """
        left = self.parse_relational_expr()

        while not self.is_at_end():
            # On teste si on a "==" ou "!="
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
                break  # on sort de la boucle

        return left

# expression logique de comparaison 
    def parse_relational_expr(self):
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

# expression logique d'addition ou de soustraction
    def parse_additive_expr(self):
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

# expression logique de multiplication
    def parse_multiplicative_expr(self):
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
    def parse_unary_expr(self):
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

        # Sinon, on tombe sur la fonction parse_primary_expr
        return self.parse_primary_expr()

#
    def parse_primary_expr(self):
        """
        primary_expr ::= NUMBER
                    | STRING
                    | BOOLEAN
                    | IDENTIFIER [ ( DELIMITER("(") argument_list DELIMITER(")") )? ]
                    | "(" expression ")"
        """
        # 1) Parenthèses
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

        # 3) BOOLEAN (si tu as un token "BOOLEAN" => true/false)
        #    ou KEYWORD("true"/"false"), selon ton tokenizer
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

        # 5) IDENTIFIER (variable ou potentiel appel de fonction)
        if self.match('IDENTIFIER'):
            id_token = self.consume('IDENTIFIER')
            node = {
                "node_type": "identifier",
                "value": id_token["value"]
            }

            # Optionnel : si on voit "(", alors c’est un appel de fonction
            # ex: drawCircle(...)
            if self.match('DELIMITER', '('):
                self.consume('DELIMITER', '(')
                args = []
                if not self.match('DELIMITER', ')'):
                    args = self.parse_argument_list()
                self.consume('DELIMITER', ')')
                # On construit un node d’appel
                node = {
                    "node_type": "call_expr",
                    "callee": id_token["value"],
                    "arguments": args
                }

            return node

        # Sinon, erreur
        raise ParserError("Expression primaire invalide.")


#-------------------------        Arguments des fonctions for, if etc..   --------------------------------------------------------

    #Initialisation
    def parse_for_init(self):
        """
        for_init ::= var_declaration_no_semi
                | assignment_expr
                | (vide)
        """
        # Si on a un 'var', on parse une déclaration *sans consommer le ';'*
        if self.match('KEYWORD', 'var'):
            return self.parse_var_declaration_no_semi()

        # Sinon, si on a un IDENTIFIER -> potentiellement un assignment
        # comme i = 0
        if self.match('IDENTIFIER'):
            return self.parse_simple_assignment()

        # Sinon, c’est vide (rien)
        return None

    """def parse_simple_assignment(self): #Mis en commentaire (Paul) car elle ne sert à rien et est trop strict
        # Identifiant
        id_token = self.consume('IDENTIFIER')
        self.consume('ASSIGN', '=')
        expr = self.parse_expression()
        # pas de ;, car c'est un “init”
        return {
        "node_type": "for_assignment",
        "target": id_token["value"],
        "value": expr
        }
    """

    #Initialisation en cas de variable deja existante (pas de declaration de variable var)
    def parse_var_declaration_no_semi(self):
        """
        var IDENTIFIER [":" TYPE] "=" EXPRESSION
        (A ne pas confondre avec la version 'parse_var_declaration' qui consomme le ';')
        """
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'var')

        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        var_type = None

        # Optionnel: si tu gères le typage ex: var x : int
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

    # Incrémentation
    def parse_assignment_expr(self):
        """
        assignment_expr ::= IDENTIFIER '=' expression
        (dans certains langages, on gère aussi +=, -=, etc.
        mais ici on se limite à '=')
        """
        # On s'attend à un identifiant
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        line_num = id_token["line"]
        # On s'attend à '='
        self.consume('ASSIGN', '=')
        # On parse l'expression
        expr = self.parse_expression()
        return {
            "node_type": "assignment_expr",
            "target": var_name,
            "value": expr,
            "line": line_num
        }

    # Pour la creation de fonction 
    def parse_parameter_list(self):
        """
        parameter_list ::= IDENTIFIER { ',' IDENTIFIER }
        """
        params = []

        # On s'attend d'abord à un IDENTIFIER
        first_param = self.consume('IDENTIFIER')
        params.append(first_param["value"])

        # Tant qu'on voit une virgule, on consomme la virgule et on attend un ident
        while self.match('DELIMITER', ','):
            self.consume('DELIMITER', ',')
            param_token = self.consume('IDENTIFIER')
            params.append(param_token["value"])

        return params

    def parse_argument_list(self):
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

# Le return d'une fonction 
    def parse_return_statement(self):
        """
        return_statement ::= 'return' [expression] ';'
        """
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'return')

        # Vérifier si on a un point-virgule direct ou pas
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



#-------------------------        Fonctions de "vrai" dessin.   --------------------------------------------------------

    def parse_copy_statement(self):
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'copy')
        self.consume('DELIMITER', '(')
        # 3) Lire 4 expressions (séparées par des virgules)
        #    => ARG_LIST_4 = expr, expr, expr, expr
        expr1 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr2 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr3 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr4 = self.parse_expression()

        # 4) consommer ')'
        self.consume('DELIMITER', ')')

        # 5) consommer le mot-clé 'to'
        self.consume('KEYWORD', 'to')

        # 6) consommer '('
        self.consume('DELIMITER', '(')

        # 7) Lire 2 expressions (séparées par une virgule)
        #    => ARG_LIST_2 = expr, expr
        expr5 = self.parse_expression()
        self.consume('DELIMITER', ',')
        expr6 = self.parse_expression()

        # 8) consommer ')'
        self.consume('DELIMITER', ')')        
        self.consume('DELIMITER', ';')

        return {
            "node_type": "copy_statement",
            "source": [expr1, expr2, expr3, expr4],
            "destination": [expr5, expr6],
            "line": line_num
        }

    def parse_animate_statement(self):
        line_num = self.current_token()["line"]
        self.consume('KEYWORD', 'animate')
        self.consume('DELIMITER', '(')
        expr1 = self.parse_expression()
        # 4) Consommer la virgule
        self.consume('DELIMITER', ',')
        # 5) Deuxième expression (par ex. 10)
        expr2 = self.parse_expression()
        # 6) Consommer ')'
        self.consume('DELIMITER', ')')        
        body_node = self.parse_block()
        return {
            "node_type": "animate_statement",
            "obj_or_expr1": expr1,
            "expr2": expr2,
            "body": body_node,
            "line": line_num
        }

#████████████████████████████████████████████ CURSEURS ████████████████████████████████████████████

# Declaration de curseur
    def parse_cursor_declaration(self):
        """
        cursor_declaration ::= 'cursor' IDENTIFIER '=' 'cursor' '(' [ argument_list ] ')' ';'
        """
        line_num = self.current_token()["line"]
        
        # 1) On consomme le mot-clé 'cursor'
        self.consume('KEYWORD', 'Cursor')
        
        # 2) On attend un identifiant (ex: myCursor)
        id_token = self.consume('IDENTIFIER')
        var_name = id_token['value']
        
        # 3) On attend '='
        self.consume('ASSIGN', '=')
        
        # 4) On attend le mot-clé 'cursor' pour appeler le "constructeur"
        if not self.match('KEYWORD', 'Cursor'):
            raise ParserError("Initialisation de curseur invalide : 'cursor(...)' attendu.")
        self.consume('KEYWORD', 'Cursor')
        
        # 5) On consomme '('
        self.consume('DELIMITER', '(')

        # 6) On parse les arguments (optionnel ou non)
        args = []
        if not self.match('DELIMITER', ')'):
            args = self.parse_argument_list()
        
        # 7) On consomme ')'
        self.consume('DELIMITER', ')')
        
        # 8) On consomme le ';'
        self.consume('DELIMITER', ';')
        
        # 9) On construit le nœud AST
        return {
            "node_type": "cursor_declaration",
            "name": var_name,
            "constructor_args": args,
            "line": line_num
        }

    def looks_like_cursor_method(self):
        # Vérifie qu'il y a assez de tokens
        if self.is_at_end():
            return False
        # On veut au moins 4 tokens disponibles
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

    def parse_cursor_method_statement(self):
        """
        Pattern: IDENTIFIER '.' IDENTIFIER '(' [argument_list] ')' ';'
        """
        line_num = self.current_token()["line"]
        
        # 1) Consommer l'objet (ex: myCursor)
        obj_token = self.consume('IDENTIFIER')
        cursor_name = obj_token['value']

        # 2) Consommer le '.'
        self.consume('ACCESS_OPERATOR', '.')

        # 3) Consommer le nom de la méthode (ex: moveTo)
        method_token = self.consume('IDENTIFIER')
        method_name = method_token['value']

        # 4) Consommer '('
        self.consume('DELIMITER', '(')

        # 5) Parse l’argument_list
        args = []
        if not self.match('DELIMITER', ')'):
            args = self.parse_argument_list()

        # 6) Consommer ')'
        self.consume('DELIMITER', ')')

        # 7) Consommer le ';'
        self.consume('DELIMITER', ';')

        return {
            "node_type": "cursor_method",
            "cursor_name": cursor_name,
            "method": method_name,
            "arguments": args,
            "line": line_num
        }








#██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#███████████████████████████████████████████████████████████████████ ANALYSEUR SEMANTIQUE   ███████████████████████████████████████████████████████████████████████████████


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def analyze(self, ast_nodes):
        for node in ast_nodes:
            self.analyze_statement(node)
        return self.errors

    def analyze_statement(self, node):
        node_type = node["node_type"]
        if node_type == "var_declaration":
            self.analyze_var_declaration(node)
        elif node_type == "cursor_declaration":
            self.analyze_cursor_declaration(node)
        elif node_type == "if_statement":
            self.analyze_if_statement(node)
        elif node_type == "for_statement":
            self.analyze_for_statement(node)
        elif node_type == "while_statement":
            self.analyze_while_statement(node)
        elif node_type == "function_declaration":
            self.analyze_function_declaration(node)
        elif node_type == "return_statement":
            self.analyze_return_statement(node)
        elif node_type == "copy_statement":
            self.analyze_copy_statement(node)
        elif node_type == "animate_statement":
            self.analyze_animate_statement(node)
        elif node_type == "cursor_method":
            self.analyze_cursor_method(node)
        elif node_type == "empty_statement":
            pass
        elif node_type == "expression_statement":
            self.analyze_expression_statement(node)
        elif node_type == "var_declaration_no_semi":
            self.analyze_var_declaration(node)
        else:
            self.errors.append(f"Statement inconnu : {node_type}")

    def analyze_var_declaration(self, node):
        var_name = node["name"]
        if var_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Variable '{var_name}' déjà déclarée."
            )
        else:
            # Ex. on enregistre 'number' par défaut
            self.symbols[var_name] = "number"

    def analyze_cursor_declaration(self, node):
        cursor_name = node["name"]
        if cursor_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Cursor '{cursor_name}' déjà déclaré."
            )
        else:
            self.symbols[cursor_name] = "cursor"

    def analyze_cursor_method(self, node):
        cursor_name = node["cursor_name"]
        if cursor_name not in self.symbols:
            self.errors.append(f"Ligne {node['line']}: Variable '{cursor_name}' non déclarée.")
            return
        if self.symbols[cursor_name] != "cursor":
            self.errors.append(f"Ligne {node['line']}: '{cursor_name}' n'est pas un curseur.")
            return

        method = node["method"]
        args = node["arguments"]

        # Méthodes valides mises à jour
        valid_methods = {
            "move": 2,           # Remplacement de "moveTo" par "move(xOuY, pixels)"
            "rotate": 1,
            "drawCircle": 1,
            "drawSegment": 1,
            "drawSquare": 1,
            "drawPoint": 1,
            "setColor": 1,       # Nouvelle méthode
            "setThickness": 1    # Nouvelle méthode
        }

        # Vérifie que la méthode appelée fait partie des méthodes valides
        if method not in valid_methods:
            self.errors.append(
                f"Ligne {node['line']}: Méthode '{method}' inconnue pour un curseur."
            )
            return

        # Vérifie que le nombre d’arguments correspond
        expected_args = valid_methods[method]
        if len(args) != expected_args:
            self.errors.append(
                f"Ligne {node['line']}: La méthode '{method}' attend {expected_args} argument(s), reçu {len(args)}."
            )


    # -- ICI on remet les méthodes d'analyse au même niveau que les autres --
    def analyze_if_statement(self, node):
        self.analyze_expression(node["condition"])
        self.analyze_block(node["then_block"])
        if node["else_block"] is not None:
            self.analyze_block(node["else_block"])

    def analyze_block(self, block_node):
        for stmt in block_node["statements"]:
            self.analyze_statement(stmt)

    def analyze_expression_statement(self, node):
        self.analyze_expression(node["expression"])

    def analyze_expression(self, expr):
        node_type = expr["node_type"]
        if node_type == "binary_op":
            self.analyze_expression(expr["left"])
            self.analyze_expression(expr["right"])
        elif node_type == "unary_op":
            self.analyze_expression(expr["expr"])
        elif node_type == "identifier":
            if expr["value"] not in self.symbols:
                self.errors.append("Variable non déclarée: " + expr["value"])
        elif node_type in ("number", "string", "bool_literal"):
            pass
        elif node_type == "call_expr":
            # Gérer la sémantique d’un appel de fonction si besoin
            for arg in expr["arguments"]:
                self.analyze_expression(arg)
        # etc.

    def analyze_for_statement(self, node):
        init_node = node["init"]
        if init_node is not None:
            self.analyze_statement(init_node)

        condition_node = node["condition"]
        if condition_node is not None:
            self.analyze_expression(condition_node)

        increment_node = node["increment"]
        if increment_node is not None:
            self.analyze_expression(increment_node)

        body_node = node["body"]
        self.analyze_block(body_node)

    def analyze_while_statement(self, node):
        condition_node = node["condition"]
        if condition_node is not None:
            self.analyze_expression(condition_node)

        body_node = node["body"]
        self.analyze_block(body_node)

    def analyze_function_declaration(self, node):
        func_name = node["name"]
        if func_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Fonction '{func_name}' déjà déclarée."
            )
        else:
            self.symbols[func_name] = "function"

        # Analyser le corps de la fonction
        body_block = node["body"]
        self.analyze_block(body_block)

    def analyze_return_statement(self, node):
        if node["expression"] is not None:
            self.analyze_expression(node["expression"])

    def analyze_copy_statement(self, node):
        for expr in node["source"]:
            self.analyze_expression(expr)
        for expr in node["destination"]:
            self.analyze_expression(expr)

    def analyze_animate_statement(self, node):
        self.analyze_expression(node["obj_or_expr1"])
        self.analyze_expression(node["expr2"])
        self.analyze_block(node["body"])
























#############################
# TEST DES FOPNCTIONS AVEC DES CHAINES DE TOKEN
#############################

# --------------------- CORRECT TOKENS ---------------------
correct_tokens = [
    # 1) Déclaration d’un curseur
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 1},
    {'type': 'IDENTIFIER', 'value': 'myCur', 'line': 1},
    {'type': 'ASSIGN', 'value': '=', 'line': 1},
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 1},
    {'type': 'DELIMITER', 'value': '(', 'line': 1},
    {'type': 'NUMBER', 'value': 100.0, 'line': 1},
    {'type': 'DELIMITER', 'value': ',', 'line': 1},
    {'type': 'NUMBER', 'value': 200.0, 'line': 1},
    {'type': 'DELIMITER', 'value': ')', 'line': 1},
    {'type': 'DELIMITER', 'value': ';', 'line': 1},

    # 2) Méthode du curseur
    {'type': 'IDENTIFIER', 'value': 'myCur', 'line': 2},
    {'type': 'ACCESS_OPERATOR', 'value': '.', 'line': 2},
    {'type': 'IDENTIFIER', 'value': 'moveTo', 'line': 2},
    {'type': 'DELIMITER', 'value': '(', 'line': 2},
    {'type': 'NUMBER', 'value': 300.0, 'line': 2},
    {'type': 'DELIMITER', 'value': ',', 'line': 2},
    {'type': 'NUMBER', 'value': 400.0, 'line': 2},
    {'type': 'DELIMITER', 'value': ')', 'line': 2},
    {'type': 'DELIMITER', 'value': ';', 'line': 2},

    # 3) Var
    {'type': 'KEYWORD', 'value': 'var', 'line': 3},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 3},
    {'type': 'ASSIGN', 'value': '=', 'line': 3},
    {'type': 'NUMBER', 'value': 10.0, 'line': 3},
    {'type': 'DELIMITER', 'value': ';', 'line': 3},

    # 4) if ( x > 5 ) { x = x + 1; } else { x = x - 1; }
    {'type': 'KEYWORD', 'value': 'if', 'line': 4},
    {'type': 'DELIMITER', 'value': '(', 'line': 4},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 4},
    {'type': 'OPERATOR', 'value': '>', 'line': 4},
    {'type': 'NUMBER', 'value': 5.0, 'line': 4},
    {'type': 'DELIMITER', 'value': ')', 'line': 4},
    {'type': 'DELIMITER', 'value': '{', 'line': 4},
    # x = x + 1;
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 5},
    {'type': 'ASSIGN', 'value': '=', 'line': 5},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 5},
    {'type': 'OPERATOR', 'value': '+', 'line': 5},
    {'type': 'NUMBER', 'value': 1.0, 'line': 5},
    {'type': 'DELIMITER', 'value': ';', 'line': 5},
    {'type': 'DELIMITER', 'value': '}', 'line': 6},
    {'type': 'KEYWORD', 'value': 'else', 'line': 6},
    {'type': 'DELIMITER', 'value': '{', 'line': 6},
    # x = x - 1;
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 7},
    {'type': 'ASSIGN', 'value': '=', 'line': 7},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 7},
    {'type': 'OPERATOR', 'value': '-', 'line': 7},
    {'type': 'NUMBER', 'value': 1.0, 'line': 7},
    {'type': 'DELIMITER', 'value': ';', 'line': 7},
    {'type': 'DELIMITER', 'value': '}', 'line': 8},

    # 5) for ( var i = 0 ; i < 5 ; i = i + 1 ) { ... }
    {'type': 'KEYWORD', 'value': 'for', 'line': 9},
    {'type': 'DELIMITER', 'value': '(', 'line': 9},
    # init: var i = 0
    {'type': 'KEYWORD', 'value': 'var', 'line': 9},
    {'type': 'IDENTIFIER', 'value': 'i', 'line': 9},
    {'type': 'ASSIGN', 'value': '=', 'line': 9},
    {'type': 'NUMBER', 'value': 0.0, 'line': 9},
    {'type': 'DELIMITER', 'value': ';', 'line': 9},
    # condition: i < 5
    {'type': 'IDENTIFIER', 'value': 'i', 'line': 9},
    {'type': 'OPERATOR', 'value': '<', 'line': 9},
    {'type': 'NUMBER', 'value': 5.0, 'line': 9},
    {'type': 'DELIMITER', 'value': ';', 'line': 9},
    # incr: i = i + 1
    {'type': 'IDENTIFIER', 'value': 'i', 'line': 9},
    {'type': 'ASSIGN', 'value': '=', 'line': 9},
    {'type': 'IDENTIFIER', 'value': 'i', 'line': 9},
    {'type': 'OPERATOR', 'value': '+', 'line': 9},
    {'type': 'NUMBER', 'value': 1.0, 'line': 9},
    {'type': 'DELIMITER', 'value': ')', 'line': 9},
    {'type': 'DELIMITER', 'value': '{', 'line': 9},
    # body: x = x + 2;
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 10},
    {'type': 'ASSIGN', 'value': '=', 'line': 10},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 10},
    {'type': 'OPERATOR', 'value': '+', 'line': 10},
    {'type': 'NUMBER', 'value': 2.0, 'line': 10},
    {'type': 'DELIMITER', 'value': ';', 'line': 10},
    {'type': 'DELIMITER', 'value': '}', 'line': 11},

    # 6) while ( x < 50 ) { x = x + 10; }
    {'type': 'KEYWORD', 'value': 'while', 'line': 12},
    {'type': 'DELIMITER', 'value': '(', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 12},
    {'type': 'OPERATOR', 'value': '<', 'line': 12},
    {'type': 'NUMBER', 'value': 50.0, 'line': 12},
    {'type': 'DELIMITER', 'value': ')', 'line': 12},
    {'type': 'DELIMITER', 'value': '{', 'line': 12},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 13},
    {'type': 'ASSIGN', 'value': '=', 'line': 13},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 13},
    {'type': 'OPERATOR', 'value': '+', 'line': 13},
    {'type': 'NUMBER', 'value': 10.0, 'line': 13},
    {'type': 'DELIMITER', 'value': ';', 'line': 13},
    {'type': 'DELIMITER', 'value': '}', 'line': 14},

    # 7) function foo(x) { return x; }
    {'type': 'KEYWORD', 'value': 'function', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'foo', 'line': 15},
    {'type': 'DELIMITER', 'value': '(', 'line': 15},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 15},
    {'type': 'DELIMITER', 'value': ')', 'line': 15},
    {'type': 'DELIMITER', 'value': '{', 'line': 15},
    {'type': 'KEYWORD', 'value': 'return', 'line': 16},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 16},
    {'type': 'DELIMITER', 'value': ';', 'line': 16},
    {'type': 'DELIMITER', 'value': '}', 'line': 17},

    # 8) copy(10, 20, 200, 200) to (400, 400);
    {'type': 'KEYWORD', 'value': 'copy', 'line': 18},
    {'type': 'DELIMITER', 'value': '(', 'line': 18},
    {'type': 'NUMBER', 'value': 10.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ',', 'line': 18},
    {'type': 'NUMBER', 'value': 20.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ',', 'line': 18},
    {'type': 'NUMBER', 'value': 200.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ',', 'line': 18},
    {'type': 'NUMBER', 'value': 200.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ')', 'line': 18},
    {'type': 'KEYWORD', 'value': 'to', 'line': 18},
    {'type': 'DELIMITER', 'value': '(', 'line': 18},
    {'type': 'NUMBER', 'value': 400.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ',', 'line': 18},
    {'type': 'NUMBER', 'value': 400.0, 'line': 18},
    {'type': 'DELIMITER', 'value': ')', 'line': 18},
    {'type': 'DELIMITER', 'value': ';', 'line': 18},
]
"""
    # 9) animate(obj, 10) { x = x + 100; }
    {'type': 'KEYWORD', 'value': 'animate', 'line': 19},
    {'type': 'DELIMITER', 'value': '(', 'line': 19},
    {'type': 'IDENTIFIER', 'value': 'obj', 'line': 19},
    {'type': 'DELIMITER', 'value': ',', 'line': 19},
    {'type': 'NUMBER', 'value': 10.0, 'line': 19},
    {'type': 'DELIMITER', 'value': ')', 'line': 19},
    {'type': 'DELIMITER', 'value': '{', 'line': 19},
    # x = x + 100;
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 20},
    {'type': 'ASSIGN', 'value': '=', 'line': 20},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 20},
    {'type': 'OPERATOR', 'value': '+', 'line': 20},
    {'type': 'NUMBER', 'value': 100.0, 'line': 20},
    {'type': 'DELIMITER', 'value': ';', 'line': 20},
    {'type': 'DELIMITER', 'value': '}', 'line': 21},
"""
# --------------------- INCORRECT TOKENS ---------------------
# On force quelques erreurs sémantiques et syntaxiques :
# 1) Erreur syntaxique: "myCursor" "." "rotate" "(" -> on oublie le ';'
# 2) Erreur sémantique: on appelle "myCur.drawRect(2,3)" qui n'existe pas
incorrect_tokens = [
    
    # cursor myCur = var(100, 200); => Invalide, on a "var" au lieu de "cursor" interne
    {'type': 'KEYWORD', 'value': 'cursor', 'line': 1},
    {'type': 'IDENTIFIER', 'value': 'myCur', 'line': 1},
    {'type': 'ASSIGN', 'value': '=', 'line': 1},
    {'type': 'KEYWORD', 'value': 'var', 'line': 1},  # <-- Mauvais
    {'type': 'DELIMITER', 'value': '(', 'line': 1},
    {'type': 'NUMBER', 'value': 100.0, 'line': 1},
    {'type': 'DELIMITER', 'value': ',', 'line': 1},
    {'type': 'NUMBER', 'value': 200.0, 'line': 1},
    {'type': 'DELIMITER', 'value': ')', 'line': 1},
    {'type': 'DELIMITER', 'value': ';', 'line': 1},

    # var x = 100 => Manque le ';'
    {'type': 'KEYWORD', 'value': 'var', 'line': 2},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 2},
    {'type': 'ASSIGN', 'value': '=', 'line': 2},
    {'type': 'NUMBER', 'value': 100.0, 'line': 2},
    # <-- on n'a pas mis le DELIMITER ';'
 
    # myCur.drawRect(2,3); => sémantique : drawRect n’existe pas Ping bien l'erreur quand le parsing il n'y a pas d'erreur de parsing
    {'type': 'IDENTIFIER', 'value': 'myCur', 'line': 3},
    {'type': 'ACCESS_OPERATOR', 'value': '.', 'line': 3},
    {'type': 'IDENTIFIER', 'value': 'drawRect', 'line': 3},
    {'type': 'DELIMITER', 'value': '(', 'line': 3},
    {'type': 'NUMBER', 'value': 2.0, 'line': 3},
    {'type': 'DELIMITER', 'value': ',', 'line': 3},
    {'type': 'NUMBER', 'value': 3.0, 'line': 3},
    {'type': 'DELIMITER', 'value': ')', 'line': 3},
    {'type': 'DELIMITER', 'value': ';', 'line': 3},
    

    # Mauvaise syntaxe: myCur rotate(30); => manque le '.'
    {'type': 'IDENTIFIER', 'value': 'myCur', 'line': 4},
    {'type': 'IDENTIFIER', 'value': 'rotate', 'line': 4},  # <-- pas d'ACCESS_OPERATOR
    {'type': 'DELIMITER', 'value': '(', 'line': 4},
    {'type': 'NUMBER', 'value': 30.0, 'line': 4},
    {'type': 'DELIMITER', 'value': ')', 'line': 4},
    {'type': 'DELIMITER', 'value': ';', 'line': 4},

]
def test_parser_and_semantic():
    print("Tokens fournis au parser :", correct_tokens)

    print("========== TEST PARSER & SEMANTIC (CORRECT) ==========")
    try:
        parser = DrawScriptParser(correct_tokens)
        print("Lancement du parsing pour les tokens corrects...")
        ast_correct, parse_errors_correct = parser.parse()
        print("Parsing terminé.")
        print("Parse errors (correct tokens):")
        for e in parse_errors_correct:
            print(e)
        if not parse_errors_correct:
            print("-- Pas d'erreur de parsing, c'est bon !")
        print("\n--- AST (correct) ---")
        print(ast_correct)

        analyzer = SemanticAnalyzer()
        print("Lancement de l'analyse sémantique pour les tokens corrects...")
        semantic_errors_correct = analyzer.analyze(ast_correct)
        print("Analyse sémantique terminée.")
        print("\nSemantic errors (correct tokens):")
        for e in semantic_errors_correct:
            print(e)
        if not semantic_errors_correct:
            print("-- Pas d'erreur sémantique, c'est bon !")
    except Exception as e:
        print(f"Erreur détectée pendant le traitement des tokens corrects : {e}")
    
    print("\n========== TEST PARSER & SEMANTIC (INCORRECT) ==========")
    try:
        parser2 = DrawScriptParser(incorrect_tokens)
        print("Lancement du parsing pour les tokens incorrects...")
        ast_incorrect, parse_errors_incorrect = parser2.parse()
        print("Parsing terminé.")
        print("Parse errors (incorrect tokens):")
        for e in parse_errors_incorrect:
            print(e)
        if not parse_errors_incorrect:
            print("-- Pas d'erreur de parsing sur incorrect ? (Surprenant)")
        
        if ast_incorrect:
            print("\n--- AST (incorrect) ---")
            print(ast_incorrect)
        else:
            print("\n-- L'AST est vide, le parsing a complètement échoué --")

        analyzer2 = SemanticAnalyzer()
        print("Lancement de l'analyse sémantique pour les tokens incorrects...")
        semantic_errors_incorrect = analyzer2.analyze(ast_incorrect)
        print("Analyse sémantique terminée.")
        print("\nSemantic errors (incorrect tokens):")
        for e in semantic_errors_incorrect:
            print(e)
        if not semantic_errors_incorrect and ast_incorrect:
            print("-- Pas d'erreur sémantique sur incorrect ? (Surprenant)")
    except Exception as e:
        print(f"Erreur détectée pendant le traitement des tokens incorrects : {e}")

if __name__ == "__main__":
    test_parser_and_semantic()



