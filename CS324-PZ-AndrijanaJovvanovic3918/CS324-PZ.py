import pygame, sys, random

def draw_bg():
    screen.blit(bg_surface, (0, bg_y_pos))
    screen.blit(bg_surface, (0, bg_y_pos - 700))

def draw_car(red_car_rect, yellow_car_rect,):
    screen.blit(yellow_car_surface, (yellow_car_rect.x, yellow_car_rect.y))
    screen.blit(red_car_surface, (red_car_rect.x, red_car_rect.y))

def yellow_car_movement(keys_pressed, yellow_car_rect):
     if keys_pressed[pygame.K_a] and yellow_car_rect.x - 2 > 0:
        yellow_car_rect.x -= 2
     if keys_pressed[pygame.K_d] and yellow_car_rect.x + 2 + yellow_car_rect.width < border.x:
        yellow_car_rect.x += 2

def red_car_movement(keys_pressed, red_car_rect):
     if keys_pressed[pygame.K_LEFT] and red_car_rect.x - 2 > border.x + border.width:
        red_car_rect.x -= 2
     if keys_pressed[pygame.K_RIGHT] and red_car_rect.x + 2 + red_car_rect.width < 500:
        red_car_rect.x += 2

def create_stone():
    random_pos = random.choice(stones)
    stone_rect = pygame.Rect(random_pos, -100, stone_width - 10, stone_height - 6)
    return stone_rect

def draw_stone(stones):
    for stone in stones:
       screen.blit(stone_surface, stone)

def move_stone(stones):
    for stone in stones:
        stone.centery += 2
    return stones

def check_red_collision(stone_list):
    for stone in stone_list:
        if red_car_rect.colliderect(stone):
           death_sound.play()
           return False
    return True

def check_yellow_collision(stone_list):
    for stone in stone_list:
        if yellow_car_rect.colliderect(stone):
             death_sound.play()
             return False
    return True

def winner_display(game_state, winner):
    if game_state == 'game_over':
        if winner == 'red':
            score_red_surface = game_font.render("YELLOW IS WINNER", True, (255, 255, 0))
            score_red_rect = score_red_surface.get_rect(center = (250, 350))
            screen.blit(score_red_surface, score_red_rect)
            space = game_font_new.render("(press space to start a new game)", True, (255, 255, 255))
            space_rect = space.get_rect(center = (250, 400))
            screen.blit(space , space_rect)
            screen.blit(yellow_car_surface, (yellow_car_rect.x, yellow_car_rect.y))
        if winner == 'yellow':
            score_yellow_surface = game_font.render("RED IS WINNER", True, (230, 46, 0))
            score_yellow_rect = score_yellow_surface.get_rect(center = (250, 350))
            screen.blit(score_yellow_surface, score_yellow_rect)
            space = game_font_new.render("(press space to start a new game)", True, (255, 255, 255))
            space_rect = space.get_rect(center = (250, 400))
            screen.blit(space , space_rect)
            screen.blit(red_car_surface, (red_car_rect.x, red_car_rect.y))
            
 
pygame.init()
screen = pygame.display.set_mode((500,700))
clock = pygame.time.Clock()

# Game Variables
border = pygame.Rect(250 - 5, 0, 10, 700)
car_width = 70
car_height = 130
stone_width = 96
stone_height = 63
life_yellow = 3
life_red = 3
game_active = True

SPAWNSTONE = pygame.USEREVENT 
pygame.time.set_timer(SPAWNSTONE, 500)

# Backgrounf
bg_surface = pygame.image.load('assets/road1.jpg')
bg_surface = pygame.transform.scale(bg_surface, (500, 700))
bg_y_pos = 0

# Car
yellow_car_surface = pygame.image.load('assets/car1.png')
yellow_car_surface = pygame.transform.scale(yellow_car_surface, (car_width, car_height))
yellow_car_rect = pygame.Rect(140, 530, car_width, car_height)

red_car_surface = pygame.image.load('assets/car2.png')
red_car_surface = pygame.transform.scale(red_car_surface, (car_width, car_height-5))
red_car_rect = pygame.Rect(280, 530, car_width, car_height)

# Stone
stone_surface = pygame.image.load('assets/stone.png')
stone_surface = pygame.transform.scale(stone_surface, (stone_width, stone_height))
stones = [5, 133, 270, 397]
stone_list = []

# Score Font
game_font = pygame.font.Font('04B_19.ttf', 50)
game_font_new = pygame.font.Font('04B_19.ttf', 25)

# Sound
death_sound = pygame.mixer.Sound('sound/udarac.wav')

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWNSTONE:
            stone_list.append(create_stone())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                stone_list.clear()
                draw_car(red_car_rect, yellow_car_rect)
                pygame.draw.rect(screen, (0,0,0), border)

      
# MOVMENT  
    keys_pressed = pygame.key.get_pressed()
    yellow_car_movement(keys_pressed, yellow_car_rect)
    red_car_movement(keys_pressed, red_car_rect)

    bg_y_pos += 1
    draw_bg()
    if bg_y_pos >= 700:
        bg_y_pos = 0
    
  
    if game_active:
        draw_car(red_car_rect, yellow_car_rect)
        pygame.draw.rect(screen, (0,0,0), border)
        if not check_yellow_collision(stone_list):
            game_active = False
            winner = "yellow"
        if not check_red_collision(stone_list):
            game_active = False
            winner = "red"

        stone_list = move_stone(stone_list)
        draw_stone(stone_list)
    else:
        winner_display('game_over', winner)

    pygame.display.update()
    clock.tick(700)