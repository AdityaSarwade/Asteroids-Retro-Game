import pygame, sys, os, random, math
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Globals
WIDTH = 800
HEIGHT = 600
time = 0

# Canvas Declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Asteroids")

# Sounds Declaration
pygame.mixer.pre_init()
pygame.init()

# Load Images
bg = pygame.image.load(os.path.join("images", "bg.jpg"))
debris = pygame.image.load(os.path.join("images", "debris2_brown.png"))
ship = pygame.image.load(os.path.join("images", "ship.png"))
ship_thrusted = pygame.image.load(os.path.join("images", "ship_thrusted.png"))
asteroid = pygame.image.load(os.path.join("images", "asteroid.png"))
shot = pygame.image.load(os.path.join("images", "shot2.png"))
explosion = pygame.image.load(os.path.join("images", "explosion_blue.png"))


# Load Sounds

# Missile
missile_sound = pygame.mixer.Sound(os.path.join("sounds", "missile.ogg"))
missile_sound.set_volume(1)

# Thrust
thruster_sound = pygame.mixer.Sound(os.path.join("sounds", "thrust.ogg"))
thruster_sound.set_volume(1)

# Explosion
explosion_sound = pygame.mixer.Sound(os.path.join("sounds", "explosion.ogg"))
explosion_sound.set_volume(1)

# Background score
pygame.mixer.music.load(os.path.join("sounds", "game.ogg"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()


# Internal Variables
ship_x = WIDTH / 2 - 50
ship_y = HEIGHT / 2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0

asteroid_x = []
asteroid_y = []
asteroid_angle = []
asteroid_speed = []
asteroid_num = 5

bullet_x = []
bullet_y = []
bullet_angle = []
bullet_num = 0

score = 0
game_over = False

for i in range(0, asteroid_num):
    asteroid_x.append(random.randint(0, WIDTH))
    asteroid_y.append(random.randint(0, HEIGHT))
    asteroid_angle.append(random.randint(0, 365))
    asteroid_speed.append(random.randint(1, 5))


# Check collision of ship and asteroid
def isCollision(enemy_x, enemy_y, bullet_x, bullet_y, dist):
    distance = math.sqrt(
        math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2))
    )
    if distance < dist:
        return True
    else:
        return False


# Rotate the ship
def rotate_center(image, angle):
    """rotate an image about it's center, while maintaining position

    Args:
        image (image): the image which is going to be rotated
        angle (number): the angle in degrees about which it will rotate
    """

    original_rectangle = image.get_rect()
    rotate_image = pygame.transform.rotate(image, angle)
    rotate_rect = original_rectangle.copy()
    rotate_rect.center = rotate_image.get_rect().center
    rotate_image = rotate_image.subsurface(rotate_rect).copy()
    return rotate_image


# Draw the game on window
def draw(canvas):
    global time
    global ship_is_forward
    global bullet_x, bullet_y
    global score
    canvas.fill(BLACK)
    canvas.blit(bg, (0, 0))
    canvas.blit(debris, (time * 0.3, 0))
    canvas.blit(debris, (time * 0.3 - WIDTH, 0))
    time += 1

    for i in range(0, bullet_num):
        canvas.blit(shot, (bullet_x[i], bullet_y[i]))

    for i in range(0, asteroid_num):
        canvas.blit(rotate_center(asteroid, time), (asteroid_x[i], asteroid_y[i]))

    if ship_is_forward:
        canvas.blit(rotate_center(ship_thrusted, ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rotate_center(ship, ship_angle), (ship_x, ship_y))

    # Draw Score
    font_1 = pygame.font.SysFont("Comic Sans MS", 40)
    label_1 = font_1.render("Score : " + str(score), 1, (255, 255, 0))
    canvas.blit(label_1, (50, 20))

    if game_over:
        font_2 = pygame.font.SysFont("Comic Sans MS", 80)
        label_2 = font_2.render("GAME OVER", 1, (255, 255, 0))
        canvas.blit(label_2, (WIDTH / 2 - 150, HEIGHT / 2 - 40))


# Handle Input
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction
    global ship_x, ship_y, ship_speed, ship_is_forward
    global bullet_x, bullet_y, bullet_angle, bullet_num
    global thruster_sound, missile_sound

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_RIGHT:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 10
            elif event.key == K_SPACE:
                bullet_x.append(ship_x + 50)
                bullet_y.append(ship_y + 50)
                bullet_angle.append(ship_angle)
                bullet_num = bullet_num + 1

        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
            elif event.key == K_UP:
                ship_is_forward = False

    if ship_is_rotating:
        if ship_direction == 1:
            ship_angle = ship_angle - 10
        if ship_direction == 0:
            ship_angle = ship_angle + 10

    if ship_is_forward or ship_speed > 0:
        ship_x = ship_x + math.cos(math.radians(ship_angle)) * ship_speed
        ship_y = ship_y + -math.sin(math.radians(ship_angle)) * ship_speed
        if ship_is_forward == False:
            ship_speed = ship_speed - 0.2


# Update screen
def update_screen():
    pygame.display.update()
    fps.tick(60)


def game_logic():
    global bullet_y, bullet_x, bullet_angle, bullet_num
    global asteroid_x, asteroid_y
    global score
    global game_over

    for i in range(0, bullet_num):
        bullet_x[i] = bullet_x[i] + math.cos(math.radians(bullet_angle[i])) * 10
        bullet_y[i] = bullet_y[i] + -math.sin(math.radians(bullet_angle[i])) * 10

    for i in range(0, asteroid_num):
        asteroid_x[i] = (
            asteroid_x[i]
            + math.cos(math.radians(asteroid_angle[i])) * asteroid_speed[i]
        )
        asteroid_y[i] = (
            asteroid_y[i]
            + -math.sin(math.radians(asteroid_angle[i])) * asteroid_speed[i]
        )
        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT
        if asteroid_y[i] > HEIGHT:
            asteroid_y[i] = 0

        if asteroid_x[i] < 0:
            asteroid_x[i] = WIDTH
        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0

        if isCollision(ship_x, ship_y, asteroid_x[i], asteroid_y[i], 27):
            print("Game Over")
            print("Score : "+str(score))
            game_over = True

    for i in range(0, bullet_num):
        for j in range(0, asteroid_num):
            if isCollision(bullet_x[i], bullet_y[i], asteroid_x[j], asteroid_y[j], 50):
                asteroid_x[j] = random.randint(0, WIDTH)
                asteroid_y[j] = random.randint(0, HEIGHT)
                asteroid_angle[j] = random.randint(0, 365)
                explosion_sound.play()
                score = score + 1


# Asteroids game loop
while True:
    draw(window)
    handle_input()
    if not game_over:
        game_logic()
    update_screen()
