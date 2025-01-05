#include <SDL2/SDL.h>
#include <SDL2_gfxPrimitives.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#include "cursor.h"
#include "utils.h"
#include "shapes.h"

// Constantes globales
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

int main(int argc, char *argv[]) {
    // Initialisation de SDL
    SDL_Start();
    SDL_Window *window = CreateWindow();
    SDL_Renderer *renderer = CreateRenderer(window);

    // Variables principales
    int centerX = 300;
    int centerY = 300;
    int radius = 50;
    int numCircles = 5;
    int angle = 0;
    float speed = 0.05;
    bool isAnimating = true;
    int gridX = 0;
    bool running = true;
    SDL_Event event;

    // Dessin initial
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

    Cursor* cursor1 = Cursor_Constructor(centerX, centerY);
    for (int  i = 0; (i < numCircles); (i = (i + 1)))
    {
        float offsetX = (centerX + ((radius * 3) * cos((angle + (i * (360 / numCircles))))));
        float offsetY = (centerY + ((radius * 3) * sin((angle + (i * (360 / numCircles))))));
        circleRGBA(renderer, offsetX, offsetY, radius, 0, 0, 0, 255);
    }

	while((gridX <= 600))
	{
		int gridY = 0;
		while((gridY <= 600))
		{
            circleRGBA(renderer, gridX, gridY, 5, 0, 0, 255, 255);
			gridY = gridY + 50;
		}
		gridX = gridX + 50;
	}
    Cursor_Move(cursor1, 400, 300);
    Cursor_Rotate(cursor1, 90);
    Cursor_DrawSegment(cursor1, renderer, 600, 600);
    Cursor_DrawCircle(cursor1, renderer, 50);
    Cursor_DrawRectangle(cursor1, renderer, 100, 50);
    circleRGBA(renderer, 250, 250, 75, 0, 0, 255, 255);

    SDL_RenderPresent(renderer);

    // Sauvegarder une capture d'écran
    saveScreenshot(renderer, "screenshot.bmp");

    // Boucle principale
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        SDL_Delay(16);
    }

    // Nettoyage
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
