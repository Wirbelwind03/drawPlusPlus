import re

class DrawScriptTokenizer:  # Nom de la classe corrigé pour respecter les conventions
    def __init__(self):
        self.cursors = {}  # Dictionary for storing cursors

    def tokenize(self, code):
        # Définir les expressions régulières pour chaque type de jeton
        token_specification = [
            ('COMMENT',       r'//.*'),  # Commentaires
            ('NUMBER',        r'\d+(\.\d+)?'),  # Nombres entiers ou flottants
            ('STRING',        r'"([^"\\]|\\.)*"'),  # Chaînes de caractères
            ('IDENTIFIER',    r'[A-Za-z_]\w*'),  # Identifiants
            ('OPERATOR',      r'==|!=|<=|>=|&&|\|\||[+\-*/%<>=!&|]'),  # Opérateurs
            ('DELIMITER',     r'[;,(){}]'),  # Délimiteurs
            ('WHITESPACE',    r'\s+'),  # Espaces blancs (à ignorer)
            ('MISMATCH',      r'.'),  # Tout autre caractère
        ]

        # Compilation des expressions régulières
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match

        # Mots-clés du langage
        keywords = {
            'var', 'function', 'if', 'else', 'while', 'for',
            'copy', 'animate', 'cursor', 'to',
        }

        # Initialisation
        pos = 0
        tokens = []
        errors = []

        # Tokenisation de tout le code
        line_number = 0
        mo = get_token(code, pos)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'WHITESPACE':
                pass  # Ignorer les espaces blancs
            elif kind == 'COMMENT':
                pass  # Ignorer les commentaires
            elif kind == 'IDENTIFIER':
                if value in keywords:
                    kind = 'KEYWORD'
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'NUMBER':
                tokens.append({'type': kind, 'value': float(value), 'line': line_number})
                errors.append(0)
            elif kind == 'STRING':
                tokens.append({'type': kind, 'value': value[1:-1], 'line': line_number})
                errors.append(0)
            elif kind in {'OPERATOR', 'DELIMITER'}:
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'MISMATCH':
                tokens.append({'type': 'UNKNOWN', 'value': value, 'line': line_number})
                errors.append(1)  # Indiquer une erreur pour ce jeton
            pos = mo.end()
            mo = get_token(code, pos)

        if pos != len(code):
            # Gérer le cas où la tokenisation s'arrête avant la fin du code
            tokens.append({'type': 'UNKNOWN', 'value': code[pos:], 'line': pos})
            errors.append(1)

        return tokens, errors
