#ifndef UTILS_H
#define UTILS_H

#include <SDL2/SDL.h>

void saveScreenshot(SDL_Renderer *renderer, const char *filename);

int SDL_Start();

SDL_Window* CreateWindow();

SDL_Renderer* CreateRenderer(SDL_Window* window);

#endif