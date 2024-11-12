## Structure des Dossiers

```
drawPlusPlus/
├── Data/
│   └── Assets/
├── Docs/
├── DrawLibrary/
│   └── Core/
│       ├── Collision/
│       │   └── aabb.py
│       ├── Math/
│       │   └── vector2.py
│       └── Shapes/
│           └── rectangle.py
├── DrawScript/
|       ├── Commands/
|       └── drawScriptParser.py
├── Model/
|       ├── canvasImage.py
|       ├── cursor.py
│       └── selectionRectangle.py
├── View/
|       ├── Resources/
│       │   ├── customText.py
│       │   └── textLineNumbers.py
|       ├── canvas.py
|       ├── mainFrame.py
|       ├── menuBar.py
|       ├── terminal.py
|       ├── textEditor.py
|       ├── toolBar.py
│       └── window.py
├── ViewModel/
|       ├── Tools/
│       │   ├── selectionRectangleTool.py
│       │   └── selectionTool.py
|       ├── canvasViewModel.py
│       └── toolManager.py
├── .gitignore
├── config.py
└── main.py
```
## Racine du Projet
- **main.py** : Point d'entrée principal de l'application.
- **config.py** : Contient les paramètres globaux de configuration.
- **.gitignore** : Fichier listant les éléments à exclure du contrôle de version.

## `Data/`
- **Assets/** : Contient les ressources nécessaires, telles que les images.

## `Docs/`
- Documentation liée au projet (README, manuel utilisateur, tutoriels).

## `DrawLibrary/`
- Librairie principale de dessin.

  - **Core/**
    - **Collision/aabb.py** : Module pour la détection de collisions AABB.
    - **Math/vector2.py** : Module pour les opérations vectorielles en 2D.
    - **Shapes/rectangle.py** : Module pour gérer et dessiner des rectangles.

## `DrawScript/`
- Contient les fichiers pour le langage de script de dessin.

  - **Commands/** : Gestion des commandes *DrawScript*.
  - **drawScriptParser.py** : Analyseur syntaxique pour *DrawScript*.

## `Model/`
- Modules gérant les données et la logique de l’application.

  - **canvasImage.py** : Gestion des images sur le canevas.
  - **cursor.py** : Gestion des positions et mouvements du curseur.
  - **selectionRectangle.py** : Module pour le rectangle de sélection.

## `View/`
- Modules pour l'interface graphique.

  - **Resources/**
    - **customText.py** : Classe de texte personnalisé.
    - **textLineNumbers.py** : Affichage des numéros de ligne dans l'éditeur.
  - **canvas.py** : Interface du canevas de dessin.
  - **mainFrame.py** : Fenêtre principale de l'application.
  - **menuBar.py** : Barre de menu.
  - **terminal.py** : Terminal intégré pour afficher les logs.
  - **textEditor.py** : Éditeur de texte pour *DrawScript*.
  - **toolBar.py** : Barre d'outils.
  - **window.py** : Gestion de la fenêtre de l'application.

## `ViewModel/`
- Connecte le modèle et la vue.

  - **Tools/**
    - **selectionRectangleTool.py** : Outil pour le rectangle de sélection.
    - **selectionTool.py** : Outil de sélection.
  - **canvasViewModel.py** : Gestion du canevas.
  - **toolManager.py** : Gestionnaire des outils de l’application.
