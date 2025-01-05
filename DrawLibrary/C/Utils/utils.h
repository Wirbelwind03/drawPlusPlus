#ifndef UTILS_H
#define UTILS_H

#include <SDL2/SDL.h>

void saveScreenshot(SDL_Renderer *renderer, int screen_width, int screen_height, const char *filename);

void savePartialScreenshot(SDL_Renderer *renderer, const char *filename, int x, int y, int width, int height);

void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a);

int SDL_Start();

SDL_Window* CreateWindow(int screen_width, int screen_height);

SDL_Renderer* CreateRenderer(SDL_Window* window);

#endif