#include <stdio.h>
#include <SDL2_rotozoom.h>

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
        return NULL;
    }
    return surface;
}

int CopyRenderToSurface(SDL_Renderer* renderer, SDL_Rect rect, SDL_Surface* surface) {
    // Copy the rendered content to the surface
    if (SDL_RenderReadPixels(renderer, &rect, SDL_PIXELFORMAT_RGBA32, surface->pixels, surface->pitch) != 0) {
        printf("Failed to read pixels: %s\n", SDL_GetError());
        SDL_FreeSurface(surface);
        return 1;
    }
    return 0;
}

SDL_Surface* RotateSurface(SDL_Surface* surface, int angle) {
    SDL_Surface *rotatedSurface = rotozoomSurface(surface, angle, 1.0, 1);
    if (!rotatedSurface) {
        printf("Failed to rotate surface.\n");
        SDL_FreeSurface(surface);
        return NULL;
    }
    return rotatedSurface;
}

SDL_Texture* CreateTexture(SDL_Renderer* renderer, SDL_Surface* surface){
        // Create a texture from the surface
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        SDL_Log("Unable to create texture! SDL_Error: %s", SDL_GetError());
        SDL_FreeSurface(surface);
        return NULL;
    }
    return texture;
}

int SaveBMP(SDL_Surface* surface, char* filename){
    if (SDL_SaveBMP(surface, filename) != 0) {
        printf("Failed to save BMP: %s\n", SDL_GetError());
        return 1;
    }
    return 0;
}

int SaveDrawing(SDL_Renderer* renderer, SDL_Rect captureRect, int angle, char* filename) {
    // Capture the current content of the renderer into an SDL_Surface
    SDL_Surface *surface = CreateSurface(captureRect.w, captureRect.h);
    // Copy the rendered content to the surface
    if (CopyRenderToSurface(renderer, captureRect, surface) != 0){
        return 1;
    }
    // Rotate the surface
    SDL_Surface *rotatedSurface = RotateSurface(surface, angle);
    // Save the rotated surface as a BMP file
    if (SaveBMP(rotatedSurface, filename) != 0){
        return 1;
    }
    // Clean up
    SDL_FreeSurface(surface);
    SDL_FreeSurface(rotatedSurface);
    // Clean the window
    ClearCanvas(renderer, 255, 255, 255, 255);

    return 0;
}

void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a){
    SDL_SetRenderDrawColor(renderer, r, g, b, a);
    SDL_RenderClear(renderer);
}