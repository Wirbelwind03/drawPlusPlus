#include <stdio.h>
#include "utils.h"

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

int SDL_Start(){
    // Initialisation de SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur SDL_Init : %s\n", SDL_GetError());
        return 1;
    }
    return 0;
}

SDL_Window* CreateWindow(){
    SDL_Window *window = SDL_CreateWindow(
    "Exemple SDL2", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur SDL_CreateWindow : %s\n", SDL_GetError());
        SDL_Quit();
        return NULL;
    }
    return window;
}

SDL_Renderer* CreateRenderer(SDL_Window* window){
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Erreur SDL_CreateRenderer : %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return NULL;
    }
    return renderer;
}

// Fonction pour capturer et sauvegarder l'écran comme une image
void saveScreenshot(SDL_Renderer *renderer, const char *filename) {
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, SCREEN_WIDTH, SCREEN_HEIGHT, 32, SDL_PIXELFORMAT_RGBA32);
    if (!surface) {
        printf("Erreur SDL_CreateRGBSurfaceWithFormat: %s\n", SDL_GetError());
        return;
    }

    // Lire les pixels de l'écran
    if (SDL_RenderReadPixels(renderer, NULL, surface->format->format, surface->pixels, surface->pitch) != 0) {
        printf("Erreur SDL_RenderReadPixels: %s\n", SDL_GetError());
        SDL_FreeSurface(surface);
        return;
    }

    // Sauvegarder l'image
    if (SDL_SaveBMP(surface, filename) != 0) {
        printf("Erreur SDL_SaveBMP: %s\n", SDL_GetError());
    } else {
        printf("Image sauvegardée dans le fichier : %s\n", filename);
    }

    SDL_FreeSurface(surface);
}