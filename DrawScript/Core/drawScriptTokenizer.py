import re  # Bibliothèque pour les expressions régulières

class DrawScriptTokenizer:
    def __init__(self):
        # Initialisation du tokenizer
        self.cursors = {}  # Dictionnaire pour stocker les curseurs (non utilisé dans ce code)

    def tokenize(self, code):
        """
        Cette méthode prend en entrée une chaîne de caractères 'code' contenant le code source du langage draw++.
        Elle retourne une liste de tokens et une liste d'erreurs correspondantes.
        """

        # Définir les expressions régulières pour chaque type de jeton
        token_specification = [
            ('COMMENT',       r'(//|#).*'),  # Commentaires
            ('NUMBER',        r'\d+(\.\d+)?'),  # Nombres entiers ou flottants
            ('STRING',        r'"([^"\\]|\\.)*"'),  # Chaînes de caractères
            ('IDENTIFIER',    r'[A-Za-z_]\w*'),  # Identifiants
            ('OPERATOR',      r'==|!=|<=|>=|&&|\|\||[+\-*/%<>=!&|]'),  # Opérateurs
            ('DELIMITER',     r'[;,(){}]'),  # Délimiteurs
            ('WHITESPACE',    r'\s+'),  # Espaces blancs (à ignorer)
            ('MISMATCH',      r'.'),  # Tout autre caractère
        ]

        # Compilation des expressions régulières en une seule expression
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex, re.DOTALL).match  # Utilisation de DOTALL pour que '.' corresponde aux nouvelles lignes

        # Définition des mots-clés du langage
        keywords = {
            'var', 'function', 'if', 'else', 'while', 'for',
            'copy', 'animate', 'to', 'cursor', 'return', 'clear',
        }

        # Initialisation des variables pour la tokenisation
        pos = 0          # Position actuelle dans le code
        tokens = []      # Liste des tokens générés
        errors = []      # Liste des erreurs (0 si pas d'erreur, 1 si erreur)
        line_number = 1  # Numéro de ligne, commence à 1

        # Démarrer la correspondance des tokens
        mo = get_token(code, pos)  # mo est un objet Match
        while mo is not None:
            kind = mo.lastgroup    # Type du token correspondant
            value = mo.group(kind) # Valeur du token
            if kind == 'NEWLINE':
                line_number += 1
            elif kind == 'WHITESPACE':
                pass  # Ignorer les espaces blancs
            elif kind == 'COMMENT':
                pass  # Ignorer les commentaires sur une ligne
            elif kind == 'MULTILINE_COMMENT':
                line_number += value.count('\n')  # Compter les nouvelles lignes dans les commentaires
            elif kind == 'IDENTIFIER':
                if value in keywords:
                    kind = 'KEYWORD'  # Si l'identifiant est un mot-clé, changer son type
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)  # Pas d'erreur pour ce token
            elif kind == 'NUMBER':
                tokens.append({'type': kind, 'value': float(value), 'line': line_number})
                errors.append(0)
            elif kind == 'STRING':
                # Enlever les guillemets de début et de fin
                tokens.append({'type': kind, 'value': value[1:-1], 'line': line_number})
                errors.append(0)
                line_number += value.count('\n')  # Compter les nouvelles lignes dans les strings si multi-ligne
            elif kind in {'OPERATOR', 'DELIMITER'}:
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'MISMATCH': #Le Code se stop si le tokenize specification n'est pas reconnu 
                tokens.append({'type': 'UNKNOWN', 'value': value, 'line': line_number})
                errors.append(1)  # Indiquer une erreur pour ce jeton
                print("Errors drawScriptTokenizer.py type Unknow:") 
                print(errors)
                exit()
            pos = mo.end()
            mo = get_token(code, pos)

        if pos != len(code):
            # Gérer le cas où la tokenisation s'arrête avant la fin du code
            tokens.append({'type': 'UNKNOWN', 'value': code[pos:], 'line': line_number})
            errors.append(1)


        return tokens, errors 


""" Exemple utilisation Tokenizer.py
tokenizer = DrawScriptTokenizer()

# Analyse de la chaîne et récupération des résultats
tokens, errors = tokenizer.tokenize("#")

# Affichage des résultats
print("Tokens:")
for token in tokens:
    print(token)

print("\nErrors:")
print(errors)
"""
