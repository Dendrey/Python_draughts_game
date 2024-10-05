import pygame
from graphics import *
from Const import Const # это константы в нашей программе. Все они хранятся в файле Const.py
from Globals import Globals # это глобальные переменные в нашей программе. Все они хранятся в файле Globals.py
from collections import deque 

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLEDZOLOT =(238,232,170)
OHRA = (160,82,45)
GREEN = (34,139,34)

def AddAwailiblePositions():
  queue = deque()
  for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    if  (0 <= Globals.chosen_checker_x + 2*x <= 7) & (0 <= Globals.chosen_checker_y + 2*y <= 7):
      if (desk[Globals.chosen_checker_x + x][Globals.chosen_checker_y + y] != 0) & (desk[Globals.chosen_checker_x + 2*x][Globals.chosen_checker_y + 2*y] == 0):
        queue.append((Globals.chosen_checker_x + 2*x, Globals.chosen_checker_y + 2*y))
        Globals.awailible_positions.append((Globals.chosen_checker_x + 2*x, Globals.chosen_checker_y + 2*y))
  while len(queue) != 0:
    (x, y) = queue[0]
    queue.popleft()
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      if not (2*dx + x, 2*dy + y) in Globals.awailible_positions:
        if  (0 <= 2*dx + x <= 7) & (0 <= 2*dy + y <= 7):
          if (desk[2*dx + x][2*dy + y] == 0) & (desk[dx + x][dy + y] != 0):
            queue.append((2*dx + x, y + 2*dy))
            Globals.awailible_positions.append((2*dx + x, 2*dy + y))
  for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    if  (0 <= Globals.chosen_checker_x + x <= 7) & (0 <= Globals.chosen_checker_y + y <= 7):
      if (desk[Globals.chosen_checker_x + x][Globals.chosen_checker_y + y] == 0):
        Globals.awailible_positions.append((Globals.chosen_checker_x + x, Globals.chosen_checker_y + y))

def MoveChecker():
  mouse_x_coordinate = (Globals.mouse_pos[0] - Globals.x_offset) // Globals.size
  mouse_y_coordinate = (Globals.mouse_pos[1] - Globals.y_offset) // Globals.size
  if not (0 <= mouse_x_coordinate <= 7) & (0 <= mouse_y_coordinate <= 7):
    return
  if ((Globals.chosen_checker_x, Globals.chosen_checker_y) == (-1, -1)):
    color = desk[mouse_x_coordinate][mouse_y_coordinate]
    if ((Globals.last_turn) & (color == 1)) | ((not Globals.last_turn) & (color == -1)):
      (Globals.chosen_checker_x, Globals.chosen_checker_y) = (mouse_x_coordinate, mouse_y_coordinate)
      AddAwailiblePositions()
  else:
    if ((mouse_x_coordinate, mouse_y_coordinate) == (Globals.chosen_checker_x, Globals.chosen_checker_y)):
      (Globals.chosen_checker_x, Globals.chosen_checker_y) = (-1, -1)
      Globals.awailible_positions = []
      return
    if ((mouse_x_coordinate, mouse_y_coordinate) in Globals.awailible_positions):
      Globals.last_turn = not Globals.last_turn
      desk[mouse_x_coordinate][mouse_y_coordinate] = desk[Globals.chosen_checker_x][Globals.chosen_checker_y]
      desk[Globals.chosen_checker_x][Globals.chosen_checker_y] = 0
      (Globals.chosen_checker_x, Globals.chosen_checker_y) = (-1, -1)
      Globals.awailible_positions = []

def EventChecker(event):   # Получение информации о нажатых клавишах и положении мыши
  if event.type == pygame.MOUSEBUTTONDOWN:
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
      Globals.mouse_pos = pygame.mouse.get_pos()
      MoveChecker()
  if event.type == pygame.QUIT: # Действия при остановке программы
    Globals.running = False

def DrawTable(screen):
  screen.fill(Const.BLACK)
  Globals.screen_width, Globals.screen_height = pygame.display.get_surface().get_size()  # ширина игрового окна и высота игрового окна
  Globals.size = min(Globals.screen_height, Globals.screen_width) // 9
  Globals.x_offset = (Globals.screen_width - Globals.size * 8)  // 2
  Globals.y_offset = (Globals.screen_height - Globals.size * 8) // 2
  for x in range(8):
    for y in range(8):
      coordinates = [Globals.size*x + Globals.x_offset, Globals.size*y + Globals.y_offset, Globals.size, Globals.size]
      pygame.draw.rect(screen, BLEDZOLOT if (x + y) % 2 == 0 else OHRA, coordinates)
  for x in range(8):
    for y in range(8):
      if desk[x][y] == 1:
        image = pygame.transform.scale(pygame.image.load(("white-queen.png") if (x, y) == (Globals.chosen_checker_x, Globals.chosen_checker_y) else ("white-regular.png")).convert_alpha(), (Globals.size, Globals.size))
        rect = image.get_rect()
        rect.center = (Globals.x_offset + Globals.size // 2 + Globals.size * x, Globals.y_offset + Globals.size // 2 + Globals.size * y)
        screen.blit(image, (Globals.x_offset + Globals.size * x, Globals.y_offset + Globals.size * y))
      if desk[x][y] == -1:
        image = pygame.transform.scale(pygame.image.load(("black-queen.png") if (x, y) == (Globals.chosen_checker_x, Globals.chosen_checker_y) else ("black-regular.png")).convert_alpha(), (Globals.size, Globals.size))
        rect = image.get_rect()
        rect.center = (Globals.x_offset + Globals.size // 2 + Globals.size * x, Globals.y_offset + Globals.size // 2 + Globals.size * y)
        screen.blit(image, (Globals.x_offset + Globals.size * x, Globals.y_offset + Globals.size * y))
  for (x, y) in Globals.awailible_positions:
    coordinates = [Globals.size*x + Globals.x_offset + Globals.size // 2, Globals.size*y + Globals.y_offset + Globals.size // 2]
    pygame.draw.circle(screen, GREEN, coordinates, Globals.size / 5)
  pygame.display.flip()


if __name__ == '__main__':
  desk = [[1,1,1,0,0,0,0,0],[1,1,1,0,0,0,0,0],[1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,-1,-1,-1],[0,0,0,0,0,-1,-1,-1],[0,0,0,0,0,-1,-1,-1]]
  buttons = []
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE) #FULLSCREEN as a variant
  font = pygame.font.SysFont('Arial', 40)
  Globals.screen_width, Globals.screen_height = pygame.display.get_surface().get_size()  # ширина игрового окна и высота игрового окна
  Globals.size = min(Globals.screen_height, Globals.screen_width) // 9
  pygame.display.set_caption("Уголки")
  clock = pygame.time.Clock()
  while Globals.running:
    clock.tick(Const.FPS)
    DrawTable(screen)
    for event in pygame.event.get():
      EventChecker(event)