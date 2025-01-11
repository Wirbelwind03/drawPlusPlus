#ifndef UTILS_H
#define UTILS_H

#include <SDL2/SDL.h>

int SDL_Start();

SDL_Window* CreateWindow(int screen_width, int screen_height);

SDL_Renderer* CreateRenderer(SDL_Window* window);

SDL_Surface* CreateSurface(int width, int height);

SDL_Surface* RotateSurface(SDL_Surface* surface, int angle);

int CopyRenderToSurface(SDL_Renderer* renderer, SDL_Rect rect, SDL_Surface* surface);

SDL_Texture* CreateTexture(SDL_Renderer* renderer, SDL_Surface* surface);

int SaveBMP(SDL_Surface* surface, char* filename);

int SaveDrawing(SDL_Renderer* renderer, SDL_Rect captureRect, int angle, char* filename);

void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a);

// Function to ensure the capture rectangle is within valid bounds
void AdjustCaptureRect(SDL_Rect* captureRect);

#endif