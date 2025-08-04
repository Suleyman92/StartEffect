import pygame
import sys
import random
from PIL import Image

logo_path = r"C:\Users\Suleyman\Desktop\SZynkron\Logo & Icon\Logo\SZ Logo.png"

image = Image.open(logo_path).convert('RGBA')
image = image.resize((100, 100), Image.Resampling.LANCZOS)
pixels = image.load()
width, height = image.size

pygame.init()
screen = pygame.display.set_mode((width * 6, height * 6))
pygame.display.set_caption("Logo Orjinal - Dağılma - Birleşme")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color):
        self.orig_x = x * 6
        self.orig_y = y * 6
        self.color = color
        self.x = self.orig_x
        self.y = self.orig_y
        self.speed_x = 0
        self.speed_y = 0
        self.state = "original"

    def spread(self):
        self.speed_x += random.uniform(-0.3, 0.3)
        self.speed_y += random.uniform(-0.3, 0.3)
        self.speed_x *= 0.95
        self.speed_y *= 0.95
        self.x += self.speed_x
        self.y += self.speed_y

    def gather(self):
        dx = self.orig_x - self.x
        dy = self.orig_y - self.y
        self.speed_x += dx * 0.01
        self.speed_y += dy * 0.01
        self.speed_x *= 0.7
        self.speed_y *= 0.7
        self.x += self.speed_x
        self.y += self.speed_y

    def update(self):
        if self.state == "spread":
            self.spread()
        elif self.state == "gather":
            self.gather()
        else:
            self.speed_x = 0
            self.speed_y = 0
            self.x = self.orig_x
            self.y = self.orig_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

particles = []

for y in range(height):
    for x in range(width):
        r,g,b,a = pixels[x, y]
        if a > 50:
            particles.append(Particle(x, y, (r, g, b)))

frame_count = 0
original_duration = 120
spread_duration = 300
gather_duration = 300

while True:
    screen.fill((18, 18, 18))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    frame_count += 1

    if frame_count < original_duration:
        for p in particles:
            p.state = "original"
    elif frame_count < original_duration + spread_duration:
        for p in particles:
            p.state = "spread"
    elif frame_count < original_duration + spread_duration + gather_duration:
        for p in particles:
            p.state = "gather"
    else:
        frame_count = 0

    for p in particles:
        p.update()
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

