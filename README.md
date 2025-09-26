# draw++ — Langage de dessin & chaîne de compilation

Ce README décrit **le langage draw++** (syntaxe utilisable dès aujourd’hui) et **la chaîne de compilation** telle qu’implémentée dans le repo : **tokenisation → parsing → analyse sémantique → génération C**.

> Les sections ci‑dessous sont **basées sur le code** des modules `drawScriptTokenizer.py`, `drawScriptParser.py`, `drawScriptSemanticAnalyzer.py` et `drawScriptDeserializerC.py` (dossier `DrawScript/Core`).

---

## 🚀 Aperçu

* **Objectif** : écrire des scripts `.dpp` pour décrire des formes et opérations 2D (cercles, rectangles, segments, triangles…), puis **générer du C** qui s’appuie sur la bibliothèque de dessin du projet. Les rendus sont sauvegardés en BMP dans `Data/Outputs/`.
* **Pipeline** :

  1. **Tokenisation** (régex) des mots‑clés, identifiants, nombres, chaînes, booléens, opérateurs.
  2. **Parsing** en AST : instructions (`var`, `if/for/while/do…while`, `function`, `return`, `copy`, `animate`, **cursors**).
  3. **Analyse sémantique** : variables/curseurs déclarés, arités des fonctions et méthodes connues via des symboles globaux.
  4. **Désérialisation → C** : production d’un `main.c` (à partir d’un gabarit `body.c`) + `globals.h` puis compilation.

---

## 📦 Prérequis (build rapide)

* **Toolchain C** (gcc/clang, C17 recommandé).
* **Python 3.10+** (exécution du pipeline).

## 🧩 Langage draw++ (syntaxe)

### Lexèmes & délimiteurs

* **Commentaires** : `// ...` (ligne) et `/* ... */` (bloc)
* **Nombres** : entiers & flottants (`-12`, `3.14`, `.5`)
* **Chaînes** : `"..."` (une seule ligne)
* **Booléens** : `true`, `false`
* **Identifiants** : `[A-Za-z_][A-Za-z0-9_]*`
* **Opérateurs** : `+  -  *  /  %  ==  !=  <=  >=  <  >  &&  ||  !`
* **Affectation** : `=`
* **Accès objet** : `.` (ex. `c.move(10, 0);`)
* **Délimiteurs** : `()  {}  ;  ,  :`

### Mots‑clés

`var`, `function`, `return`, `if`, `else`, `for`, `while`, `do`, `copy`, `to`, `animate`, `Cursor`

### Déclarations & types implicites

```drawpp
var x = 10;          // type déduit → int
var y = 3.14;        // type déduit → float
var ok = true;       // type déduit → bool

// Annotation facultative (nom de type libre côté grammaire)
var r: float = 25.0;
```

> Le parseur déduit `int/float/bool` à partir de l’expression d’initialisation ; sinon, le type peut rester vide et sera décidé côté génération C.

### Expressions (précédence)

Parenthèses `()` > unaire `! + -` > multiplicatif `* / %` > additif `+ -` > relationnel `< <= > >=` > égalité `== !=` > logique `&&` > logique `||`.

Appels de fonction : `ident(expr, expr, ...)`.

### Contrôle de flux

```drawpp
if (x > 0) { ... } else { ... }

for (var i = 0; i < 10; i = i + 1) { ... }

while (cond) { ... }

do { ... } while (cond);

function foo() { /* corps */ }
return 42;  // dans une fonction
```

### Cursors (objet "tortue")

Déclarer & initialiser :

```drawpp
Cursor c = Cursor(100, 200);
```

Méthodes disponibles (selon le backend) :

```drawpp
c.move(dx, dy);
c.rotate(angleDegrees);

c.drawCircle(radius);
c.drawFilledCircle(radius);
c.drawEllipse(rx, ry);
c.drawFilledEllipse(rx, ry);
c.drawRectangle(width, height);
c.drawRoundedRectangle(width, height, radius);
c.drawBox(w, h);
c.drawRoundedBox(w, h, radius);
c.drawSegment(length);
c.drawTriangle(x0, y0, x1, y1);

// Couleur courante RGBA (0–255) ; si >255, valeur inversée (255 - v)
c.setRGBA(r, g, b, a);
```

