#include <stdlib.h>
#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>

#include "cursor.h"
#include "shapes.h"
#include "utils.h"

Cursor* Cursor_Constructor(int x, int y)
{
    Cursor* cursor = malloc(sizeof(Cursor));
    cursor->x = x;
    cursor->y = y;
    cursor->angle = 0;
    cursor->thickness = 1;
    cursor->rgba[0] = 0;
    cursor->rgba[1] = 0;
    cursor->rgba[2] = 0;
    cursor->rgba[3] = 255;
    return cursor;
}


void Cursor_Move(Cursor* cursor, int x, int y){
    cursor->x = x;
    cursor->y = y;
}

void Cursor_DrawCircle(Cursor* cursor, SDL_Renderer* renderer, int radius, char* filename) {
    // if (cursor->thickness == 1){
    //     circleRGBA(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3]);
    //     return;
    // }
    
    // int inner_radius = radius - cursor->thickness;
    // filledCircleRGBA(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3]);
    // filledCircleRGBA(renderer, cursor->x, cursor->y, inner_radius, 255, 255, 255, 255);
    drawCircle(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawFilledCircle(Cursor* cursor, SDL_Renderer* renderer, int radius, char* filename) {
    drawFilledCircle(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawEllipse(Cursor* cursor, SDL_Renderer* renderer, int rx, int ry, char* filename) {
    drawEllipse(renderer, cursor->x, cursor->y, rx, ry, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawFilledEllipse(Cursor* cursor, SDL_Renderer* renderer, int rx, int ry, char* filename) {
    drawFilledEllipse(renderer, cursor->x, cursor->y, rx, ry, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawRoundedRectangle(Cursor* cursor, SDL_Renderer* renderer, int width, int height, int radius, char* filename) {
    drawRoundedRectangle(renderer, cursor->x, cursor->y, width, height, radius, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawBox(Cursor* cursor, SDL_Renderer* renderer, int width, int height, char* filename) {
    drawBox(renderer, cursor->x, cursor->y, width, height, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawRoundedBox(Cursor* cursor, SDL_Renderer* renderer, int width, int height, int radius, char* filename) {
    drawRoundedBox(renderer, cursor->x, cursor->y, width, height, radius, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawSegment(Cursor* cursor, SDL_Renderer *renderer, int length, char* filename) {
    // Convert the angle to radians
    double angleRadians = cursor->angle * (M_PI / 180.0);

    // Calculate the end point using trigonometry
    int x1 = cursor->x + (int)(length * cos(angleRadians));
    int y1 = cursor->y + (int)(length * sin(angleRadians));

    // Draw the line
    drawSegment(renderer, cursor->x, cursor->y, x1, y1, cursor->thickness, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawRectangle(Cursor* cursor, SDL_Renderer *renderer, int width, int height, char* filename) {
    drawRectangle(renderer, 
                cursor->x, cursor->y, 
                width, height, 
                cursor->angle, 
                cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], 
                filename);
}

void Cursor_DrawTriangle(Cursor* cursor, SDL_Renderer *renderer, int x0, int y0, int x1, int y1, char* filename){
    drawTriangle(renderer, 
                cursor->x, cursor->y, x0, y0, x1, y1, 
                cursor->angle, cursor->rgba[0], 
                cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], 
                filename);
}

void Cursor_Rotate(Cursor* cursor, int degrees){
    cursor->angle = degrees;
}

void Cursor_SetColor(Cursor* cursor, int r, int g, int b, int a){
    cursor->rgba[0] = r;
    cursor->rgba[1] = g;
    cursor->rgba[2] = b;
    cursor->rgba[3] = a;
}

void Cursor_SetThickness(Cursor* cursor, int thickness){
    cursor->thickness = thickness;
}
