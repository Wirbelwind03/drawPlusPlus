#include <stdlib.h>
#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>

#include "shapes.h"
#include "utils.h"
#include "globals.h"

void drawCircle(SDL_Renderer *renderer, 
                int x, int y, 
                int radius, 
                int r, int g, int b, int a, 
                char* filename) {
    // Draw the circle on the renderer
    aacircleRGBA(renderer, x, y, radius, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box
    SDL_Rect captureRect = { x - radius, y - radius, 2 * radius + 1, 2 * radius + 1 };

    AdjustCaptureRect(&captureRect);

    SaveDrawing(renderer, captureRect, 0, filename);
}

void drawFilledCircle(SDL_Renderer *renderer, 
                int x, int y, 
                int radius, 
                int r, int g, int b, int a, 
                char* filename) {
    
    filledCircleRGBA(renderer, x, y, radius, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box
    SDL_Rect captureRect = { x - radius, y - radius, 2 * radius + 1, 2 * radius + 1 };

    AdjustCaptureRect(&captureRect);

    SaveDrawing(renderer, captureRect, 0, filename);
}

void drawEllipse(SDL_Renderer *renderer, 
                   int x, int y, 
                   int rx, int ry, 
                   int angle, 
                   int r, int g, int b, int a, 
                   char* filename) {
    // Draw the anti-aliased ellipse on the renderer
    aaellipseRGBA(renderer, x, y, rx, ry, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box
    SDL_Rect captureRect = {
        x - rx, 
        y - ry, 
        2 * rx + 1, 
        2 * ry + 1
    };

    AdjustCaptureRect(&captureRect);

    // Save the captured drawing
    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawFilledEllipse(SDL_Renderer *renderer, 
                   int x, int y, 
                   int rx, int ry, 
                   int angle, 
                   int r, int g, int b, int a, 
                   char* filename) {
    // Draw the filled ellipse on the renderer
    filledEllipseRGBA(renderer, x, y, rx, ry, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box
    SDL_Rect captureRect = {
        x - rx, 
        y - ry, 
        2 * rx + 1, 
        2 * ry + 1
    };

    AdjustCaptureRect(&captureRect);

    // Save the captured drawing
    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawSegment(SDL_Renderer *renderer, 
                int x0, int y0, int x1, int y1, 
                int thickness, 
                int r, int g, int b, int a, 
                char* filename) {
    thickLineRGBA(renderer, x0, y0, x1, y1, thickness, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the area to capture (based on the line's bounding box)
    int minX = x0 < x1 ? x0 : x1;
    int minY = y0 < y1 ? y0 : y1;
    int maxX = x0 > x1 ? x0 : x1;
    int maxY = y0 > y1 ? y0 : y1;

    SDL_Rect captureRect = {
        minX - thickness, 
        minY - thickness, 
        (maxX - minX) + thickness * 2, 
        (maxY - minY) + thickness * 2
    };

    SaveDrawing(renderer, captureRect, 0, filename);
}

void drawRectangle(SDL_Renderer *renderer, 
                int x, int y, 
                int width, int height, 
                int angle, 
                int r, int g, int b, int a,
                char* filename) {
    // Draw the rectangle on the renderer
    rectangleRGBA(renderer, x, y, x + width, y + height, r, g, b, a);
    
    // Render the drawing to the window
    SDL_RenderPresent(renderer);
    
    // Define the area to capture
    SDL_Rect captureRect = { x, y, width, height };
    
    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawTriangle(SDL_Renderer *renderer,
                int x1, int y1, int x2, int y2, int x3, int y3, 
                int angle, int r, int g, int b, int a, 
                char* filename) {
    aatrigonRGBA(renderer, x1, y1, x2, y2, x3, y3, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box of the trigon
    // https://www.sunshine2k.de/coding/java/TriangleRasterization/boundingbox.png
    int minX = (x1 < x2 ? (x1 < x3 ? x1 : x3) : (x2 < x3 ? x2 : x3));
    int minY = (y1 < y2 ? (y1 < y3 ? y1 : y3) : (y2 < y3 ? y2 : y3));
    int maxX = (x1 > x2 ? (x1 > x3 ? x1 : x3) : (x2 > x3 ? x2 : x3));
    int maxY = (y1 > y2 ? (y1 > y3 ? y1 : y3) : (y2 > y3 ? y2 : y3));

    SDL_Rect captureRect = {
        minX, 
        minY, 
        maxX - minX, 
        maxY - minY
    };

    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawRoundedRectangle(SDL_Renderer *renderer,
                          int x, int y, 
                          int width, int height, 
                          int radius, 
                          int angle, int r, int g, int b, int a, 
                          char* filename) {
    // Draw the rounded rectangle on the renderer
    roundedRectangleRGBA(renderer, x, y, x + width, y + height, radius, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box of the rounded rectangle
    SDL_Rect captureRect = {
        x, 
        y, 
        width, 
        height
    };

    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawBox(SDL_Renderer *renderer, 
                int x, int y, 
                int width, int height, 
                int angle, 
                int r, int g, int b, int a,
                char* filename) {
    // Draw the box on the renderer
    boxRGBA(renderer, x, y, x + width, y + height, r, g, b, a);
    
    // Render the drawing to the window
    SDL_RenderPresent(renderer);
    
    // Define the bounding box
    SDL_Rect captureRect = {
        x, 
        y, 
        width, 
        height
    };
    
    SaveDrawing(renderer, captureRect, angle, filename);
}

void drawRoundedBox(SDL_Renderer *renderer,
                          int x, int y, 
                          int width, int height, 
                          int radius, 
                          int angle, int r, int g, int b, int a, 
                          char* filename) {
    // Draw the rounded rectangle on the renderer
    roundedBoxRGBA(renderer, x, y, x + width, y + height, radius, r, g, b, a);

    // Render the drawing to the window
    SDL_RenderPresent(renderer);

    // Define the bounding box of the rounded rectangle
    SDL_Rect captureRect = {
        x, 
        y, 
        width, 
        height
    };

    SaveDrawing(renderer, captureRect, angle, filename);
}