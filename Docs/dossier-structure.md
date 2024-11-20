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
- Le répertoire `ViewModel` agit comme un pont entre les données du modèle et la présentation visuelle dans la vue. Il gère la logique permettant d’assurer que les modifications apportées aux données sont reflétées dans l’interface utilisateur, et inversement.

  - **Tools/**
    - **selectionRectangleTool.py** : Implémente un outil dédié à la création et la gestion d’un rectangle de sélection. Permet à l’utilisateur de délimiter une zone spécifique à l’aide d’un clic-glissé.
    - **selectionTool.py** : Un outil générique de sélection permettant de sélectionner des éléments individuels dans une interface.
  - **canvasViewModel.py** : Responsable de la gestion du canevas. Ce fichier gère les interactions entre la vue du canevas (ex : zoom, translation, redimensionnement) et les données sous-jacentes.
  - **selectionRectangleCanvasViewModel** : Gère spécifiquement les interactions avec l’outil rectangle de sélection sur le canevas. Cela inclut la création, la mise à jour et la suppression des rectangles visibles dans l’interface utilisateur.
  - **toolManager.py** : Fonctionne comme un gestionnaire centralisé pour les outils de l’application. Il est chargé d’activer, de désactiver et de gérer les interactions entre les différents outils définis, tels que ceux présents dans le répertoire `Tools/`.
