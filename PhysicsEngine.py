import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Physics + Buttons")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color = (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        txt_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

class Ball:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.radius = 30
        self.color = color
        self.dragging = False
        self.last_mouse_pos = pygame.Vector2(x, y)

    def update(self, dt):
        if not self.dragging:
            self.pos += self.vel * dt
            self.vel *= 0.98  # friction
            self.check_wall_collision()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def check_wall_collision(self):
        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > WIDTH:
            self.vel.x *= -1
            self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        if self.pos.y - self.radius < 0 or self.pos.y + self.radius > HEIGHT:
            self.vel.y *= -1
            self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

    def check_collision(self, other):
        offset = other.pos - self.pos
        distance = offset.length()
        if distance < self.radius + other.radius:
            overlap = self.radius + other.radius - distance
            direction = offset.normalize()
            self.pos -= direction * overlap / 2
            other.pos += direction * overlap / 2
            self.vel, other.vel = other.vel, self.vel

balls = [
    Ball(200, 300, (255, 0, 0)),
    Ball(600, 300, (0, 0, 255)),
]

delete_mode = False

# --- Button Callbacks ---
def add_ball():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    color = [random.randint(50, 255) for _ in range(3)]
    balls.append(Ball(x, y, color))

def toggle_delete_mode():
    global delete_mode
    delete_mode = True

# --- Create Buttons ---
buttons = [
    Button(WIDTH - 220, 10, 100, 30, "Add Ball", add_ball),
    Button(WIDTH - 110, 10, 100, 30, "Delete Ball", toggle_delete_mode)
]

running = True
while running:
    dt = clock.tick(60) / 16
    screen.fill((30, 30, 30))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.Vector2(event.pos)

            # Button click check
            for button in buttons:
                button.check_click(event.pos)

            # Ball interaction
            if delete_mode:
                for ball in balls:
                    if (ball.pos - pos).length() < ball.radius:
                        balls.remove(ball)
                        delete_mode = False
                        break
            else:
                for ball in balls:
                    if (pos - ball.pos).length() < ball.radius:
                        ball.dragging = True
                        ball.last_mouse_pos = pos
                        ball.vel = pygame.Vector2(0, 0)

        elif event.type == pygame.MOUSEBUTTONUP:
            for ball in balls:
                if ball.dragging:
                    current_pos = pygame.Vector2(event.pos)
                    ball.vel = (current_pos - ball.last_mouse_pos) * 0.5
                    ball.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            for ball in balls:
                if ball.dragging:
                    ball.pos = pygame.Vector2(event.pos)

    # Physics update
    for ball in balls:
        ball.update(dt)

    # Collision check
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].check_collision(balls[j])

    # Draw balls
    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()

pygame.quit()
