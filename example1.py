import pygame

# https://realpython.com/pygame-a-primer/

pygame.init()

screen = pygame.display.set_mode([500, 500])

running = True
while running:
    for event in pygame.event.get():
        # quit if user clicked close button
        if event.type == pygame.QUIT:
            running = False
            
    # fill screen - white
    screen.fill((255, 255, 255))
    
    # Draw circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    
    # flip the display
    pygame.display.flip()
    
pygame.quit()