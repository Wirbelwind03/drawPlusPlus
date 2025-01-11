#include <stdlib.h>
#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>
#include <SDL2_rotozoom.h>

#include "cursor.h"
#include "shapes.h"
#include "utils.h"
#include "globals.h"

void drawCircle(SDL_Renderer *renderer, int x, int y, int radius, int r, int g, int b, int a, char* filename){
    // Draw the rectangle on the renderer (red color)
    circleRGBA(renderer, x, y, radius, r, g, b, a);

    // Render the content to the window
    SDL_RenderPresent(renderer);

    // Define the area to capture (the area where the rectangle was drawn)
    SDL_Rect captureRect = { x - radius, y - radius, 2 * radius + 1, 2 * radius + 1 };

    // Ensure the capture rectangle's coordinates are valid
    if (captureRect.x < 0) {
        captureRect.w += captureRect.x;  // Reduce width if it overflows to the left
        captureRect.x = 0;  // Reset to 0 if it's off-screen
    }

    if (captureRect.y < 0) {
        captureRect.h += captureRect.y;  // Reduce height if it overflows to the top
        captureRect.y = 0;  // Reset to 0 if it's off-screen
    }

    // Check if the rectangle extends beyond the window (right and bottom)
    if (captureRect.x + captureRect.w > SCREEN_WIDTH) {  // Window width (640px in this case)
        captureRect.w = SCREEN_WIDTH - captureRect.x;  // Adjust the width to fit within the window
    }

    if (captureRect.y + captureRect.h > SCREEN_HEIGHT) {  // Window height (480px in this case)
        captureRect.h = SCREEN_HEIGHT - captureRect.y;  // Adjust the height to fit within the window
    }

    // Capture the current content of the renderer into an SDL_Surface
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, captureRect.w, captureRect.h, 32, SDL_PIXELFORMAT_RGBA32);
    if (!surface) {
        printf("Surface creation failed: %s\n", SDL_GetError());
        return;
    }

    // Copy the rendered content to the surface
    if (SDL_RenderReadPixels(renderer, &captureRect, SDL_PIXELFORMAT_RGBA32, surface->pixels, surface->pitch) != 0) {
        printf("Failed to read pixels: %s\n", SDL_GetError());
        SDL_FreeSurface(surface);
        return;
    }

    // Save the surface as a BMP file
    if (SDL_SaveBMP(surface, filename) != 0) {
        printf("Failed to save BMP: %s\n", SDL_GetError());
    }
    // Clean up
    SDL_FreeSurface(surface);

    ClearCanvas(renderer, 255, 255, 255, 255);
}

void drawSegment(SDL_Renderer *renderer, int x0, int y0, int x1, int y1, int thickness, int r, int g, int b, int a, char* filename){
    thickLineRGBA(renderer, x0, y0, x1, y1, thickness, r, g, b, a);

    // Render the content to the window
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

    // Capture the current content of the renderer into an SDL_Surface
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, captureRect.w, captureRect.h, 32, SDL_PIXELFORMAT_RGBA32);
    if (!surface) {
        printf("Surface creation failed: %s\n", SDL_GetError());
        return;
    }

    // Copy the rendered content to the surface
    if (SDL_RenderReadPixels(renderer, &captureRect, SDL_PIXELFORMAT_RGBA32, surface->pixels, surface->pitch) != 0) {
        printf("Failed to read pixels: %s\n", SDL_GetError());
        SDL_FreeSurface(surface);
        return;
    }

    // Save the rotated surface as a BMP file
    if (SDL_SaveBMP(surface, filename) != 0) {
        printf("Failed to save BMP: %s\n", SDL_GetError());
    }

    // Clean up
    SDL_FreeSurface(surface);

    ClearCanvas(renderer, 255, 255, 255, 255);
}

void drawRectangle(SDL_Renderer *renderer, int x, int y, int width, int height, int angle, int r, int g, int b, int a, char* filename){
    // Draw the rectangle on the renderer (red color)
    boxRGBA(renderer, x, y, x + width, y + height, r, g, b, a);

    // Render the content to the window
    SDL_RenderPresent(renderer);

    // Define the area to capture (the area where the rectangle was drawn)
    SDL_Rect captureRect = { x, y, width, height };

    // Capture the current content of the renderer into an SDL_Surface
    SDL_Surface *surface = SDL_CreateRGBSurfaceWithFormat(0, captureRect.w, captureRect.h, 32, SDL_PIXELFORMAT_RGBA32);
    if (!surface) {
        printf("Surface creation failed: %s\n", SDL_GetError());
        return;
    }

    // Copy the rendered content to the surface
    if (SDL_RenderReadPixels(renderer, &captureRect, SDL_PIXELFORMAT_RGBA32, surface->pixels, surface->pitch) != 0) {
        printf("Failed to read pixels: %s\n", SDL_GetError());
        SDL_FreeSurface(surface);
        return;
    }

    // Rotate the surface
    SDL_Surface *rotatedSurface = rotozoomSurface(surface, angle, 1.0, 1);
    if (!rotatedSurface) {
        printf("Failed to rotate surface.\n");
        SDL_FreeSurface(surface);
        return;
    }

    // Save the rotated surface as a BMP file
    if (SDL_SaveBMP(rotatedSurface, filename) != 0) {
        printf("Failed to save BMP: %s\n", SDL_GetError());
    }

    // Clean up
    SDL_FreeSurface(surface);
    SDL_FreeSurface(rotatedSurface);

    ClearCanvas(renderer, 255, 255, 255, 255);
}