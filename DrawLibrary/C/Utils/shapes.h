#ifndef SHAPES_H
#define SHAPES_H

#include <SDL2/SDL.h>

void drawCircle(SDL_Renderer *renderer, 
                int x, int y, 
                int radius, 
                int r, int g, int b, int a, 
                char *filename);

void drawFilledCircle(SDL_Renderer *renderer, 
                      int x, int y, 
                      int radius, 
                      int r, int g, int b, int a, 
                      char *filename);

void drawEllipse(SDL_Renderer *renderer, 
                 int x, int y, 
                 int rx, int ry, 
                 int angle, 
                 int r, int g, int b, int a, 
                 char *filename);

void drawFilledEllipse(SDL_Renderer *renderer, 
                       int x, int y, 
                       int rx, int ry, 
                       int angle, 
                       int r, int g, int b, int a, 
                       char *filename);

void drawSegment(SDL_Renderer *renderer, 
                 int x0, int y0, int x1, int y1, 
                 int thickness, 
                 int r, int g, int b, int a, 
                 char *filename);

void drawRectangle(SDL_Renderer *renderer, 
                   int x, int y, 
                   int width, int height, 
                   int angle, 
                   int r, int g, int b, int a, 
                   char *filename);

void drawTriangle(SDL_Renderer *renderer, 
                  int x1, int y1, int x2, int y2, int x3, int y3, 
                  int angle, 
                  int r, int g, int b, int a, 
                  char *filename);

void drawRoundedRectangle(SDL_Renderer *renderer, 
                          int x, int y, 
                          int width, int height, 
                          int radius, 
                          int angle, 
                          int r, int g, int b, int a, 
                          char *filename);

void drawBox(SDL_Renderer *renderer, 
             int x, int y, 
             int width, int height, 
             int angle, 
             int r, int g, int b, int a, 
             char *filename);

void drawRoundedBox(SDL_Renderer *renderer, 
                    int x, int y, 
                    int width, int height, 
                    int radius, 
                    int angle, 
                    int r, int g, int b, int a, 
                    char *filename);

#endif