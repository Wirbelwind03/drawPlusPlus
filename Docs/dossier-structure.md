## Structure des Dossiers

```
drawPlusPlus/
├── Controller/
│   ├── Tools/
│   │   ├── selectionRectangleTool.py
│   │   └── selectionTool.py
│   ├── canvasController.py
│   ├── mainController.py
│   ├── menuBarController.py
│   ├── scriptEditorController.py
│   └── selectionRectangleCanvasController.py
├── Data/
│   └── Assets/
├── Docs/
│   ├── dossier-structure.md
│   └── SujetPython_GI_2024.pdf
├── DrawLibrary/
│   ├── Core/
│   │   ├── Collision/
│   │   │   └── aabb.py
│   │   ├── Math/
│   │   │   └── vector2.py
│   │   └── Shapes/
│   │       └── rectangle.py
│   └── Graphics/
│       ├── canvasEntity.py
│       └── canvasImage.py
├── DrawScript/
│   ├── Commands/
│   │   ├── baseCommand.py
│   │   ├── cursorCommand.py
│   │   ├── drawCommand.py
│   │   └── moveCommand.py
│   └── Core/
│       ├── drawScriptParser.py
│       └── drawScriptTokenizer.py
├── Model/
│   ├── canvasEntities.py
│   ├── cursor.py
│   ├── selectionRectangle.py
│   └── toolManager.py
├── View/
│   ├── Resources/
│   │   └── Widgets/
│   │       ├── terminal.py
│   │       ├── textEditor.py
│   │       └── toolBar.py
│   ├── mainFrame.py
│   └── window.py
├── .gitignore
├── config.py
└── main.py
```
## Racine du projet
- `main.py` : Point d'entrée principal de l'application.
- `config.py` : Configuration globale du projet.
- `.gitignore` : Fichiers ignorés par Git.

## `Controller/`
Ce module gère les interactions utilisateur et la logique principale de l'application.
- **Tools/** : Contient les outils de sélection (ex. : `selectionRectangleTool.py`, `selectionTool.py`).
- `canvasController.py` : Contrôle principal du canevas.
- `mainController` : Gère les fonctionnalités générales.
- `selectionRectangleCanvasController.py` : Contrôle de la sélection rectangulaire.

## `Data/`
- **Assets/** : Stocke les ressources nécessaires au projet.

## `Docs/`
- `dossier-structure.md` : Documentation sur la structure du projet.
- `SujetPython_GI_2024.pdf` : Document décrivant le sujet ou le contexte du projet.

## `DrawLibrary/`
Bibliothèque principale pour les opérations graphiques et mathématiques :
- **Core/** :
  - **Collision/aabb.py** : Gestion des collisions à l'aide des boîtes englobantes alignées sur les axes (AABB).
  - **Math/vector2.py** : Gestion des opérations mathématiques sur les vecteurs 2D.
  - **Shapes/rectangle.py** : Modélisation des rectangles.
- **Graphics/canvasImage.py** : Gestion des images sur le canevas.

## `DrawScript/`
Module pour la gestion et le parsing de scripts de dessin.
- **Commands/** : Contient les commandes de dessin (à compléter).
- **Core/drawScriptParser.py** : Analyse et interprétation des scripts de dessin.

## `Model/`
Représentation des données du projet :
- `canvasImages.py` : Gestion des images sur le canevas.
- `cursor.py` : Modélisation du curseur.
- `selectionRectangle.py` : Gestion des rectangles de sélection.

## `View/`
Interface utilisateur et composants graphiques.
- **Resources/Widgets/** : Composants d'interface tels que la barre de menu (`menuBar.py`), le terminal (`terminal.py`), l'éditeur de texte (`textEditor.py`), et la barre d'outils (`toolBar.py`).
- `mainFrame.py` : Gestion du cadre principal de l'application.
- `window.py` : Fenêtre principale de l'application.
