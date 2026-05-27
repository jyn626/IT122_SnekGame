import pygame
import random
import sys

high_score = 0

cell_size = 25
number_of_cells = 25

retry_btn_image = pygame.image.load('./assets/retry_btn.png')

SNAKE_COLOR = (52, 211, 153)
FOOD_COLOR = (244, 63, 94)

RETRY_BUTTON_COLOR = (234, 179, 8)
QUIT_BUTTON_COLOR = (168, 85, 247)

BACKGROUND_COLOR = (18, 24, 38)


class Button:

    def __init__(self, window, text, bg, fg, x, y):

        self.window = window
        self.text = text

        self.x = x
        self.y = y

        self.bg = bg
        self.fg = fg

        self.font = pygame.font.Font('./fonts/slkscre.ttf', 22)

        self.rect = pygame.Rect(self.x, self.y, 150, 80)

    def draw(self):

        text = self.font.render(self.text, True, self.fg)

        text_rect = text.get_rect(center=self.rect.center)

        pygame.draw.rect(self.window, self.bg, self.rect)

        self.window.blit(text, text_rect)


def game_over_screen(window, score, high_score):

    retry_button = Button(
        window,
        "Retry",
        RETRY_BUTTON_COLOR,
        (0, 0, 0),
        window.get_width() // 2 - 250,
        280
    )

    quit_button = Button(
        window,
        "Quit",
        QUIT_BUTTON_COLOR,
        (0, 0, 0),
        retry_button.rect.x + 350,
        280
    )

    # para naay score ug high score sa game over
    font = pygame.font.Font('./fonts/slkscre.ttf', 36)

    score_text = font.render(
        f"SCORE: {score}",
        True,
        (255, 255, 255)
    )

    high_score_text = font.render(
        f"HIGHEST SCORE: {high_score}",
        True,
        (255, 255, 255)
    )

    while True:

        window.fill(BACKGROUND_COLOR)

        score_rect = score_text.get_rect(
            center=(window.get_width() // 2, 130)
        )

        high_score_rect = high_score_text.get_rect(
            center=(window.get_width() // 2, 190)
        )

        window.blit(score_text, score_rect)
        window.blit(high_score_text, high_score_rect)

        retry_button.draw()
        quit_button.draw()

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                # Retry button
                if retry_button.rect.collidepoint(mouse_pos):
                    main()

                # Quit button
                if quit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


class Food:

    def __init__(self, window, snake_body):

        self.window = window
        self.snake_body = snake_body

        self.position = self.generate_random_position()

    def draw(self):

        rect = pygame.Rect(
            (self.position.x * cell_size,
             self.position.y * cell_size),

            (cell_size, cell_size)
        )

        pygame.draw.rect(self.window, FOOD_COLOR, rect)

    def generate_random_position(self):

        random_x = random.randint(0, number_of_cells - 1)
        random_y = random.randint(0, number_of_cells - 1)

        coordinates = pygame.Vector2(random_x, random_y)

        while coordinates in self.snake_body:

            random_x = random.randint(0, number_of_cells - 1)
            random_y = random.randint(0, number_of_cells - 1)

            coordinates = pygame.Vector2(random_x, random_y)

        return coordinates


class Snake:

    def __init__(self, window):

        self.window = window

        self.body = [
            pygame.Vector2(5, 7),
            pygame.Vector2(5, 6)
        ]

        self.is_growing = False

        self.direction = pygame.Vector2(1, 0)
        self.new_direction = self.direction

    def draw(self):
        """
        for drawing, its gonna be a grid by grid system 
        so we will not do our movement by pixels but by grid.
        """

        # here we draw every cell in the snake.body
        for cell in self.body:
            # the parameters are, respectively: x, y, width, height
            # we need to multiply the cell's x and y by the tile size
            # because this is a grid system, we will move or place each cell 
            # by grid. take for example
            #  cell.x -> 1px, then cell.x * 25 = 25 (that's one block)
            #  cell.x -> 2px, then cell.x * 25 = 50 (that's two blocks)
            # and so on...
            rect = pygame.Rect(
                (cell.x * cell_size,
                 cell.y * cell_size),

                (cell_size, cell_size)
            )

            # the parameters are, respectively: window, color, rect (object), rectangle thickness, border radius
            pygame.draw.rect(
                self.window,
                SNAKE_COLOR,
                rect,
                0,
                4
            )

    def movement(self):
        """
        for the movement, it constantly adds new `head` (with the new coordinates) 
        and removes the `tail` every frame so it creates the illusion of movement
        """

        # suppose the current head's vector is (5, 6) and our direction is right (1, 0)
        # we will add it up so (6, 6), and this becomes the new head
        new_head = self.body[0] + self.direction 
        
        # insert the new head in the place of the current head (to replace it as the new head)
        self.body.insert(
            0,
            new_head
        )

        # we check if we currently aren't eating the apple in the current frame
        if not self.is_growing:
            # if NOT then we remove the tail to keep the length
            self.body = self.body[:-1]  # [:-1] excludes the last element of the array.

        else:
            # but if we are eating, then we won't remove the tail, so it grows 1 block. 
            self.is_growing = False


def main():

    global high_score

    pygame.init()

    window = pygame.display.set_mode(
        (
            cell_size * number_of_cells,
            cell_size * number_of_cells
        )
    )

    clock = pygame.time.Clock()
    
    score = 0

    font = pygame.font.Font('./fonts/slkscre.ttf', 28)

    snake = Snake(window)

    food = Food(window, snake.body)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d and snake.direction.x != -1:

                    snake.new_direction = pygame.Vector2(1, 0)

                elif event.key == pygame.K_a and snake.direction.x != 1:

                    snake.new_direction = pygame.Vector2(-1, 0)

                elif event.key == pygame.K_w and snake.direction.y != 1:

                    snake.new_direction = pygame.Vector2(0, -1)

                elif event.key == pygame.K_s and snake.direction.y != -1:

                    snake.new_direction = pygame.Vector2(0, 1)

        window.fill(BACKGROUND_COLOR)

        # para sa score sa top left
        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        window.blit(score_text, (10, 10))

        food.draw()

        snake.draw()

        snake.movement()

        snake.direction = snake.new_direction
        
        if snake.body[0] == food.position:

            food.position = food.generate_random_position()

            snake.is_growing = True

            score += 1

            # para ma update ang highest score
            if score > high_score:
                high_score = score

        if snake.body[0] in snake.body[1:]:

            game_over_screen(window, score, high_score)

        if snake.body[0].x < 0:

            game_over_screen(window, score, high_score)

            snake.body[0].x = number_of_cells

        elif snake.body[0].x >= number_of_cells:

            game_over_screen(window, score, high_score)

            snake.body[0].x = 0

        if snake.body[0].y < 0:

            game_over_screen(window, score, high_score)

            snake.body[0].y = number_of_cells

        elif snake.body[0].y >= number_of_cells:

            game_over_screen(window, score, high_score)

            snake.body[0].y = 0

        pygame.display.flip()

        clock.tick(12)


if __name__ == '__main__':
    main()
