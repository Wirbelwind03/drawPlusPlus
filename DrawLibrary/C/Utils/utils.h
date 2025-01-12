#ifndef UTILS_H
#define UTILS_H

#include <SDL2/SDL.h>

// Start SDL
int SDL_Start();

// Create a window given the width and height
SDL_Window* CreateWindow(int screen_width, int screen_height);

// Create a renderer, where the drawings will be rendered
SDL_Renderer* CreateRenderer(SDL_Window* window);

// Create a surface with a given width and height
SDL_Surface* CreateSurface(int width, int height);

// Rotate a surface with angle given
SDL_Surface* RotateSurface(SDL_Surface* surface, int angle);

// Copy a render to a surface
int CopyRenderToSurface(SDL_Renderer* renderer, SDL_Rect rect, SDL_Surface* surface);

// Create a SDL texture from a renderer and a surface
SDL_Texture* CreateTexture(SDL_Renderer* renderer, SDL_Surface* surface);

// Save the surface as BMP, and write it given the filename
int SaveBMP(SDL_Surface* surface, char* filename);

// Save a drawing present on the renderer
int SaveDrawing(SDL_Renderer* renderer, SDL_Rect captureRect, int angle, char* filename);

// Clear the canvas, and recolor it with the color given
void ClearCanvas(SDL_Renderer *renderer, int r, int g, int b, int a);

// Function to ensure the capture rectangle is within valid bounds
void AdjustCaptureRect(SDL_Rect* captureRect);

#endif