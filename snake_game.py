"""
Snake Game
By Dylan Lee
Created with PyGame
"""

import random
import pygame as pg
from pygame.locals import *

# 3 playable modes:
# -- easy (same rules as the classic snake game)
# -- medium (the snake is enraged because it is too hungry, snake_speed increases based on score)
#           (for every 3 foods eaten, speed increases by 1. Starting speed is 13 and max speed is 35)
# -- hard (number of poisonous fruits (white) increases the longer your snake gets, up to 10 poisonous fruits)


def main():
    pg.init()

    # Colors used in the game
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screen settings
    screen_width = 600
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    snake_width = 15
    controls = {K_UP: (0, -1 * snake_width), K_DOWN: (0, snake_width),
                K_LEFT: (-1 * snake_width, 0), K_RIGHT: (snake_width, 0), 'start': (0, 0)}
    game_modes = {K_1: (1, "Easy"), K_2: (2, "Medium"), K_3: (3, "Hard")}

    score_font = pg.font.SysFont("bahnschrift", 35)
    game_font = pg.font.SysFont("bahnschrift", 35)
    default_speed = 13
    max_speed = 35

    # def render_multi_lines(text, text_color, x_coord, y_coord, font_size):
    #     lines = text.splitlines()
    #     for i, line in enumerate(lines):
    #         screen.blit(game_font.render(line, 0, text_color),
    #                     (x_coord + y_coord + font_size * i))

    def gen_random():
        x_rand = random.randrange(
            0, screen_width // snake_width) * snake_width
        y_rand = random.randrange(
            0, screen_height // snake_width) * snake_width
        return [x_rand, y_rand]

    def random_color(poison_color):
        r = random.randrange(0, 256)
        g = random.randrange(0, 256)
        b = random.randrange(0, 256)
        new_color = (r, g, b)
        if new_color != poison_color:
            return new_color
        return random_color(poison_color)

    def not_valid_move(x_val, y_val, snake_list, length_snake, poison_list):
        return x_val >= screen_width or x_val < 0 or y_val >= screen_height or y_val < 0 or (
            length_snake > 1 and [x_val, y_val] in snake_list[:length_snake - 1]) or [x_val, y_val] in poison_list

    def update_snake(snake_color, snake_width, snake_body):
        for part in snake_body:
            pg.draw.rect(screen, snake_color,
                         (part[0], part[1], snake_width, snake_width))

    def food_spawn(prev_pos, snake_body):
        food_pos = gen_random()
        while food_pos[0] == prev_pos[0] and food_pos[1] == prev_pos[1] or prev_pos in snake_body:
            food_pos = gen_random()
        return food_pos

    def poison_spawn(score, food_pos, snake_body):
        num_poisons = (score // 5) + 1 if score < 45 else 10
        poison_list = []
        for i in range(num_poisons):
            poison_pos = gen_random()
            while poison_pos in poison_list or poison_pos in snake_body or (
                    poison_pos[0] == food_pos[0] and poison_pos[1] == food_pos[1]):
                poison_pos = gen_random()
            poison_list.append(poison_pos)
        return poison_list

    def increased_speed(score):
        more_speed = (score // 3) * 2 if (score // 3) * \
            2 < max_speed else max_speed
        return default_speed + more_speed

    def display_score(score_color, score):
        score_tally = score_font.render(
            "Score: " + str(score), True, score_color)
        screen.blit(score_tally, [0, 0])

    def display_lost_screen(score):
        screen.fill(black)
        message = pg.font.SysFont("comicsansms", 25).render(
            "You lost! Your score was: " + str(score), True, magenta)
        play_again = pg.font.SysFont("comicsansms", 25).render(
            "Press (space key) to play again", True, magenta)
        change_mode = pg.font.SysFont("comicsansms", 25).render(
            "Press (Y) to switch game modes", True, magenta)
        screen.blit(message, (screen_width / 5, screen_height / 4))
        screen.blit(play_again, (screen_width / 5, screen_height / 3))
        screen.blit(change_mode, (screen_width / 5, screen_height / 2))
        pg.display.update()

    def select_mode_display():
        screen.fill(black)
        pg.display.set_caption("Snake Game")
        font = pg.font.SysFont("comicsansms", 25)
        first_line = font.render("Select game mode:", True, magenta)
        normal = font.render("1 - Easy", True, magenta)
        hard = font.render("2 - Medium", True, magenta)
        crazy = font.render("3 - Hard", True, magenta)
        screen.blit(first_line, [screen_width / 5, screen_height / 8])
        screen.blit(normal, [screen_width / 5, screen_height / 6])
        screen.blit(hard, [screen_width / 5, screen_height / 5])
        screen.blit(crazy, [screen_width / 5, screen_height / 4])
        pg.display.update()

    def select_mode_loop():
        selected = False
        while not selected:
            select_mode_display()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key in game_modes:
                        selection = game_modes[event.key][0]
                        name = game_modes[event.key][1]
                        selected = True
        return selection, name

    def game(selection, name):
        cur_selection, cur_name = selection, name
        food_color = yellow if cur_selection == 2 else blue
        snake_color = red if cur_selection == 2 else green
        caption = "Snake Game (" + cur_name + ")"
        pg.display.set_caption(caption)
        x_pos = screen_width // 2
        y_pos = screen_height // 2
        snake_length = 1
        snake_body = []
        poison_fruits = []
        x_rand = random.randrange(0, screen_width // snake_width) * snake_width
        y_rand = random.randrange(
            0, screen_height // snake_width) * snake_width
        food_pos = [x_rand, y_rand]
        game_running = True
        game_lost = False
        cur_key = 'start'

        while game_running:

            while game_lost:
                display_lost_screen(snake_length - 1)
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            game(cur_selection, cur_name)
                        if event.key == K_y:
                            game_loop()

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key in controls:
                        cur_key = event.key

            x_pos += controls[cur_key][0]
            y_pos += controls[cur_key][1]

            game_lost = not_valid_move(
                x_pos, y_pos, snake_body, snake_length, poison_fruits)

            screen.fill(black)
            if food_pos[0] == x_pos and food_pos[1] == y_pos:
                snake_length += 1
                food_pos = food_spawn(food_pos, snake_body)
                if cur_selection == 3:
                    poison_fruits = poison_spawn(
                        snake_length - 1, food_pos, snake_body)
                    snake_color = food_color
                    food_color = random_color(white)

            cur_pos = [x_pos, y_pos]
            snake_body.append(cur_pos)
            pg.draw.rect(
                screen, food_color, (food_pos[0], food_pos[1], snake_width, snake_width))
            for pos in poison_fruits:
                pg.draw.rect(screen, white,
                             (pos[0], pos[1], snake_width, snake_width))

            if len(snake_body) > snake_length:
                snake_body.pop(0)

            display_score(cyan, snake_length - 1)
            update_snake(snake_color, snake_width, snake_body)
            pg.display.update()
            snake_speed = increased_speed(
                snake_length - 1) if cur_selection != 1 else default_speed
            pg.time.Clock().tick(snake_speed)

        pg.quit()

    def game_loop():
        selection, name = select_mode_loop()
        game(selection, name)

    game_loop()


if __name__ == '__main__':
    main()
