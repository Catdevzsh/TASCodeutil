import pygame
import random
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake - Retro Style!")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Snake properties
snake_block_size = 10
snake_speed = 15

# Font for displaying score
font_style = pygame.font.SysFont(None, 25)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Sound generation function
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.5)  # Adjust volume as needed
    return sound

# Sounds
sounds = {
    "eat": generate_beep_sound(440, 0.1),  # A4 for eating
    "death": generate_beep_sound(220, 0.2),  # A3 for game over
}

def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def draw_snake(snake_block_size, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, green, [x, y, snake_block_size, snake_block_size])

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            screen.fill(black)
            message = font_style.render("You Lost! Press C-Play Again or Q-Quit", True, red)
            screen.blit(message, [width / 6, height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block_size
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            sounds["death"].play()
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, white, [foodx, foody, snake_block_size, snake_block_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                sounds["death"].play()
                game_close = True

        draw_snake(snake_block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0
            snake_length += 1
            sounds["eat"].play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
