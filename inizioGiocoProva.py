import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FNF Style")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)

lane_width = WIDTH // 4
hit_line_y = HEIGHT - 120
note_speed = 5
hit_window = 40

font = pygame.font.SysFont("arial", 40)

score = 0
health = 100

# Mappa tasti
key_map = {
    pygame.K_LEFT: 0,
    pygame.K_DOWN: 1,
    pygame.K_UP: 2,
    pygame.K_RIGHT: 3
}

arrow_symbols = ["←", "↓", "↑", "→"]


# ------------------------
# FRECCIA CHE SCENDE
# ------------------------
class Note:
    def __init__(self, lane):
        self.lane = lane
        self.x = lane * lane_width + lane_width // 2
        self.y = -50

    def update(self):
        self.y += note_speed

    def draw(self):
        text = font.render(arrow_symbols[self.lane], True, WHITE)
        rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, rect)


# ------------------------
# PERSONAGGIO
# ------------------------
class Character:
    def __init__(self, x, color):
        self.x = x
        self.y = 380
        self.base_y = self.y
        self.color = color
        self.anim_timer = 0

    def animate(self):
        self.anim_timer = 10

    def update(self):
        if self.anim_timer > 0:
            self.y = self.base_y - 15
            self.anim_timer -= 1
        else:
            self.y = self.base_y

    def draw(self):
        # Corpo
        pygame.draw.rect(screen, self.color, (self.x-40, self.y, 80, 120))
        # Testa
        pygame.draw.circle(screen, (255, 220, 180), (self.x, self.y), 40)


notes = []
spawn_timer = 0

player = Character(200, (50, 100, 255))
enemy = Character(600, (200, 50, 50))

running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    spawn_timer += 1
    if spawn_timer > 20:
        notes.append(Note(random.randint(0, 3)))
        spawn_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in key_map:
                lane = key_map[event.key]
                hit = False

                for note in notes:
                    if note.lane == lane and abs(note.y - hit_line_y) < hit_window:
                        notes.remove(note)
                        score += 10
                        player.animate()
                        hit = True
                        break

                if not hit:
                    health -= 5

    for note in notes[:]:
        note.update()
        if note.y > HEIGHT:
            notes.remove(note)
            health -= 5

    player.update()
    enemy.update()

    # Disegna frecce fisse in basso
    for i in range(4):
        x = i * lane_width + lane_width // 2
        text = font.render(arrow_symbols[i], True, (100, 255, 100))
        rect = text.get_rect(center=(x, hit_line_y))
        screen.blit(text, rect)

    # Disegna note
    for note in notes:
        note.draw()

    player.draw()
    enemy.draw()

    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 60))
    

    if health <= 0:
        game_over = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over, (WIDTH//2 - 120, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()