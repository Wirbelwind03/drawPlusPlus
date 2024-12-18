# Rectangle

```python
class DrawLibrary.Core.Shapes.Rectangle
```
Cet object crée un rectangle dont le point d'origine se trouve en haut à gauche

## Attributs
```python
self.x: int
```
Représente l'abscisse du rectangle.
```python
self.y: int
```
Représente l'ordonnée du rectangle.
```python
self.width : int
```
Représente la longueur du rectangle.
```python
self.height : int
```
Représente la largeur du rectangle.

## Propriétés

### x
- Getter
```python
def x(self) -> int
```
Retourne l'abscisse du rectangle.
- Setter
```python
def x(self, newValue: int) -> None
```
Met à jour la valeur pour l'abscisse du rectangle.<br>
Quand elle est changé, elle bouge le rectangle entier sur l'abscisse<br>
Sa valeur ne peut pas être < 0 vu que la librarie est conçue pour un canvas tkinter (dont les coordonnées négatives n'existent pas)<br>
**PARAMETERS:**<br>
newValue (int) - La nouvelle valeur à mettre pour l'abscisse du rectangle

### y
- Getter
```python
def y(self) -> int
```
Retourne l'abscisse du rectangle.
- Setter
```python
def y(self, newValue: int) -> None
```
Met à jour la valeur pour l'ordonnée du rectangle.<br>
Quand elle est changé, elle bouge le rectangle entier sur l'ordonnée<br>
Sa valeur ne peut pas être < 0 vu que la librarie est conçue pour un canvas tkinter (dont les coordonnées négatives n'existent pas)<br>
**PARAMETERS:**<br>
newValue (int) - La nouvelle valeur à mettre pour l'ordonnée du rectangle

### width
- Getter
```python
def width(self) -> int
```
Retourne la longueur du rectangle.
- Setter
```python
def width(self, newValue: int) -> None
```
Met à jour la valeur pour la longueur du rectangle.<br>
Sa valeur ne peut pas être < 0, si elle l'est, cela retourne une erreur.<br>
**PARAMETERS:**<br>
newValue (int) - La nouvelle valeur à mettre pour la longueur du rectangle

### height
- Getter
```python
def height(self) -> int
```
Retourne la largeur du rectangle.
- Setter
```python
def height(self, newValue: int) -> None
```
Met à jour la valeur pour la largeur du rectangle.<br>
Sa valeur ne peut pas être < 0, si elle l'est, cela retourne une erreur.<br>
**PARAMETERS:**<br>
newValue (int) - La nouvelle valeur à mettre pour la largeur du rectangle

### left
- Getter
```python
def left(self) -> int
```
Retourne la coordonnée gauche du rectangle.
- Setter
```python
def left(self, value: int) -> None
```
Met à jour la valeur du coordonnée gauche du rectangle. <br>
Quand elle est changée, elle met à jour la longueur du rectagnle. <br>
Si elle dépasse la coordonnée de celle de droite, sa valeur sera fixée à celui ci <br>
**PARAMETERS:**<br>
value (int) - La nouvelle valeur à mettre pour la coordonnée gauche du rectangle

### right
- Getter
```python
def right(self) -> int
```
Retourne la coordonnée droite du rectangle.
- Setter
```python
def right(self, value: int) -> None
```
Met à jour la valeur du coordonnée droite du rectangle. <br>
Quand elle est changée, elle met à jour la longueur du rectagnle. <br>
Si elle dépasse la coordonnée de celle de gauche, sa valeur sera fixée à celui ci <br>
**PARAMETERS:**<br>
value (int) - La nouvelle valeur à mettre pour la coordonnée droite du rectangle

### top
- Getter
```python
def top(self) -> int
```
Retourne la coordonnée haut du rectangle.
- Setter
```python
def top(self, value: int) -> None
```
Met à jour la valeur du coordonnée haut du rectangle. <br>
Quand elle est changée, elle met à jour la largeur du rectagnle. <br>
Si elle dépasse la coordonnée de celle du bas, sa valeur sera fixée à celui ci <br>
**PARAMETERS:**<br>
value (int) - La nouvelle valeur à mettre pour la coordonnée haut du rectangle


### bottom
- Getter
```python
def bottom(self) -> int
```
Retourne la coordonnée bas du rectangle.
- Setter
```python
def bottom(self, value: int) -> None
```
Met à jour la valeur du coordonnée bas du rectangle. <br>
Quand elle est changée, elle met à jour la largeur du rectagnle. <br>
Si elle dépasse la coordonnée de celle du haut, sa valeur sera fixée à celui ci <br>
**PARAMETERS:**<br>
value (int) - La nouvelle valeur à mettre pour la coordonnée bas du rectangle

### center
- Getter
```python
def center(self) -> int
```
Retourne le centre du rectangle.

### topLeft
- Getter
```python
def topLeft(self) -> Vector2
```
Retourne les coordonnées du coté en haut à gauche du rectangle.
- Setter
```python
def topLeft(self, value: Vector2) -> None
```
Met à jour les coordonnées du coté en haut à gauche du rectangle.
Cela met à jour les propriétés **top** et **left**

### topRight
- Getter
```python
def topRight(self) -> Vector2
```
Retourne les coordonnées du coté en haut à droite du rectangle.<br>
- Setter
```python
def topRight(self, value: Vector2) -> None
```
Met à jour les coordonnées du coté en haut à droite du rectangle.<br>
Cela met à jour les propriétés **top** et **right**

### bottomLeft
- Getter
```python
def bottomLeft(self) -> Vector2
```
Retourne les coordonnées du coté en bas à gauche du rectangle.<br>
- Setter
```python
def bottomLeft(self, value: Vector2) -> None
```
Met à jour les coordonnées du coté en bas à gauche du rectangle.<br>
Cela met à jour les propriétés **bottom** et **left**

### bottomRight
- Getter
```python
def bottomRight(self) -> Vector2
```
Retourne les coordonnées du coté en bas à droite du rectangle.<br>
- Setter
```python
def bottomRight(self, value: Vector2) -> None
```
Met à jour les coordonnées du coté en bas à droite du rectangle.<br>
Cela met à jour les propriétés **bottom** et **right**
