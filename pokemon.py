import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)
import random

# player class definition
class Pokemon(pygame.sprite.Sprite):
    def __init__(self):
        super(Pokemon, self).__init__()
        self.surf = pygame.image.load("images/charizard.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# enemy class definition
class Pokeball(pygame.sprite.Sprite):
    def __init__(self):
        super(Pokeball, self).__init__()
        self.surf = pygame.image.load("images/pokeball.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill


# calculate score based on time passed
def get_game_score(start_time):
    return int((pygame.time.get_ticks() - start_time) / 10)


pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Pokeball Dodge")

font = pygame.font.SysFont("monospace", 18)
clock = pygame.time.Clock()
game_start_time = pygame.time.get_ticks()

# add background music johto
pygame.mixer.music.load("music/Johto.mp3")
pygame.mixer.music.play(loops=-1)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
background = pygame.image.load("images/field.jpg")

# clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1  # unique event id
pygame.time.set_timer(ADDENEMY, 500)  # difficulty level?

# init player
player = Pokemon()
player_score = 0

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Pokeball()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # update player movement
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # update game score
    player_score = get_game_score(game_start_time)
    score_text = font.render(f"SCORE: {str(player_score)}", True, (0, 0, 0))
    screen.blit(score_text, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # end the game if player collided with enemy
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()

# game ends
pygame.mixer.music.stop()
pygame.mixer.quit()
