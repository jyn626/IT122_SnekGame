import pygame
import random
import sys

cell_size = 25
number_of_cells = 25

retry_btn_image = pygame.image.load('./assets/retry_btn.png')


class Button:

  def __init__(self, window, text, x, y, image):
    self.window = window 
    self.text = text
    self.x = x 
    self.y = y
    self.font = pygame.font.SysFont(None, 60)
    self.small_font = pygame.font.SysFont(None, 40)
    
    self.image = image.convert()
    # self.image.set_colorkey('white')
    self.image = pygame.transform.scale(self.image, (200, 100))
    self.rect = self.image.get_rect()
    self.image.set_colorkey('black')
    self.rect.center = (self.x + (60 - 35), self.y + (50 - 40))
    
  def draw(self):
    # retry ni
    # rect = pygame.Rect(self.x, self.y, 120, 50)
    # pygame.draw.rect(self.window, (0, 200, 0), self.rect, border_radius=10)
    # text = self.small_font.render(self.text, True, (255, 255, 255))
    self.window.blit(self.image, self.rect)


def game_over_screen(window):
    retry_button = Button(window, "Retry", 180, 280, retry_btn_image)
    # pixel_font = pygame.font.Font('./fonts/slkscre.ttf')
    font = pygame.font.Font('./fonts/slkscre.ttf', 60)
    small_font = pygame.font.Font('./fonts/slkscre.ttf', 24)

    while True:
        # sa game over
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        window.blit(game_over_text, ((window.get_width() // 2) - 230, window.get_height() // 2 - 120))

        # retry ni
        # retry_rect = pygame.Rect(180, 280, 120, 50)
        # pygame.draw.rect(window, (0, 200, 0), retry_rect, border_radius=10)
        
        retry_button.draw()

        # retry_text = small_font.render("Retry", True, (255, 255, 255))
        # window.blit(retry_text, (205, 292))

        # Para sa quit button
        quit_rect = pygame.Rect(330, 280, 120, 50)
        pygame.draw.rect(window, (200, 0, 0), quit_rect, border_radius=10)

        quit_text = small_font.render("Quit", True, (255, 255, 255))
        window.blit(quit_text, (330 + 30, 292))

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

                # quist button
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


class Food: 

    def __init__(self, window, snake_body): 
        self.window = window
        self.snake_body = snake_body
        self.position = self.generate_random_position()

    def draw(self):
        rect = pygame.Rect((self.position.x * cell_size, self.position.y * cell_size), (cell_size, cell_size))
        pygame.draw.rect(self.window, (255, 0, 0), rect)
        
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
        self.body = [pygame.Vector2(5, 7), pygame.Vector2(5, 6), pygame.Vector2(5, 5)]
        self.is_growing = False
        self.direction = pygame.Vector2(1, 0)
        
    def draw(self):
        for cell in self.body:
            rect = pygame.Rect((cell.x * cell_size, cell.y * cell_size), (cell_size, cell_size))
            pygame.draw.rect(self.window, (0, 255, 0), rect, 0, 4)
      
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
                if event.key == pygame.K_w and snake.direction.y != 1:
                    snake.direction = pygame.Vector2(0, -1)
                if event.key == pygame.K_s and snake.direction.y != -1:
                    snake.direction = pygame.Vector2(0, 1)
                if event.key == pygame.K_d and snake.direction.x != -1:
                    snake.direction = pygame.Vector2(1, 0)
                if event.key == pygame.K_a and snake.direction.x != 1:
                    snake.direction = pygame.Vector2(-1, 0)

        window.fill((25, 25, 25))
        food.draw()
        snake.draw()
        snake.movement()
          
        # Check if nakaon sa snake ang apple
        if snake.body[0] == food.position:
            food.position = food.generate_random_position()
            snake.is_growing = True

        # Bawal Kaonon ang ikog rule
        for segment in snake.body[1:]:
            if snake.body[0] == segment:
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
