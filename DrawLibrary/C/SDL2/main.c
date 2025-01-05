#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "cursor.h"
#include "utils.h"
#include "shapes.h"

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600

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

    int centerX = 300;
    int centerY = 300;
    int radius = 50;
    int numCircles = 5;
    int angle = 0;
    float speed = 0.05;
    bool isAnimating = true;
    int gridX = 0;

    char filename[255];
    int drawing_index = 1;
    bool running = true;
    SDL_Event event;

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

    Cursor* cursor1 = Cursor_Constructor(centerX, centerY);
    for (int  i = 0; (i < numCircles); (i = (i + 1)))
    {
        float offsetX = (centerX + ((radius * 3) * cos((angle + (i * (360 / numCircles))))));
        float offsetY = (centerY + ((radius * 3) * sin((angle + (i * (360 / numCircles))))));
        circleRGBA(renderer, offsetX, offsetY, radius, 0, 0, 0, 255);
        fprintf(file, "%d,%d\n", (int)offsetX, (int)offsetY);
        snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);
        drawing_index++;
        savePartialScreenshot(renderer, filename, offsetX - radius, offsetY - radius, radius * 2 + 1, radius * 2 + 1);
        ClearCanvas(renderer, 255, 255, 255, 255);
    }
    
    while((gridX <= 600))
    {
        int gridY = 0;
        while((gridY <= 600))
        {
            circleRGBA(renderer, gridX, gridY, 5, 0, 0, 0, 255);
            fprintf(file, "%d,%d\n", (int)gridX, (int)gridY);
            snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);
            drawing_index++;
            savePartialScreenshot(renderer, filename, gridX - 5, gridY - 5, 5 * 2 + 1, 5 * 2 + 1);
            ClearCanvas(renderer, 255, 255, 255, 255);
            (gridY = (gridY + 50));
        }
        (gridX = (gridX + 50));
    }
    Cursor_Move(cursor1, 400, 300);
    Cursor_Rotate(cursor1, 90);
    
    Cursor_DrawSegment(cursor1, renderer, 600, 600);
    fprintf(file, "%d,%d\n", (int)cursor1->x, (int)cursor1->y);
    
    Cursor_DrawCircle(cursor1, renderer, 50);
    fprintf(file, "%d,%d\n", (int)cursor1->x, (int)cursor1->y);
    
    Cursor_DrawRectangle(cursor1, renderer, 100, 50);
    fprintf(file, "%d,%d\n", (int)cursor1->x, (int)cursor1->y);
    
    circleRGBA(renderer, 250, 250, 75, 0, 0, 0, 255);
    fprintf(file, "%d,%d\n", (int)250, (int)250);
    snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);
    drawing_index++;
    savePartialScreenshot(renderer, filename, 250 - 75, 250 - 75, 75 * 2 + 1, 75 * 2 + 1);
    ClearCanvas(renderer, 255, 255, 255, 255);

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
