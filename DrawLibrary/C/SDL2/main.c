#include <SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "utils.h"
#include "shapes.h"

// Constantes globales
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

int main(int argc, char *argv[]) {
    // Initialisation de SDL
    SDL_Start();
    SDL_Window *window = CreateWindow();
    SDL_Renderer *renderer = CreateRenderer(window);

    // Variables principales
    int centerX = 400, centerY = 400, radius = 50, numCircles = 5;
    double angle = 0, speed = 0.05;
    bool running = true;
    SDL_Event event;

    // Dessin initial
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

    for (int i = 0; i < numCircles; i++) {
        double offsetAngle = angle + (i * (360.0 / numCircles));
        int offsetX = centerX + (radius * 3) * cos(offsetAngle);
        int offsetY = centerY + (radius * 3) * sin(offsetAngle);
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Noir
        drawCircle(renderer, offsetX, offsetY, radius);
    }

    for (int gridX = 0; gridX <= SCREEN_WIDTH; gridX += 50) {
        for (int gridY = 0; gridY <= SCREEN_HEIGHT; gridY += 50) {
            SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255); // Bleu
            drawCircle(renderer, gridX, gridY, 5);
        }
    }

    SDL_RenderPresent(renderer);

    // Sauvegarder une capture d'écran
    saveScreenshot(renderer, "screenshot.bmp");

    // Boucle principale
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        SDL_Delay(16);
    }

    // Nettoyage
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
