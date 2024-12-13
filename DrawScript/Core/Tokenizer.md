# Rappel
Ma partie consiste à détailler le script Python `drawScriptTokenizer.py`, qui joue un rôle clé dans l'analyse lexicale des programmes écrits en **draw++**. Cette analyse est une étape préliminaire à la compilation ou l'exécution d'un code **draw++**.

# Structure Générale de `drawScriptTokenizer`
Le fichier Python `drawScriptTokenizer.py` implémente une classe `DrawScriptTokenizer` qui convertit un programme draw++ en une liste de tokens (jetons). Ces jetons servent ensuite à identifier les éléments syntaxiques et à signaler les erreurs potentielles.

Le script se décompose en plusieurs parties principales :

- **Initialisation :** Définit les attributs de la classe et prépare les structures nécessaires pour la tokenisation.
- **Définition des expressions régulières :** Spécifie les règles lexicales pour reconnaître les types de tokens.
- **Processus de tokenisation :** Analyse le code, ligne par ligne, pour générer des tokens et détecter des erreurs.
- **Gestion des erreurs :** Identifie les erreurs dans le code source et les rapporte.

# Initialisation du Tokenizer
## Code Source
```python
class DrawScriptTokenizer:
    def __init__(self):
        # Initialisation du tokenizer
        self.cursors = {}  # Dictionnaire pour stocker les curseurs (non utilisé dans ce code)
```

## Explication
Lors de l'initialisation :

- L'attribut `cursors` est créé pour stocker les curseurs définis dans le code draw++. Cependant, dans ce script, il n'est pas encore utilisé activement.
- Cette initialisation prépare la structure pour des extensions futures, comme la gestion des curseurs lors de l'analyse lexicale ou syntaxique.

# Définition des Règles Lexicales
La méthode `tokenize` est au cœur de la classe. Elle commence par définir les règles lexicales sous forme d'expressions régulières, organisées en catégories de tokens.

## Code Source
```python
token_specification = [
    ('NEWLINE', r'\n'),                      # Nouvelle ligne
    ('WHITESPACE', r'[ ]+'),                 # Espaces et tabulations
    ('MULTILINE_COMMENT', r'/\*.*?\*/'),   # Commentaire sur plusieurs lignes
    ('COMMENT', r'//.*'),                    # Commentaire sur une ligne
    ('NUMBER', r'-?\d+(\.\d+)?'),         # Nombres entiers ou décimaux
    ('STRING', r'"[^"]*"'),               # Chaînes de caractères
    ('BOOLEAN', r'(true|false)'),            # Booléens
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiants
    ('ACCESS_OPERATOR', r'\.'),            # Opérateur d'accès
    ('OPERATOR', r'[+\-*/%]|==|!=|<=|>=|<|>|&&|\|\||!'),
    ('DELIMITER', r'[(){};,\:]'),           # Délimiteurs
    ('ASSIGN', r'='),                        # Opérateur d'affectation
    ('MISMATCH', r'.'),                      # Caractère non reconnu
]
```

## Explication
Cette liste associe chaque type de token à une expression régulière :

- **NEWLINE** reconnaît les sauts de ligne pour suivre correctement les numéros de ligne.
- **WHITESPACE** détecte les espaces et tabulations à ignorer.
- **COMMENT** et **MULTILINE_COMMENT** traitent les commentaires (une ou plusieurs lignes).
- **NUMBER**, **STRING** et **BOOLEAN** identifient les valeurs littérales.
- **IDENTIFIER** reconnaît les noms de variables et de fonctions, en distinguant les mots-clés.
- **OPERATOR** et **DELIMITER** capturent les opérateurs et délimiteurs syntaxiques.
- **MISMATCH** identifie les caractères non reconnus, signalant des erreurs potentielles.

# Gestion des Mots-Clés
En plus des expressions régulières, un ensemble de mots-clés est défini pour identifier des instructions spécifiques à draw++.

## Code Source
```python
keywords = {
    'var', 'function', 'if', 'else', 'while', 'for',
    'copy', 'animate', 'to', 'cursor', 'return', 'clear',
}
```

