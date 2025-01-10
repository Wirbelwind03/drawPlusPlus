#include <stdio.h>
#include "utils.h"

int SDL_Start(){
    // Initialisation de SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur SDL_Init : %s\n", SDL_GetError());
        return 1;
    }
    return 0;
}

SDL_Window* CreateWindow(int screen_width, int screen_height){
    SDL_Window *window = SDL_CreateWindow(
    "Exemple SDL2", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, screen_width, screen_height, SDL_WINDOW_HIDDEN);
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

SDL_Surface* CreateSurface(int width, int height){
    // Create an empty surface to draw on
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, SDL_PIXELFORMAT_RGBA32);
    if (!surface) {
        SDL_Log("Unable to create surface! SDL_Error: %s", SDL_GetError());
        SDL_Quit();
        return NULL;
    }
    return surface;
}

SDL_Texture* CreateTexture(SDL_Renderer* renderer, SDL_Surface* surface){
        // Create a texture from the surface
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        SDL_Log("Unable to create texture! SDL_Error: %s", SDL_GetError());
        SDL_FreeSurface(surface);
        SDL_Quit();
        return NULL;
    }
    return texture;
}

void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a){
    SDL_SetRenderDrawColor(renderer, r, g, b, a);
    SDL_RenderClear(renderer);
}