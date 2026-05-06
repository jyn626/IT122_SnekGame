import pygame
import random

pygame.init()

cell_size = 25
number_of_cells = 25

screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
clock = pygame.time.Clock()  # mao ata ning fps nya hahaha
running = True


def gen_random_pos():
  random_x = random.randint(0, number_of_cells)
  random_y = random.randint(0, number_of_cells)
  return pygame.Vector2(random_x, random_y)


snake_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
snake_body = [pygame.Vector2(5, 7), pygame.Vector2(5, 6), pygame.Vector2(5, 5)]
food_pos = gen_random_pos()

vel = 5
snake_direction = pygame.Vector2(1, 0)

# food_rect = pygame.Rect((food_pos.x, food_pos.y), (cell_size, cell_size))
growing = False
  
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      keys = pygame.key.get_pressed()
  
      if keys[pygame.K_w]:
        snake_direction = pygame.Vector2(0, -1)
      if keys[pygame.K_s]:
        snake_direction = pygame.Vector2(0, 1)
      elif keys[pygame.K_d]:
        snake_direction = pygame.Vector2(1, 0)
      elif keys[pygame.K_a]:
        snake_direction = pygame.Vector2(-1, 0)
    
  screen.fill('black')
  
  # food
  food_rect = pygame.Rect((food_pos.x * cell_size , food_pos.y * cell_size), (cell_size, cell_size))
  pygame.draw.rect(screen, (255, 0, 0), food_rect)

  # snake
  for cell in snake_body:
    snake_rect = pygame.Rect((cell.x * cell_size, cell.y * cell_size), (cell_size, cell_size))
    pygame.draw.rect(screen, (0, 255, 0), snake_rect, 0, 4)
  
  snake_body.insert(0, snake_body[0] + snake_direction)

  if not growing:
    snake_body = snake_body[:-1]
  else:
    growing = False
  
  # check for collisions
  if snake_body[0] == food_pos:
    growing = True 
    new_food_pos = gen_random_pos()
    
    while new_food_pos in snake_body:
      new_food_pos = gen_random_pos()
      
    food_pos = new_food_pos
    
    # lets make this grow!!!!
    # new_head = snake_body[0] + snake_direction
    # snake_body.insert(0, new_head)
    
  pygame.display.flip()
  clock.tick(10)
  
pygame.quit()