## Explication
Ces mots-clés couvrent les principales instructions du langage draw++ :

- `var`, `function` pour les déclarations.
- `if`, `else` pour les conditions.
- `while`, `for` pour les boucles.
- `copy`, `animate` pour les instructions graphiques spécifiques.

# Processus de Tokenisation
La fonction `tokenize` est responsable de parcourir le code draw++ pour identifier et classifier les éléments syntaxiques en utilisant les règles lexicales définies précédemment.

## Code Source
```python
def tokenize(self, code):
    pos = 0          # Position actuelle dans le code
    tokens = []      # Liste des tokens générés
    errors = []      # Liste des erreurs (0 si pas d'erreur, 1 si erreur)
    line_number = 1  # Numéro de ligne, commence à 1

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
            line_number += value.count('\n')  # Compter les nouvelles lignes
        elif kind == 'IDENTIFIER':
            if value in keywords:
                kind = 'KEYWORD'  # Identifier les mots-clés
            tokens.append({'type': kind, 'value': value, 'line': line_number})
            errors.append(0)
        elif kind == 'NUMBER':
            tokens.append({'type': kind, 'value': float(value), 'line': line_number})
            errors.append(0)
        elif kind == 'STRING':
            tokens.append({'type': kind, 'value': value[1:-1], 'line': line_number})
            errors.append(0)
        elif kind in {'OPERATOR', 'DELIMITER', 'ASSIGN', 'ACCESS_OPERATOR'}:
            tokens.append({'type': kind, 'value': value, 'line': line_number})
            errors.append(0)
        elif kind == 'MISMATCH':
            tokens.append({'type': 'UNKNOWN', 'value': value, 'line': line_number})
            errors.append(1)

        pos = mo.end()
        mo = get_token(code, pos)

    if pos != len(code):
        remaining = code[pos:]
        for char in remaining:
            if char == '\n':
                line_number += 1
            tokens.append({'type': 'UNKNOWN', 'value': char, 'line': line_number})
            errors.append(1)

    return tokens, errors
```

## Explication
La fonction effectue les étapes suivantes :

- Initialise les variables pour suivre la position dans le code et stocker les tokens et erreurs.
- Utilise les expressions régulières pour trouver les correspondances dans le code.
- Traite chaque correspondance selon son type, en ajoutant des tokens valides ou en signalant des erreurs.
- Gère les commentaires et les espaces blancs en les ignorant.
- Retourne les listes de tokens et d'erreurs à la fin de l'analyse.

# Exemples de Tokenisation
Voici un exemple d'utilisation de la classe `DrawScriptTokenizer` avec un code draw++ simple :

## Exemple de Code Source
```python
code = """
var x = 10;
var y = 20;
function draw() {
    circle(x, y, 5);
}
"""

# Tokenisation
tokens, errors = tokenizer.tokenize(code)
```

## Résultat Obtenu
```python
Tokens = [
    {'type': 'KEYWORD', 'value': 'var', 'line': 1},
    {'type': 'IDENTIFIER', 'value': 'x', 'line': 1},
    {'type': 'ASSIGN', 'value': '=', 'line': 1},
    {'type': 'NUMBER', 'value': 10.0, 'line': 1},
    {'type': 'DELIMITER', 'value': ';', 'line': 1},
    ...
]
```

## Explication
Chaque ligne du code est analysée pour produire des tokens qui reflètent sa structure syntaxique. Les erreurs sont rapportées lorsqu'un élément non reconnu est trouvé.

# Gestion des Erreurs
Les erreurs sont identifiées en utilisant le token `MISMATCH` ou lorsque le code contient des caractères non reconnus après la fin de la correspondance principale. Chaque erreur est enregistrée avec des informations sur la ligne concernée, ce qui facilite le débogage.

# Idées d'Extensions Futures
Pour améliorer le tokenizer, voici quelques pistes :

- Ajouter la gestion active des curseurs définis dans `self.cursors`.
- Implémenter des tests unitaires pour valider chaque fonctionnalité.
- Intégrer des fonctionnalités avancées comme la détection de structures imbriquées complexes.
