import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants for screen dimensions and text properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)  # White color
BACKGROUND_COLOR = (0, 0, 0)  # Black color
FONT_SIZE = 36

# Create the Pygame screen/window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Pygame")

# Create a font object
font = pygame.font.Font("Die in a fire PG.otf", FONT_SIZE)

# Create the text surface
text = font.render("LIVE A BASIC LIFE", True, TEXT_COLOR)

# Get the text's rect (position and dimensions)
text_rect = text.get_rect()

# Center the text on the screen
text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color (black)
    screen.fill(BACKGROUND_COLOR)

    # Draw the text on the screen
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()