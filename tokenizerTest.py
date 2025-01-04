from DrawScript.Core.drawScriptTokenizer import DrawScriptTokenizer
from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Core.drawScriptDeserializerC import DrawScriptDeserializerC

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
    Cursor cursor1 = Cursor(centerX, centerY);

    // 5. Boucle for pour dessiner plusieurs cercles
    for (var i = 0; i < numCircles; i = i + 1) {
        var offsetX = centerX + (radius * 3) * cos(angle + (i * (360 / numCircles)));
        var offsetY = centerY + (radius * 3) * sin(angle + (i * (360 / numCircles)));
        drawCircle(offsetX, offsetY, radius);
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

parser = DrawScriptParser(tokens)
ast_nodes, errors = parser.parse()

interpreter = DrawScriptDeserializerC(ast_nodes)
interpreter.write_c()