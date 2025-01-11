#ifndef CURSOR_H
#define CURSOR_H

#include <SDL2/SDL.h>

typedef struct {
    int x;
    int y;
    int angle;
    int thickness;
    int rgba[4];
} Cursor;

Cursor* Cursor_Constructor();

void Cursor_Move(Cursor* cursor, int x, int y);

void Cursor_Rotate(Cursor* cursor, int degrees);

void Cursor_DrawCircle(Cursor* cursor, SDL_Renderer* renderer, int radius, char* filename);

void Cursor_DrawSegment(Cursor* cursor, SDL_Renderer *renderer, int length, char* filename);

void Cursor_DrawRectangle(Cursor* cursor, SDL_Renderer *renderer, int width, int height, char* filename);

void Cursor_SetColor(Cursor* cursor, int r, int g, int b, int a);

void Cursor_SetThickness(Cursor* cursor, int thickness);

#endif