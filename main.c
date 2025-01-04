#include <SDL2/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "utils.h"
#include "shapes.h"

// Constantes globales
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 800

int main(int argc, char *argv[]) {
    // Start SDL
    SDL_Start();
    SDL_Window *window = CreateWindow();
    SDL_Renderer *renderer = CreateRenderer(window);

    int centerX = 300;
	int centerY = 300;
	int radius = 50;
	int numCircles = 5;
	int angle = 0;
	float speed = 0.05;
	bool isAnimating = true;
	int gridX = 0;
	// INSERT VARIABLES
    bool running = true;
    SDL_Event event;

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Transparent
    SDL_RenderClear(renderer);

    for (int  i = 0; (i < numCircles); (i = (i + 1)))
	{
		float offsetX = (centerX + ((radius * 3) * cos((angle + (i * (360 / numCircles))))));
		float offsetY = (centerY + ((radius * 3) * sin((angle + (i * (360 / numCircles))))));
		SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
		drawCircle(renderer, offsetX, offsetY, radius);
	}

	while((gridX <= 600))
	{
		int gridY = 0;
		while((gridY <= 600))
		{
			SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
			drawCircle(renderer, gridX, gridY, 5);
			(gridY = (gridY + 50));
		}
		(gridX = (gridX + 50));
	}
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
	drawCircle(renderer, 250, 250, 75);
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

    return 0;
}