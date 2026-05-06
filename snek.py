import pygame
import random
import sys

cell_size = 25
number_of_cells = 25


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

    snake.draw()
    snake.movement()
      
    pygame.display.flip()
    clock.tick(15)
  
  # food_rect = pygame.Rect((food_pos.x * cell_size , food_pos.y * cell_size), (cell_size, cell_size))
  # pygame.draw.rect(screen, (255, 0, 0), food_rect)

  # for cell in snake_body:
  #   snake_rect = pygame.Rect((cell.x * cell_size, cell.y * cell_size), (cell_size, cell_size))
  #   pygame.draw.rect(screen, (0, 255, 0), snake_rect, 0, 4)
  
  # snake_body.insert(0, snake_body[0] + snake_direction)

  # if not growing:
  #   snake_body = snake_body[:-1]
  # else:
  #   growing = False
  
  # if snake_body[0] == food_pos:
  #   growing = True 
  #   new_food_pos = gen_random_pos()
    
  #   while new_food_pos in snake_body:
  #     new_food_pos = gen_random_pos()
      
  #   food_pos = new_food_pos
    
  # pygame.display.flip()
  # clock.tick(10)


def gen_random_pos():
  random_x = random.randint(0, number_of_cells)
  random_y = random.randint(0, number_of_cells)
  return pygame.Vector2(random_x, random_y)


snake_body = [pygame.Vector2(5, 7), pygame.Vector2(5, 6), pygame.Vector2(5, 5)]
food_pos = gen_random_pos()

vel = 5
snake_direction = pygame.Vector2(1, 0)

# food_rect = pygame.Rect((food_pos.x, food_pos.y), (cell_size, cell_size))
growing = False

if __name__ == '__main__':
  main()
