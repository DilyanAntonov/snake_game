import pygame
import sys
import random

pygame.font.init()

# Colors
white = (255, 255, 255)
gray = (89, 89, 89)
black = (0, 0, 0)
green = (0, 225, 0)
red = (225, 0, 0)

screen_size = 900  # The size of the window
block_size = 30  # The size of Snake and Food blocks


class Snake:
    def __init__(self):
        self.position = [screen_size//2, screen_size//2]  # Starting position for the snake
        self.body = [[screen_size//2, screen_size//2]]  # The list that will contain all block of the snake
        self.direction = "RIGHT"  # Direction to go upon starting the game

    def change_direction(self, direction):
        if direction == "RIGHT" and not self.direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "RIGHT"

        if direction == "LEFT" and not self.direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "LEFT"

        if direction == "UP" and not self.direction == "DOWN" and not self.direction == "UP":
            self.direction = "UP"

        if direction == "DOWN" and not self.direction == "UP" and not self.direction == "DOWN":
            self.direction = "DOWN"

    def move(self, food_pos):
        if self.direction == "RIGHT":
            self.position[0] += block_size

        if self.direction == "LEFT":
            self.position[0] -= block_size

        if self.direction == "UP":
            self.position[1] -= block_size

        if self.direction == "DOWN":
            self.position[1] += block_size

        self.body.insert(0, list(self.position))
        if self.position == food_pos:
            return 1
        else:
            self.body.pop()
            return 0

    def wall_collision(self):
        if self.position[0] > screen_size or self.position[0] < 0:
            return 1
        elif self.position[1] > screen_size or self.position[1] < 0:
            return 1
        for body_part in self.body[1:]:
            if self.position == body_part:
                return 1
        return 0

    def get_head(self):
        return self.position

    def get_body(self):
        return self.body


class Food:
    def __init__(self):
        self.position = [random.randrange(0, screen_size//block_size)*block_size, random.randrange(0, screen_size//block_size)*block_size]
        self.existing_food = False

    def spawn_food(self):
        if self.existing_food is False:
            self.position = [random.randrange(0, screen_size//block_size)*block_size, random.randrange(0, screen_size//block_size)*block_size]
            self.existing_food = True
        return self.position

    def draw_food(self, a):
        self.existing_food = a


window = pygame.display.set_mode((screen_size, screen_size))  # The main window
pygame.display.set_caption("Snake game")  # The caption of the window
fps = pygame.time.Clock()

# Fonts
score_font = pygame.font.SysFont('Comic Sans MS', 30)
you_died_font = pygame.font.SysFont('Ariel', 120)
game_over_font = pygame.font.SysFont('Ariel', 60)

def game_over():
    window.fill(white)  # Hides the uneaten food and snake
    died_text = you_died_font.render('YOU DIED', False, red)
    game_over_text = game_over_font.render("Press SPACE to play again or ESC to exit", False, red)
    window.blit(died_text, (250, 300))
    window.blit(game_over_text, (50, 450))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_loop()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def game_loop(score=0):
    snake = Snake()
    food = Food()

    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                if event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                if event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game_loop()

        food_position = food.spawn_food()
        window.fill(white)

        if snake.move(food_position) == 1:
            score += 1
            food.draw_food(False)

        for block in snake.get_body():
            pygame.draw.rect(window, green, pygame.Rect(block[0], block[1], block_size, block_size))

        pygame.draw.rect(window, red, pygame.Rect(food_position[0], food_position[1], block_size, block_size))

        if snake.wall_collision() == 1:
            game_over()

        score_text = score_font.render('Score: ' + str(score), False, black)
        window.blit(score_text, (770,5))

        pygame.display.flip()
        fps.tick(10)

        pygame.display.update()

game_loop()