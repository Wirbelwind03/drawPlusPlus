#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#include "cursor.h"
#include "utils.h"
#include "shapes.h"
#include "globals.h"

int main(int argc, char *argv[]) {
    FILE *file = fopen("Data/Outputs/drawing_positions.txt", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Start SDL
    SDL_Start();
    SDL_Window *window = CreateWindow(SCREEN_WIDTH, SCREEN_HEIGHT);
    SDL_Renderer *renderer = CreateRenderer(window);

// INSERT VARIABLES
    char filename[255];
    int drawing_index = 1;
    SDL_Event event;

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

// INSERT DRAWINGS
    SDL_RenderPresent(renderer);

// INSERT ANIMATIONS

    // Clean
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    fclose(file);

    return 0;
}