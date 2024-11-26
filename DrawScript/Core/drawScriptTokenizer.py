import re  # Bibliothèque pour les expressions régulières
from drawScriptParser import DrawScriptParser

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

        # Compilation des expressions régulières en une seule expression
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex, re.MULTILINE).match  # Utilisation de MULTILINE pour gérer les débuts de lignes correctement

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
            '''
            # Debug: Afficher le token courant
            print(f"Matched {kind}: '{value}' at line {line_number}")
            '''
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

""" Exemple utilisation Tokenizer.py
"""
tokenizer = DrawScriptTokenizer()

code = """/*
    * Exemple complet de draw++ utilisant toutes les fonctionnalités
    * Auteur : Votre Nom
    * Date : Date du jour
    */

    // 1. Déclarations de variables
    var centerX = 300;
    var centerY = 300;
    var radius = 50;
    var numCircles = 5;
    var angle = 0;
    var speed = 0.05;
    var isAnimating = true;

    // 2. Déclaration d'une variable de type cursor
    var myCursor : cursor = cursor(centerX, centerY);

    // 3. Fonction pour dessiner un cercle
    function drawCircle(x, y, r) {
        // Appel à une fonction prédéfinie
        circle(x, y, r);
    }

    // 4. Fonction pour dessiner une étoile
    function drawStar(x, y, size) {
        // Logique pour dessiner une étoile
        polygon(x, y, size, 5, 2);
    }

    // 5. Boucle for pour dessiner plusieurs cercles
    for (var i = 0; i < numCircles; i = i + 1) {
        var offsetX = centerX + (radius * 3) * cos(angle + (i * (360 / numCircles)));
        var offsetY = centerY + (radius * 3) * sin(angle + (i * (360 / numCircles)));
        drawCircle(offsetX, offsetY, radius);
    }

    // 6. Animation
    animate(starObject, 10) {
        while (isAnimating) {
            // Mise à jour de l'angle
            angle = angle + speed;

            // Mise à jour de la position de l'étoile
            var starX = centerX + (radius * 4) * cos(angle);
            var starY = centerY + (radius * 4) * sin(angle);

            // Effacer l'ancienne étoile
            clear(starObject);

            // Redessiner l'étoile à la nouvelle position
            drawStar(starX, starY, radius);

            // Vérification pour arrêter l'animation après un tour complet
            if (angle >= 360) {
                isAnimating = false;
            }
        }
    }

    // 7. Instruction copy-paste
    copy(100, 100, 200, 200) to (400, 400);

    // 8. Instruction conditionnelle if-else
    if (radius > 40 && numCircles >= 5) {
        // Dessiner un grand carré si la condition est vraie
        drawSquare(centerX, centerY, radius * 2);
    } else {
        // Sinon, dessiner un triangle
        drawTriangle(centerX, centerY, radius * 2);
    }

    // 9. Boucle while imbriquée pour créer une grille
    var gridX = 0;
    while (gridX <= 600) {
        var gridY = 0;
        while (gridY <= 600) {
            // Dessiner un petit cercle à chaque point de la grille
            drawCircle(gridX, gridY, 5);
            gridY = gridY + 50;
        }
        gridX = gridX + 50;
    }

    // 10. Utilisation du curseur pour dessiner une forme géométrique
    myCursor.moveTo(400, 300);      // Déplacer le curseur en traçant une ligne
    myCursor.rotate(90);            // Tourner le curseur de 90 degrés
    myCursor.drawLine(400, 400);    // Dessiner une ligne jusqu'au point (400, 400)
    myCursor.drawCircle(50);        // Dessiner un cercle de rayon 50 à la position actuelle
    myCursor.drawRectangle(100, 50);// Dessiner un rectangle de largeur 100 et hauteur 50

    // 11. Appel de fonction
    drawCircle(250, 250, 75);

    // 12. Fin du script
    """

# Analyse de la chaîne et récupération des résultats
tokens, errors = tokenizer.tokenize(code)


# Affichage des résultats
print("Tokens:")
for token in tokens:
    print(token)
"""
print("\nErrors:")
print(errors)
"""

"""
"""