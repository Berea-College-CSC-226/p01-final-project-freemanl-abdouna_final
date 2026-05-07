import pygame
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
        self.wave = 1
        self.shoot_timer = 0
        self.shot_interval = 60
        self.paused = False
        self.pause_timer = 0
        self.pause_duration = 180  # frames (180 = 3 seconds at 60fps)
        self.speed = 3

    def move(self):
        if self.going_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

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
        if self.paused:
            return
        self.shoot_timer += 1
        if self.shoot_timer >= self.shot_interval:
            proj = Projectile(self.rect.centerx, self.rect.bottom, speed=7)
            self.projectiles.append(proj)
            self.wave_counter += 1
            self.shoot_timer = 0

            # Update wave based on shot count
            if self.wave_counter >= 35:
                self.wave = 3
                self.shot_interval = 26
                self.speed = 6
                if self.wave_counter == 35:
                    self.paused = True
            elif self.wave_counter >= 10:
                self.wave = 2
                self.shot_interval = 40
                self.speed = 4
                if self.wave_counter == 10:
                    self.paused = True
            else:
                self.wave = 1
                self.shot_interval = 50
                self.speed = 3

    def take_damage(self):
        self.health -= 30
        if self.health <= 0:
            self.alive = False

    def update_projectiles(self, screen, screen_height, player):
        for proj in self.projectiles[:]:
            proj.movement()
            proj.draw(screen)
            if proj.y > screen_height:
                self.projectiles.remove(proj)

            # Check if projectile rect collides with player rect
            proj_rect = pygame.Rect(proj.x + 15, proj.y + 15, 20, 20)
            if proj_rect.colliderect(player.rect):
                player.alive = False
                self.projectiles.remove(proj)

    def update_pause(self):
        if self.paused:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_duration:
                self.paused = False
                self.pause_timer = 0


class WaveText():
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 36)
        self.big_font = pygame.font.SysFont("Arial", 72)
        self.health_font = pygame.font.SysFont("Arial", 36)
        self.win_font = pygame.font.SysFont("Arial", 84)


    def draw(self, screen, wave):
        text_surface = self.font.render(f"Wave {wave}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    def draw_announcement(self, screen, wave):

        text_surface = self.big_font.render(f"Wave {wave}, Boss health down 30", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))    # centered on 800x600 screen
        screen.blit(text_surface, text_rect)

    def draw_health(self, screen, health):
        text_surface = self.health_font.render(f"Boss Health:{health}/90", True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.topright = (800, 10)
        screen.blit(text_surface, text_rect)

    def draw_win(self, screen):
        text_surface = self.win_font.render("YOU WINN!!!!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 250))
        screen.blit(text_surface, text_rect)

        story_font = pygame.font.SysFont("Arial", 24)
        story_lines = [
            "The ancient turtle king has fallen.",
            "Peace returns to the land at last.",
            "The hunter walks home, a legend.",
        ]
        for i, line in enumerate(story_lines):
            story_surface = story_font.render(line, True, (255, 255, 255))
            story_rect = story_surface.get_rect(center=(400, 350 + i * 30))
            screen.blit(story_surface, story_rect)

    def draw_lose(self, screen):
        text_surface = self.win_font.render("YOU LOSE!", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)

    def draw_retry_button(self, screen):
        button_rect = pygame.Rect(325, 480, 150, 60)
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        button_font = pygame.font.SysFont("Arial", 32)
        text_surface = button_font.render("TRY AGAIN", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        return button_rect


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


class Player():
    def __init__(self, image_path, screen_width, screen_height):
        self.pic = pygame.image.load(image_path)
        self.pic = pygame.transform.scale(self.pic, (100, 100))
        self.pic.set_colorkey((0, 0, 0))
        self.alive = True
        self.rect = self.pic.get_rect()
        self.rect.x = 350
        self.rect.y = 480
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width
        if self.rect.y < 110:
            self.rect.y = 110
        if self.rect.y > self.screen_height - self.rect.height:
            self.rect.y = self.screen_height - self.rect.height


def run_boss_fight():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    bg_image = pygame.image.load("image/proj_bg.gif")
    bg_image = pygame.transform.scale(bg_image, (800, 600))
    clock = pygame.time.Clock()

    boss = BossTurt("image/turtle.png", 90, 800)
    player = Player("image/hunter.png", 800, 600)
    wave_display = WaveText()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # retry button click — only matters if game is over
                if not player.alive or not boss.alive:
                    if retry_rect.collidepoint(event.pos):
                        boss = BossTurt("image/turtle.png", 90, 800)
                        player = Player("image/hunter.png", 800, 600)

        boss.update_pause()

        if not boss.paused:
            boss.move()

        boss.fire()

        screen.blit(bg_image, (0, 0))
        screen.blit(boss.pic, boss.rect)
        boss.update_projectiles(screen, 600, player)
        wave_display.draw(screen, boss.wave)

        if boss.paused:
            wave_display.draw_announcement(screen, boss.wave)

        wave_display.draw_health(screen, boss.health)

        # Player attacks boss during cooldown
        if boss.paused and player.rect.colliderect(boss.rect):
            boss.take_damage()
            player.rect.x = 350
            player.rect.y = 480
            boss.paused = False
            boss.pause_timer = 0

        retry_rect = None    # default — no button this frame

        if not player.alive:
            screen.fill((50, 50, 50))
            wave_display.draw_lose(screen)
            retry_rect = wave_display.draw_retry_button(screen)
            boss.paused = True
            boss.projectiles = []

        if not boss.alive:
            screen.fill((50, 50, 50))
            wave_display.draw_win(screen)
            retry_rect = wave_display.draw_retry_button(screen)

        if player.alive and boss.alive:
            player.move()
            screen.blit(player.pic, player.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_boss_fight()
