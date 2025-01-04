import re  # Bibliothèque pour les expressions régulières
from config import DEBUG

# Définir les expressions régulières pour chaque type de jeton
TOKEN_SPECIFICATION = [
    ('NEWLINE',             r'\n'),                      # Nouvelle ligne
    ('WHITESPACE',          r'[ \t]+'),                  # Espaces et tabulations
    ('MULTILINE_COMMENT', r'/\*[\s\S]*?\*/'),           # Commentaire sur plusieurs lignes
    ('COMMENT',             r'//.*'),                    # Commentaire sur une ligne
    ('NUMBER', r'-?\d+(\.\d+)?|\.\d+'),                  # Nombres entiers ou décimaux (positifs et négatifs)
    ('STRING',              r'"[^"\n]*"'),               # Chaînes de caractères entre guillemets (sans saut de ligne)
    ('BOOLEAN',             r'\b(true|false)\b'),        # Booléens
    ('IDENTIFIER',          r'[A-Za-z_]\w*'),            # Identifiants
    ('ACCESS_OPERATOR',     r'\.'),                      # Opérateur d'accès (séparé des autres opérateurs)
    ('OPERATOR',            r'\+|\-|\*|\/|\%|==|!=|<=|>=|<|>|&&|\|\||!'),  # Autres opérateurs
    ('DELIMITER',           r'\(|\)|\{|\}|;|,|\:'),      # Délimiteurs
    ('ASSIGN',              r'='),                       # Opérateur d'affectation
    ('MISMATCH',            r'.'),                       # Caractère non reconnu
]

# Définition des mots-clés du langage
KEYWORDS = [
    'var', 'function', 'if', 'else', 'while', 'for',
    'copy', 'animate', 'to', 'Cursor', 'return',
]

class DrawScriptTokenizer:
    def __init__(self):
        # Initialisation du tokenizer
        self.cursors = {}  # Dictionnaire pour stocker les curseurs (non utilisé dans ce code)

    def tokenize(self, code):
        """
        Cette méthode prend en entrée une chaîne de caractères 'code' contenant le code source du langage draw++.
        Elle retourne une liste de tokens et une liste d'erreurs correspondantes.
        """

        # Compilation des expressions régulières en une seule expression
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
        get_token = re.compile(tok_regex, re.MULTILINE).match  # Utilisation de MULTILINE pour gérer les débuts de lignes correctement

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
            if DEBUG:
                # Debug: Afficher le token courant
                print(f"Matched {kind}: '{repr(value)[1:-1]}' at line {line_number}")
            if kind == 'NEWLINE':
                line_number += 1
            elif kind == 'WHITESPACE':
                pass  # Ignorer les espaces blancs
            elif kind == 'MULTILINE_COMMENT':
                line_number += value.count('\n')  # Compter les nouvelles lignes dans les commentaires
            elif kind == 'COMMENT':
                pass  # Ignorer les commentaires sur une ligne
            elif kind == 'NUMBER':
                number = float(value)
                if float.is_integer(number):
                    number = round(number)
                tokens.append({'type': kind, 'value': number, 'line': line_number})
                errors.append(0)
            elif kind == 'STRING':
                # Enlever les guillemets de début et de fin
                tokens.append({'type': kind, 'value': value[1:-1], 'line': line_number})
                errors.append(0)
            elif kind == 'BOOLEAN':
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'IDENTIFIER':
                if value in KEYWORDS:
                    kind = 'KEYWORD'  # Si l'identifiant est un mot-clé, changer son type
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)  # Pas d'erreur pour ce token
            elif kind in {'OPERATOR', 'DELIMITER', 'ASSIGN', 'ACCESS_OPERATOR'}:
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'MISMATCH':
                # Token non reconnu, enregistrer une erreur
                tokens.append({'type': 'UNKNOWN', 'value': value, 'line': line_number})
                errors.append(1)  # Indiquer une erreur pour ce jeton
            pos = mo.end()  # Mettre à jour la position
            mo = get_token(code, pos)  # Correspondance suivante

        if pos != len(code):
            # Gérer le cas où la tokenisation s'arrête avant la fin du code
            remaining = code[pos:]
            for char in remaining:
                if char == '\n':
                    line_number += 1
                tokens.append({'type': 'UNKNOWN', 'value': char, 'line': line_number})
                errors.append(1)

        print("\nTokenisation terminée.\n")
        return tokens, errors