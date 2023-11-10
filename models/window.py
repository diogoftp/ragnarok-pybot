import win32gui
from helpers.map import CELL_PIXEL_SIZE


class Window():
  def __init__(self, player):
    self.handle = win32gui.FindWindow(None, "4th | Gepard Shield 3.0 (^-_-^)")
    self.player = player

  def get_rect(self):
    return win32gui.GetWindowRect(self.handle)

  def center(self):
    game_window = self.get_rect()
    width = game_window[2] - game_window[0]
    height = game_window[3] - game_window[1]

    return (int(width / 2), int(height / 2))

  def skill_center(self):
    center = self.center()
    x = center[0] - (CELL_PIXEL_SIZE[0] / 2)
    y = center[1] - (CELL_PIXEL_SIZE[1] / 2)

    return (int(x), int(y))

  def player_coords(self):
    return (self.player.coordinates()[0], self.player.coordinates()[1])

  def translate_to_screen_coords(self, target_coords):
    player_coords = self.player_coords()
    game_coords_diff = (target_coords[0] - player_coords[0], target_coords[1] - player_coords[1])
    center = self.center()

    x = center[0] + game_coords_diff[0] * CELL_PIXEL_SIZE[0]
    y = center[1] - game_coords_diff[1] * CELL_PIXEL_SIZE[1]

    return x, y