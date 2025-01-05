from DrawScript.Core.drawScriptTokenizer import DrawScriptTokenizer
from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Core.drawScriptSemanticAnalyzer import SemanticAnalyzer
from DrawScript.Core.drawScriptDeserializerC import DrawScriptDeserializerC


code = """
/*
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

// 7. Instruction copy-paste
copy(100, 100, 200, 200) to (400, 400);

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
cursor1.move(400, 300);      // Déplacer le curseur en traçant une ligne
cursor1.rotate(90);            // Tourner le curseur de 90 degrés
cursor1.drawSegment(600, 600);    // Dessiner une ligne jusqu'au point (400, 400)
cursor1.drawCircle(50);        // Dessiner un cercle de rayon 50 à la position actuelle
cursor1.drawSquare(100, 50);// Dessiner un rectangle de largeur 100 et hauteur 50

// 11. Appel de fonction
drawCircle(250, 250, 75);

// 12. Fin du script
"""

tokenizer = DrawScriptTokenizer()
tokens, errors = tokenizer.tokenize(code)

parser = DrawScriptParser(tokens)
ast_nodes, parse_errors = parser.parse()

# -- Vérification: si le parseur a retourné des erreurs, on les affiche:
if parse_errors:
    print("=== Erreurs de parsing détectées ===")
    for err in parse_errors:
        # Chaque err est un dict: {"message": str(e), "line": line}
        print(f"Ligne {err['line']}: {err['message']}")
    print("Impossible de poursuivre l'analyse sémantique.")
else:
    print("Aucune erreur de parsing.")
    # Si pas d'erreur de parsing, on effectue l'analyse sémantique
    analyzer = SemanticAnalyzer()
    semantic_errors = analyzer.analyze(ast_nodes)

    if semantic_errors:
        print("=== Erreurs sémantiques détectées ===")
        for err in semantic_errors:
            print(err)
        print("Annulation de la génération du code C.")
    else:
        print("Aucune erreur sémantique, génération du code C en cours.")
        interpreter = DrawScriptDeserializerC(ast_nodes)
        interpreter.write_c()