### Primitives sous forme d’appels "libres"

En plus des méthodes de curseur, des fonctions globales sont prévues :

```drawpp
drawCircle(x, y, radius);
drawFilledCircle(x, y, radius);
drawEllipse(x, y, rx, ry);
drawFilledEllipse(x, y, rx, ry);
drawRectangle(x, y, w, h);
drawRoundedRectangle(x, y, w, h, radius);
drawBox(x, y, w, h);
drawRoundedBox(x, y, w, h, radius);
drawSegment(x0, y0, x1, y1);
drawTriangle(x0, y0, x1, y1, x2, y2);

setRGBA(r, g, b, a); // fixe la couleur courante pour les primitives suivantes
```

### Instructions spécialisées

```drawpp
// Copier une zone source (x0, y0, x1, y1) vers une destination (x, y)
copy(x0, y0, x1, y1) to (x, y);

// Animer un objet / une propriété pendant une durée
animate(targetExpr, durationOrValue) {
  // bloc d’instructions animé
}
```

---

## 🧪 Exemple complet

```drawpp
// Hello draw++
var cx = 320; var cy = 240; var r = 80;

setRGBA(52, 152, 219, 255);      // bleu

drawFilledCircle(cx, cy, r);     // disque plein

drawRectangle(cx - 120, cy - 90, 240, 180); // rectangle autour

Cursor c = Cursor(cx, cy);
c.setRGBA(231, 76, 60, 255);      // rouge
c.drawSegment(140);               // segment depuis la position du curseur
c.rotate(120); c.drawSegment(140);
c.rotate(120); c.drawSegment(140);
```

---

## 🛠️ Chaîne de compilation (vue d’ensemble)

1. **Tokenisation** : production d’une liste de tokens (`NUMBER`, `STRING`, `BOOLEAN`, `IDENTIFIER`, `OPERATOR`, `DELIMITER`, `ASSIGN`, `ACCESS_OPERATOR`, etc.).
2. **Parsing** : transformation en **AST** (nœuds : `var_declaration`, `if_statement`, `for_statement`, `while_statement`, `do_while_statement`, `function_declaration`, `return_statement`, `copy_statement`, `animate_statement`, `cursor_declaration`, `cursor_method`, `expression_statement`, expressions binaires/unaires/appels, etc.).
3. **Analyse sémantique** : vérifie déclarations, types de symboles (`variable`, `cursor`, `function`), existence/arité des fonctions globales et méthodes de curseur.
4. **Génération C** :

   * Création/maj de `DrawLibrary/C/Utils/globals.h` (dimensions fenêtre).
   * Lecture de `body.c` → insertion des **déclarations** puis des **instructions** à la place de `// INSERT VARIABLES` et `// INSERT DRAWINGS`.
   * Écriture de `main.c` final.

Les appels graphiques connus (`drawCircle`, `drawRectangle`, `drawTriangle`, …) sont émis avec un petit boilerplate qui **sauvegarde chaque rendu** dans `Data/Outputs/drawing_<n>.bmp` et journalise des coordonnées (fichier ouvert côté gabarit).

> Les méthodes de `Cursor` génèrent des appels `Cursor_*` équivalents (ex. `Cursor_DrawCircle`). La couleur courante est gérée via `setRGBA` côté générateur.

---

## ▶️ Utilisation (exécution & build)

> Exécutez `main.py` avec la commande : `python main.py`

---

## 🧰 Débogage

* **Trace tokens** / **AST** : activez votre drapeau DEBUG ou ajoutez des prints.
* **Erreurs parseur** : messages avec la **ligne** et un **texte explicite** (attendu/reçu).
* **Analyse sémantique** : messages typiques `Undeclared variable …`, arités incorrectes (`expects N argument(s)`).
