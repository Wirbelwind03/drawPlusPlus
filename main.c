#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdio.h>

int main(int argc, char *argv[]){
	int centerX = 300;
	int centerY = 300;
	int radius = 50;
	int numCircles = 5;
	int angle = 0;
	float speed = 0.05;
	bool isAnimating = true;
	for (int i = 0; i < numCircles; i = i + 1)
 {
		offsetX = centerX + radius * 3 * cos(angle + i * 360 / numCircles);
		offsetY = centerY + radius * 3 * sin(angle + i * 360 / numCircles);
		drawCircle(offsetX, offsetY, radius);
	}
	if (radius > 40 && numCircles >= 5) {
		drawSquare(centerX, centerY, radius * 2);
	}
	else {
		drawTriangle(centerX, centerY, radius * 2);
	}
	int gridX = 0;
	while (gridX <= 600) {
		int gridY = 0;
		while (gridY <= 600) {
		drawCircle(gridX, gridY, 5);
		gridY = gridY + 50;
	}
		gridX = gridX + 50;
	}
	drawCircle(250, 250, 75);
}
