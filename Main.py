import pygame
import sys
import math
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TITLE = "Shape Arena"
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

def get_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return -math.degrees(math.atan2(dy, dx))

player_x = WINDOW_WIDTH / 2
player_y = WINDOW_HEIGHT / 2
player_radius = 15
player_speed = 5
player_color = (0, 255, 128)

player_surface_size = player_radius * 2 + 16
player_original = pygame.Surface((player_surface_size, player_surface_size), pygame.SRCALPHA)

center_pt = player_surface_size // 2

pygame.draw.circle(player_original, player_color, (center_pt, center_pt), player_radius)

pygame.draw.polygon(player_original, (255, 255, 255), [
    (center_pt + player_radius - 2, center_pt - 5),
    (center_pt + player_radius + 8, center_pt),
    (center_pt + player_radius - 2, center_pt + 5)
])

bullets = []
bullet_speed = 12
bullet_radius = 4
bullet_color = (255, 255, 100)
shoot_cooldown = 10
shoot_timer = 0

enemies = []
enemy_size = 30
enemy_speed = 2
enemy_spawn_cooldown = 90
enemy_spawn_timer = 0

enemy_original = pygame.Surface((enemy_size, enemy_size), pygame.SRCALPHA)
pygame.draw.rect(enemy_original, (255, 80, 80), (0, 0, enemy_size, enemy_size))
pygame.draw.rect(enemy_original, (255, 255, 255), (enemy_size - 8, enemy_size // 2 - 4, 8, 8))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed

    if player_x < player_radius:
        player_x = player_radius
    if player_x > WINDOW_WIDTH - player_radius:
        player_x = WINDOW_WIDTH - player_radius
    if player_y < player_radius:
        player_y = player_radius
    if player_y > WINDOW_HEIGHT - player_radius:
        player_y = WINDOW_HEIGHT - player_radius

    mouse_pos = pygame.mouse.get_pos()
    angle = get_angle((player_x, player_y), mouse_pos)
    
    player_rotated = pygame.transform.rotate(player_original, angle)
    player_rect = player_rotated.get_rect(center=(int(player_x), int(player_y)))

    if shoot_timer > 0:
        shoot_timer -= 1

    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0] and shoot_timer == 0:
        dx = mouse_pos[0] - player_x
        dy = mouse_pos[1] - player_y
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
            
            bullets.append({
                "x": player_x,
                "y": player_y,
                "vx": dir_x * bullet_speed,
                "vy": dir_y * bullet_speed
            })
            shoot_timer = shoot_cooldown

    for bullet in bullets[:]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]
        
        if (bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or 
            bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT):
            bullets.remove(bullet)

    if enemy_spawn_timer > 0:
        enemy_spawn_timer -= 1
    else:
        random_choice1 = random.randint(0, 1)
        random_choice2 = random.randint(0, 1)
        if random_choice1 == 0:
            spawn_x = random.randint(-30, 830)
            if random_choice2 == 0:
                spawn_y = -30
            else:
                spawn_y = 630
        if random_choice1 == 1:
            spawn_y = random.randint(-30, 630)
            if random_choice2 == 0:
                spawn_x = -30
            else:
                spawn_x = 830
        
        enemies.append({
            "x": float(spawn_x),
            "y": float(spawn_y),
            "health": 3
        })
        enemy_spawn_timer = enemy_spawn_cooldown

    for enemy in enemies:
        dx = player_x - enemy["x"]
        dy = player_y - enemy["y"]
        distance = math.hypot(dx, dy)
        if distance > 0:
            enemy["x"] += (dx / distance) * enemy_speed
            enemy["y"] += (dy / distance) * enemy_speed

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(
            enemy["x"] - enemy_size / 2,
            enemy["y"] - enemy_size / 2,
            enemy_size,
            enemy_size
        )
        for bullet in bullets[:]:
            closest_x = max(enemy_rect.left, min(bullet["x"], enemy_rect.right))
            closest_y = max(enemy_rect.top, min(bullet["y"], enemy_rect.bottom))
            
            dist_x = bullet["x"] - closest_x
            dist_y = bullet["y"] - closest_y
            distance = math.hypot(dist_x, dist_y)
            
            if distance < bullet_radius:
                if bullet in bullets:
                    bullets.remove(bullet)
                enemy["health"] -= 1
                if enemy["health"] <= 0:
                    if enemy in enemies:
                        enemies.remove(enemy)
                    break

    screen.fill((30, 30, 40))

    for bullet in bullets:
        pygame.draw.circle(screen, bullet_color, (int(bullet["x"]), int(bullet["y"])), bullet_radius)

    for enemy in enemies:
        enemy_angle = get_angle((enemy["x"], enemy["y"]), (player_x, player_y))
        enemy_rotated = pygame.transform.rotate(enemy_original, enemy_angle)
        enemy_draw_rect = enemy_rotated.get_rect(center=(int(enemy["x"]), int(enemy["y"])))
        screen.blit(enemy_rotated, enemy_draw_rect.topleft)

    screen.blit(player_rotated, player_rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()