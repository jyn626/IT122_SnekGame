import pygame
import random
import sys

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
    self.font = pygame.font.SysFont('./fonts/slkscre.ttf', 22)
    self.rect = pygame.Rect(self.x, self.y, 150, 80)  
    
  def draw(self):
    text = self.font.render(self.text, True, self.fg)
    text_rect = text.get_rect(center=self.rect.center)

    pygame.draw.rect(self.window, self.bg, self.rect)
    self.window.blit(text, text_rect)


def game_over_screen(window):
    retry_button = Button(window, "Retry", RETRY_BUTTON_COLOR, (0, 0, 0), 180, 280)
    quit_button = Button(window, "Quit", QUIT_BUTTON_COLOR, (0, 0, 0), retry_button.rect.x + 200, 280)

    while True:
        # sa game over
        retry_button.draw()
        # Para sa quit button
        quit_button.draw()
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # retry button
                if retry_button.rect.collidepoint(mouse_pos):
                    main()

                # quit button
                if quit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


class Food: 

    def __init__(self, window, snake_body): 
        self.window = window
        self.snake_body = snake_body
        self.position = self.generate_random_position()

    def draw(self):
        rect = pygame.Rect((self.position.x * cell_size, self.position.y * cell_size), (cell_size, cell_size))
        pygame.draw.rect(self.window, FOOD_COLOR, rect)
        
    def generate_random_position(self):
        random_x = random.randint(0, number_of_cells - 1)
        random_y = random.randint(0, number_of_cells - 1)
        
        coordinates = pygame.Vector2(random_x, random_y)
        
        while (coordinates in self.snake_body):
          random_x = random.randint(0, number_of_cells - 1)
          random_y = random.randint(0, number_of_cells - 1)
        
          coordinates = pygame.Vector2(random_x, random_y)
        
        return coordinates 


class Snake:

    def __init__(self, window):
        self.window = window
        self.body = [pygame.Vector2(5, 7), pygame.Vector2(5, 6)]
        self.is_growing = False
        self.direction = pygame.Vector2(1, 0)
        self.new_direction = self.direction
        
    def draw(self):
        for cell in self.body:
            rect = pygame.Rect((cell.x * cell_size, cell.y * cell_size), (cell_size, cell_size))
            pygame.draw.rect(self.window, SNAKE_COLOR, rect, 0, 4)
      
    def movement(self):
        self.body.insert(0, self.body[0] + self.direction)
        if not self.is_growing: 
            self.body = self.body[:-1]  
        else:
            self.is_growing = False


def main():
    pygame.init()
    window = pygame.display.set_mode((cell_size * number_of_cells + 100, cell_size * number_of_cells))
    clock = pygame.time.Clock() 
    is_gameover = False
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
              
              print(snake.new_direction)
              print(snake.direction)

        window.fill(BACKGROUND_COLOR)
        food.draw()
        snake.draw()
        snake.movement()
        snake.direction = snake.new_direction
          
        # Check if nakaon sa snake ang apple
        if snake.body[0] == food.position:
            food.position = food.generate_random_position()
            snake.is_growing = True

        # Bawal Kaonon ang ikog rule
        if snake.body[0] in snake.body[1:]:
          game_over_screen(window)
        
        if snake.body[0].x < 0:
            game_over_screen(window)
            snake.body[0].x = number_of_cells - 1
        elif snake.body[0].x >= number_of_cells + 8:
            game_over_screen(window)
            snake.body[0].x = 0
        if snake.body[0].y < 0:
            game_over_screen(window)
            snake.body[0].y = number_of_cells - 1
        elif snake.body[0].y >= number_of_cells: 
            game_over_screen(window)
            snake.body[0].y = 0
      
        pygame.display.flip()
        clock.tick(12)


if __name__ == '__main__':
    main()
