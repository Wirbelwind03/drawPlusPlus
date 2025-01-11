#ifndef SHAPES_H
#define SHAPES_H

#include <SDL2/SDL.h>

void drawCircle(SDL_Renderer *renderer, int x, int y, int radius, int r, int g, int b, int a, char* filename);

void drawSegment(SDL_Renderer *renderer, int x0, int y0, int x1, int y1, int thickness, int r, int g, int b, int a, char* filename);

void drawRectangle(SDL_Renderer *renderer, int x, int y, int width, int height, int angle, int r, int g, int b, int a, char* filename);

#endif