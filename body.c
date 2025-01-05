#include <SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "cursor.h"
#include "utils.h"
#include "shapes.h"

// INSERT GLOBALS

int main(int argc, char *argv[]) {
    FILE *file = fopen("example.txt", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Start SDL
    SDL_Start();
    SDL_Window *window = CreateWindow(SCREEN_WIDTH, SCREEN_HEIGHT);
    SDL_Renderer *renderer = CreateRenderer(window);

    // INSERT VARIABLES
    int drawing_index = 1;
    bool running = true;
    SDL_Event event;

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

    // INSERT DRAWINGS

    SDL_RenderPresent(renderer);

    // Boucle principale
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        // INSERT ANIMATIONS

        SDL_Delay(16);
    }

    // Clean
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    fclose(file);

    printf("END");

    return 0;
}