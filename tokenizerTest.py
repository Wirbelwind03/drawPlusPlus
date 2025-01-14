import os, subprocess

from DrawScript.Core.drawScriptTokenizer import DrawScriptTokenizer
from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Core.drawScriptSemanticAnalyzer import SemanticAnalyzer
from DrawScript.Core.drawScriptDeserializerC import DrawScriptDeserializerC

from DrawLibrary.Graphics.canvasImage import CanvasImage


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

// 11. Appel de fonction
drawCircle(250, 250, 75);

// 2. Déclaration d'une variable de type cursor
Cursor cursor1 = Cursor(centerX, centerY);

// 10. Utilisation du curseur pour dessiner une forme géométrique
cursor1.move(400, 300);      // Déplacer le curseur en traçant une ligne
cursor1.rotate(90);            // Tourner le curseur de 90 degrés
cursor1.drawSegment(600);    // Dessiner une ligne qui fait 600 de longueur
cursor1.drawCircle(50);        // Dessiner un cercle de rayon 50 à la position actuelle
cursor1.drawRectangle(100, 50);// Dessiner un rectangle de largeur 100 et hauteur 50

// 12. Fin du script
var dox = 10;
var doy = 20;
var x = 0;
do {
    x = x + 1;
} while (x < 10);
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

        # Get the directory where the code is ran
        current_directory = os.getcwd()

        gcc_command = [
            "gcc",
            f"-I{current_directory}/DrawLibrary/C/SDL2/src/include",
            f"-I{current_directory}/DrawLibrary/C/SDL2_gfx",
            f"-I{current_directory}/DrawLibrary/C/Utils",
            f"{current_directory}/DrawLibrary/C/Utils/shapes.c",
            f"{current_directory}/DrawLibrary/C/Utils/cursor.c",
            f"{current_directory}/DrawLibrary/C/Utils/utils.c",
            f"{current_directory}/main.c",
            f"{current_directory}/DrawLibrary/C/SDL2_gfx/SDL2_gfxPrimitives.c",
            f"{current_directory}/DrawLibrary/C/SDL2_gfx/SDL2_rotozoom.c",
            f"-L{current_directory}/DrawLibrary/C/SDL2/src/lib",
            "-lmingw32",
            "-lSDL2main",
            "-lSDL2",
            f"-o{current_directory}/DrawLibrary/C/SDL2/main.exe",
        ]

        # Compile the C code
        try:
            subprocess.run(gcc_command, check=True)
            print("Build successful!")
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")

        output_folder = f'{current_directory}/Data/Outputs'
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path) and filename != ".gitignore":
                os.remove(file_path)

        # Run the C code
        try:
            subprocess.run(f"{current_directory}/DrawLibrary/C/SDL2/main.exe", check=True)  # This will run the exe and wait for it to finish
            print(f"Successfully launched {current_directory}/DrawLibrary/C/SDL2/main.exe")
        except subprocess.CalledProcessError as e:
            print(f"Failed to launch {current_directory}/DrawLibrary/C/SDL2/main.exe: {e}")

        with open(f'{current_directory}/Data/Outputs/drawing_positions.txt', "r") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            x, y = line.strip().split(',')
