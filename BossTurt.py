import pygame
import random

class BossTurt():
    def __init__(self, image_path, health, screen_width):
        self.health = health
        self.alive = True
        self.pic = pygame.image.load(image_path)
        self.pic = pygame.transform.scale(self.pic, (100, 100))
        self.pic = pygame.transform.flip(self.pic, False, True)   # flips image upside down so mouth faces player
        self.pic.set_colorkey((0, 0, 0))
        self.rect = self.pic.get_rect()
        self.rect.x = 350
        self.rect.y = 50
        self.screen_width = screen_width                          # stored so move() knows where the right wall is
        self.going_right = True
        self.going_down = True
        self.projectiles = []                                     # stores shots fired from boss
        self.shoot_timer = 0
        self.shot_pattern = random.randint(20, 60)                # frame count when the next shot fires
        self.cooling_down = False                                 # True = boss is resting, player can attack
        self.cooldown_timer = 0

    def move(self):
        if self.going_right:
            self.rect.x += 2
        else:
            self.rect.x -= 2

        if self.rect.x > self.screen_width - self.rect.width:     # hit right wall, flip direction
            self.going_right = False
        if self.rect.x < 0:                                       # hit left wall, flip direction
            self.going_right = True

        if self.going_down:
            self.rect.y += 0.6
        else:
            self.rect.y -= 0.6

        if self.rect.y > 80:                                      # bottom of sway range
            self.going_down = False
        if self.rect.y < 40:                                      # top of sway range
            self.going_down = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    boss = BossTurt("image/turtle.png", 90, 800)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        boss.move()

        screen.fill((50, 50, 50))
        screen.blit(boss.pic, boss.rect)
        pygame.display.flip()
        clock.tick(60)                       # cap at 60 frames per second

    pygame.quit()

main()