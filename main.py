import pygame
import sys
import math
import random


pygame.init()


WIDTH, HEIGHT = 500, 700
RADIUS_INCREASE = 1.3
FPS = 60
GRAVITY = 0.5
RESTITUTION = 1
BALL_SPEED_INCREASE = 0.30
BALL_RADIUS_INCREASE = 0.4
MUSIC_PLAY_TIME = 550
COLOR_CHANGE_STEP = 5  


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SUBSCRIBE PLS')
screen.fill(BLACK)


ball_pos = [WIDTH +500 // 2, HEIGHT // 4]
ball_radius = 30
ball_speed = [8, 8]
hue = 240

# Circle setup
circle_radius = min(WIDTH, HEIGHT) // 2 - 20
circle_center = (WIDTH // 2, HEIGHT // 2)


pygame.mixer.init()
pygame.mixer.music.load('music.mp3')


music_start_time = 0
paused_time = 0


def reflect(speed, normal):
    dot_product = speed[0] * normal[0] + speed[1] * normal[1]
    reflected_speed = [speed[0] - 2 * dot_product * normal[0], speed[1] - 2 * dot_product * normal[1]]
    reflected_speed[0] *= RESTITUTION
    reflected_speed[1] *= RESTITUTION
    return reflected_speed


def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    hi = int(h / 60) % 6
    f = h / 60 - hi
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


clock = pygame.time.Clock()
running = True
music_playing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    ball_speed[1] += GRAVITY

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]


    dx = ball_pos[0] - circle_center[0]
    dy = ball_pos[1] - circle_center[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance + ball_radius >= circle_radius:

        normal = [dx / distance, dy / distance]
        ball_speed = reflect(ball_speed, normal)


        random_angle = random.uniform(-math.pi / 6, math.pi / 6)
        cos_angle = math.cos(random_angle)
        sin_angle = math.sin(random_angle)
        new_speed_x = ball_speed[0] * cos_angle - ball_speed[1] * sin_angle
        new_speed_y = ball_speed[0] * sin_angle + ball_speed[1] * cos_angle
        ball_speed = [new_speed_x, new_speed_y]


        ball_speed[0] += BALL_SPEED_INCREASE if ball_speed[0] > 0 else -BALL_SPEED_INCREASE
        ball_speed[1] += BALL_SPEED_INCREASE if ball_speed[1] > 0 else -BALL_SPEED_INCREASE


        ball_radius += BALL_RADIUS_INCREASE


        hue = (hue + 30) % 360


        overlap = (distance + ball_radius) - circle_radius
        ball_pos[0] -= overlap * normal[0]
        ball_pos[1] -= overlap * normal[1]


        if not music_playing:
            pygame.mixer.music.play(0, paused_time / 1000.0)
            music_start_time = pygame.time.get_ticks()
            music_playing = True

    if music_playing and pygame.time.get_ticks() - music_start_time >= MUSIC_PLAY_TIME:
        pygame.mixer.music.stop()
        paused_time += MUSIC_PLAY_TIME
        music_playing = False


    ball_color = hsv_to_rgb(hue, 1, 1)


    pygame.draw.circle(screen, BLACK, ball_pos, int(ball_radius) + 2)
    pygame.draw.circle(screen, ball_color, ball_pos, int(ball_radius))
    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 5)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
