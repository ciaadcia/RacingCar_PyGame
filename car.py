import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Car Endless Road")

clock = pygame.time.Clock()
FPS = 60

def load_img(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((200, 200, 200))
        return surf

road_img = load_img("road.png", (WIDTH, HEIGHT))
car_img = load_img("car.png", (100, 100))
rock_img = load_img("vehicle.png", (80, 80))
coin_img = load_img("money.png", (40, 40))

lanes = [WIDTH//4, WIDTH//2, WIDTH - WIDTH//4]

player_lane = 1
player_x = lanes[player_lane]
player_y = HEIGHT - 120

lives = 3
score = 0

rocks = []
coins = []

rock_timer = 0
coin_timer = 0

# road scroll
road_y = 0
scroll_speed = 5

def draw_text(text, x, y, color=(255,255,255), size=28):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_rock():
    lane = random.randint(0, 2)
    x = lanes[lane]
    rocks.append([x, -100])

def spawn_coin():
    lane = random.randint(0, 2)
    x = lanes[lane]
    coins.append([x, -100])

def move_player():
    global player_x
    target_x = lanes[player_lane]
    player_x += (target_x - player_x) * 0.2  # smooth movement

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

running = True
game_over = False
win = False

while running:
    clock.tick(FPS)

    screen.fill((0,0,0))

    # scroll road
    road_y += scroll_speed
    if road_y >= HEIGHT:
        road_y = 0

    screen.blit(road_img, (0, road_y - HEIGHT))
    screen.blit(road_img, (0, road_y))

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over and not win:
                if event.key == pygame.K_LEFT:
                    player_lane = max(0, player_lane - 1)
                if event.key == pygame.K_RIGHT:
                    player_lane = min(2, player_lane + 1)

    if not game_over and not win:
        # smooth movement
        move_player()
        # spawn rocks (slow)
        rock_timer += 1
        if rock_timer > 60:  # ~1 sec
            if random.random() < 0.7:
                spawn_rock()
            rock_timer = 0
        # spawn coins (rarer)
        coin_timer += 1
        if coin_timer > 100:
            if random.random() < 0.5:
                spawn_coin()
            coin_timer = 0
        # move rocks
        for rock in rocks[:]:
            rock[1] += scroll_speed + 2
            if rock[1] > HEIGHT:
                rocks.remove(rock)
        # move coins
        for coin in coins[:]:
            coin[1] += scroll_speed + 2
            if coin[1] > HEIGHT:
                coins.remove(coin)
        # player rect
        player_rect = car_img.get_rect(center=(player_x, player_y))
        # rocks collision
        for rock in rocks[:]:
            rock_rect = rock_img.get_rect(center=(rock[0], rock[1]))
            if check_collision(player_rect, rock_rect):
                rocks.remove(rock)
                lives -= 1
                if lives <= 0:
                    game_over = True
        # coin collision
        for coin in coins[:]:
            coin_rect = coin_img.get_rect(center=(coin[0], coin[1]))
            if check_collision(player_rect, coin_rect):
                coins.remove(coin)
                score += 1
                if score >= 10:
                    win = True
        # draw objects
        for rock in rocks:
            screen.blit(rock_img, rock_img.get_rect(center=(rock[0], rock[1])))
        for coin in coins:
            screen.blit(coin_img, coin_img.get_rect(center=(coin[0], coin[1])))
        # draw player
        screen.blit(car_img, player_rect)
        # UI
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", 10, 40)
    if game_over:
        draw_text("GAME OVER", WIDTH//2 - 100, HEIGHT//2, (255,0,0), 40)
        draw_text(f"Final Score: {score}", WIDTH//2 - 110, HEIGHT//2 + 50)
    if win:
        draw_text("YOU WIN!", WIDTH//2 - 90, HEIGHT//2, (0,255,0), 40)
        draw_text(f"Score: {score}", WIDTH//2 - 70, HEIGHT//2 + 50)
    pygame.display.update()
pygame.quit()
sys.exit()