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

void Cursor_DrawCircle(Cursor* cursor, SDL_Renderer* renderer, int windowWidth, int windowHeight, int radius, char* filename) {
    // if (cursor->thickness == 1){
    //     circleRGBA(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3]);
    //     return;
    // }
    
    // int inner_radius = radius - cursor->thickness;
    // filledCircleRGBA(renderer, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3]);
    // filledCircleRGBA(renderer, cursor->x, cursor->y, inner_radius, 255, 255, 255, 255);
    drawCircle(renderer, windowWidth, windowHeight, cursor->x, cursor->y, radius, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawSegment(Cursor* cursor, SDL_Renderer *renderer, int windowWidth, int windowHeight, int length, char* filename) {
    // Convert the angle to radians
    double angleRadians = cursor->angle * (M_PI / 180.0);

    // Calculate the end point using trigonometry
    int x1 = cursor->x + (int)(length * cos(angleRadians));
    int y1 = cursor->y + (int)(length * sin(angleRadians));

    // Draw the line
    drawSegment(renderer, windowWidth, windowHeight, cursor->x, cursor->y, x1, y1, cursor->thickness, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
}

void Cursor_DrawRectangle(Cursor* cursor, SDL_Renderer *renderer, int windowWidth, int windowHeight, int width, int height, char* filename) {
    drawRectangle(renderer, windowWidth, windowHeight, cursor->x, cursor->y, width, height, cursor->angle, cursor->rgba[0], cursor->rgba[1], cursor->rgba[2], cursor->rgba[3], filename);
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
