import pygame
import random
import time

class BossTurt():
    def __init__(self, image_path, health, screen_width):
        self.health = health
        self.alive = True
        self.pic = pygame.image.load(image_path)
        self.pic = pygame.transform.scale(self.pic, (100, 100))
        self.pic = pygame.transform.flip(self.pic, False, True)
        self.pic.set_colorkey((0, 0, 0))
        self.rect = self.pic.get_rect()
        self.rect.x = 350
        self.rect.y = 50
        self.screen_width = screen_width
        self.going_right = True
        self.going_down = True
        self.projectiles = []
        self.wave_counter = 0
        self.wave = 0
        self.shoot_timer = 0
        self.shot_interval = 40  # frames until next shot

    def move(self):
        if self.going_right:
            self.rect.x += 2
        else:
            self.rect.x -= 2

        if self.rect.x > self.screen_width - self.rect.width:
            self.going_right = False
        if self.rect.x < 0:
            self.going_right = True
            self.wave_counter += 1

        if self.going_down:
            self.rect.y += 0.6
        else:
            self.rect.y -= 0.6

        if self.rect.y > 80:
            self.going_down = False
        if self.rect.y < 40:
            self.going_down = True


    def reset_firing(self, shot_interval):
        self.wave_counter = 0
        self.shoot_timer = 0
        proj = Projectile(
            self.rect.centerx,
            self.rect.bottom,
            speed=7
        )
        self.projectiles.append(proj)  # store it so it persists
        self.shoot_timer = 0
        self.shot_interval = shot_interval  # randomize next interval


    def fire(self):
        if self.wave_counter >= 1:
            self.wave += 1
            self.reset_firing(10)

        self.shoot_timer += 1
        if self.shoot_timer >= self.shot_interval:
            # Spawn projectile at the boss's current center
            proj = Projectile(
                self.rect.centerx,
                self.rect.bottom,
                speed=7
            )
            self.projectiles.append(proj)       # store it so it persists
            self.shoot_timer = 0
            self.shot_interval = 45  # randomize next interval

    def update_projectiles(self, screen, screen_height):
        for proj in self.projectiles[:]:        # copy so we can remove safely mid-loop
            proj.movement()
            proj.draw(screen)
            if proj.y > screen_height:          # remove once off screen
                self.projectiles.remove(proj)


class Projectile():
    def __init__(self, x, y, speed):
        self.pic = pygame.image.load("image/bubble_scaled_down_3x.png")
        self.pic = pygame.transform.scale(self.pic, (50, 50))
        self.x = x
        self.y = y
        self.speed = speed

    def movement(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.pic, (self.x, self.y))


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
        boss.fire()                                         # increments timer, fires when ready



        screen.fill((50, 50, 50))
        screen.blit(boss.pic, boss.rect)
        boss.update_projectiles(screen, 600)               # moves, draws, and cleans up projectiles
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()