#include <DrawLibrary/C/SDL2/src/include/SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

// Constantes globales
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

// https://en.wikipedia.org/w/index.php?title=Midpoint_circle_algorithm&oldid=889172082#C_example
void drawCircle(SDL_Renderer *renderer, int x0, int y0, int radius)
{
    int x = radius-1;
    int y = 0;
    int dx = 1;
    int dy = 1;
    int err = dx - (radius << 1);

    while (x >= y)
    {
        SDL_RenderDrawPoint(renderer, x0 + x, y0 + y);
        SDL_RenderDrawPoint(renderer, x0 + y, y0 + x);
        SDL_RenderDrawPoint(renderer, x0 - y, y0 + x);
        SDL_RenderDrawPoint(renderer, x0 - x, y0 + y);
        SDL_RenderDrawPoint(renderer, x0 - x, y0 - y);
        SDL_RenderDrawPoint(renderer, x0 - y, y0 - x);
        SDL_RenderDrawPoint(renderer, x0 + y, y0 - x);
        SDL_RenderDrawPoint(renderer, x0 + x, y0 - y);

        if (err <= 0)
        {
            y++;
            err += dy;
            dy += 2;
        }
        
        if (err > 0)
        {
            x--;
            dx += 2;
            err += dx - (radius << 1);
        }
    }
}

// Fonction pour dessiner une étoile (approximée avec lignes)
void drawStar(SDL_Renderer *renderer, int x, int y, int size) {
    double angleStep = M_PI / 5; // 5 branches, 2 points par branche
    for (int i = 0; i < 10; i++) {
        double angle1 = i * angleStep;
        double angle2 = (i + 2) * angleStep; // Relier à un point distant
        int x1 = x + cos(angle1) * (i % 2 == 0 ? size : size / 2);
        int y1 = y + sin(angle1) * (i % 2 == 0 ? size : size / 2);
        int x2 = x + cos(angle2) * (i % 2 == 0 ? size : size / 2);
        int y2 = y + sin(angle2) * (i % 2 == 0 ? size : size / 2);
        SDL_RenderDrawLine(renderer, x1, y1, x2, y2);
    }
}

int main(int argc, char *argv[]) {
    // Initialisation de SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur SDL_Init : %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow(
        "Exemple SDL2", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur SDL_CreateWindow : %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Erreur SDL_CreateRenderer : %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Variables principales
    int centerX = 400, centerY = 400, radius = 50, numCircles = 5;
    double angle = 0, speed = 0.05;
    bool isAnimating = true;

    // Boucle principale
    bool running = true;
    SDL_Event event;

    while (running) {
        // Gestion des événements
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        // Nettoyage de l'écran
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Noir
        SDL_RenderClear(renderer);

        // Dessiner plusieurs cercles
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Blanc
        for (int i = 0; i < numCircles; i++) {
            double offsetAngle = angle + (i * (360.0 / numCircles));
            int offsetX = centerX + (radius * 3) * cos(offsetAngle);
            int offsetY = centerY + (radius * 3) * sin(offsetAngle);
            drawCircle(renderer, offsetX, offsetY, radius);
        }

        // Animation de l'étoile
        if (isAnimating) {
            angle += speed;
            int starX = centerX + (radius * 4) * cos(angle);
            int starY = centerY + (radius * 4) * sin(angle);
            drawStar(renderer, starX, starY, radius);
            if (angle >= 2 * M_PI) {
                angle = 0; // Réinitialiser
                isAnimating = false;
            }
        }

        // Dessiner une conditionnelle
        if (radius > 40 && numCircles >= 5) {
            SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255); // Vert
            SDL_Rect rect = {centerX - radius, centerY - radius, radius * 2, radius * 2};
            SDL_RenderFillRect(renderer, &rect);
        } else {
            SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Rouge
            SDL_RenderDrawLine(renderer, centerX - radius, centerY, centerX + radius, centerY);
            SDL_RenderDrawLine(renderer, centerX, centerY - radius, centerX, centerY + radius);
        }

        // Afficher la grille
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255); // Bleu
        for (int gridX = 0; gridX <= SCREEN_WIDTH; gridX += 50) {
            for (int gridY = 0; gridY <= SCREEN_HEIGHT; gridY += 50) {
                drawCircle(renderer, gridX, gridY, 5);
            }
        }

        // Mettre à jour l'écran
        SDL_RenderPresent(renderer);

        // Petite pause pour limiter la vitesse
        SDL_Delay(16);
    }

    // Nettoyage
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}

