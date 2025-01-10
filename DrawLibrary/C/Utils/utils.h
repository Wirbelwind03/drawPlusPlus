#ifndef UTILS_H
#define UTILS_H

#include <SDL2/SDL.h>

int SDL_Start();

SDL_Window* CreateWindow(int screen_width, int screen_height);

SDL_Renderer* CreateRenderer(SDL_Window* window);

SDL_Surface* CreateSurface(int width, int height);

SDL_Texture* CreateTexture(SDL_Renderer* renderer, SDL_Surface* surface);

void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a);

#endif