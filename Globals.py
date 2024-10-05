import pygame
class Globals:
  running = True
  screen_width = 0
  screen_height = 0
  size = 0
  x_offset = 0
  y_offset = 0
  is_chosen = False
  all_sprites = pygame.sprite.Group()
  mouse_pos = (0,0)
  chosen_checker_x = -1
  chosen_checker_y = -1
  awailible_positions = []
  last_turn = True