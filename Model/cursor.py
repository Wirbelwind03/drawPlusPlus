import math
import tkinter as tk
from tkinter import filedialog, messagebox

# Cursor class
class Cursor:
    def __init__(self, x=0, y=0, angle=0, visible=True, couleur="black", epaisseur=1):
        self.x = x
        self.y = y
        self.angle = angle  # angle in degree
        self.visible = visible
        self.couleur = couleur
        self.epaisseur = epaisseur

    def set_couleur(self, couleur):
        self.couleur = couleur
        print(f"La couleur du curseur est maintenant {self.couleur}")

    def set_epaisseur(self, epaisseur):
        self.epaisseur = epaisseur
        print(f"L'épaisseur du curseur est maintenant {self.epaisseur}")

    def avancer(self, distance):
        rad = math.radians(self.angle)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
        print(f"Le curseur avance de {distance} pixels à la position ({self.x}, {self.y})")

    def tourner(self, angle):
        self.angle = (self.angle + angle) % 360
        print(f"Le curseur tourne de {angle} degrés. Nouvel angle: {self.angle}")

    def dessiner_segment(self, longueur):
        self.avancer(longueur)
        print(f"Dessine un segment de longueur {longueur} à partir de la position ({round(self.x, 2)}, {round(self.y, 2)})")

    def dessiner_cercle(self, rayon):
        print(f"Dessine un cercle de rayon {rayon} à la position ({self.x}, {self.y})")

    def dessiner_carre(self, cote):
        for _ in range(4):
            self.avancer(cote)
            self.tourner(90)

    def dessiner_point(self):
        print(f"Dessine un point à la position ({round(self.x, 2)}, {round(self.y, 2)})")

    def dessiner_arc(self, rayon, angle_debut, angle_fin):
        print(f"Dessine un arc de rayon {rayon} de l'angle {angle_debut} à {angle_fin}")

def executer_commande(commande, curseur):
    elements = commande.split()
    
    if not elements:
        print("Commande vide.")
        return
    
    action = elements[0]

    try:
        if action == "move" and len(elements) == 2:
            distance = int(elements[1])
            curseur.avancer(distance)
        
        elif action == "rotate" and len(elements) == 2:
            angle = int(elements[1])
            curseur.tourner(angle)
        
        elif action == "line" and len(elements) == 2:
            longueur = int(elements[1])
            curseur.dessiner_segment(longueur)

        elif action == "circle" and len(elements) == 2:
            rayon = int(elements[1])
            curseur.dessiner_cercle(rayon)

        elif action == "square" and len(elements) == 2:
            cote = int(elements[1])
            curseur.dessiner_carre(cote)

        elif action == "point" and len(elements) == 1:
            curseur.dessiner_point()

        elif action == "arc" and len(elements) == 4:
            rayon, angle_debut, angle_fin = map(int, elements[1:])
            curseur.dessiner_arc(rayon, angle_debut, angle_fin)

        else:
            print(f"Commande '{commande}' non reconnue ou mal formée.")
    
    except ValueError:
        print(f"Erreur: paramètres invalides dans la commande '{commande}'.")
