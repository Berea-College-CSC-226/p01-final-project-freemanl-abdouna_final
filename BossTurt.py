import pygame
import random

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
        self.wave = 1
        self.shoot_timer = 0
        self.shot_interval = 60

    def move(self):
        if self.going_right:
            self.rect.x += 2
        else:
            self.rect.x -= 2

        if self.rect.x > self.screen_width - self.rect.width:
            self.going_right = False
        if self.rect.x < 0:
            self.going_right = True

        if self.going_down:
            self.rect.y += 0.6
        else:
            self.rect.y -= 0.6

        if self.rect.y > 80:
            self.going_down = False
        if self.rect.y < 40:
            self.going_down = True

    def fire(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shot_interval:
            proj = Projectile(self.rect.centerx, self.rect.bottom, speed=7)
            self.projectiles.append(proj)
            self.wave_counter += 1
            self.shoot_timer = 0

            # Update wave based on shot count
            if self.wave_counter >= 25:
                self.wave = 3
                self.shot_interval = 30
            elif self.wave_counter >= 10:
                self.wave = 2
                self.shot_interval = 45
            else:
                self.wave = 1
                self.shot_interval = 60

    def update_projectiles(self, screen, screen_height):
        for proj in self.projectiles[:]:
            proj.movement()
            proj.draw(screen)
            if proj.y > screen_height:
                self.projectiles.remove(proj)


class WaveText():
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 36)

    def draw(self, screen, wave):
        text_surface = self.font.render(f"Wave {wave}", True, (0, 255, 0))
        screen.blit(text_surface, (10, 10))


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
    wave_display = WaveText()          # created once, reused every frame

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        boss.move()
        boss.fire()

        screen.fill((50, 50, 50))
        screen.blit(boss.pic, boss.rect)
        boss.update_projectiles(screen, 600)
        wave_display.draw(screen, boss.wave)   # draws current wave number every frame
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()