import pygame
import random
import sys

cell_size = 25
number_of_cells = 25


class Food: 

  def __init__(self, window): 
    self.window = window
    self.position = self.generate_random_position()

  def draw(self):
    rect = pygame.Rect((self.position.x * cell_size, self.position.y * cell_size), (cell_size, cell_size))
    pygame.draw.rect(self.window, (255, 0, 0), rect)
    
  def generate_random_position(self):
    random_x = random.randint(0, number_of_cells - 1)
    random_y = random.randint(0, number_of_cells - 1)
    
    return pygame.Vector2(random_x, random_y)


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
  window = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
  clock = pygame.time.Clock()  # mao ata ning fps nya hahaha
  
  snake = Snake(window)
  food = Food(window)
  while True:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_w]:
          snake.direction = pygame.Vector2(0, -1)
        if keys[pygame.K_s]:
          snake.direction = pygame.Vector2(0, 1)
        elif keys[pygame.K_d]:
          snake.direction = pygame.Vector2(1, 0)
        elif keys[pygame.K_a]:
          snake.direction = pygame.Vector2(-1, 0)

    window.fill('black')

    food.draw()
    snake.draw()
    snake.movement()
      
    # Check if nakaon sa snake ang apple
    if snake.body[0] == food.position:
      # then e set napud nato ang position sa food into a random value
      food.position = food.generate_random_position()
      
      # then set nato ang is_growing to True 
      snake.is_growing = True
      
    """ 
      Check nato if mulapas ang snake sa screen.
      If mulapas then ilusot ra nato ang sa other side haha
      ex. mulapas sa left side then mulusot sa right side
    """
    if snake.body[0].x < -1:
      snake.body[0].x = number_of_cells
    elif snake.body[0].x > number_of_cells: 
      snake.body[0].x = 0
      
    if snake.body[0].y < -1:
      snake.body[0].y = number_of_cells
    elif snake.body[0].y > number_of_cells: 
      snake.body[0].y = 0
  
    pygame.display.flip()
    clock.tick(8)


if __name__ == '__main__':
  main()
