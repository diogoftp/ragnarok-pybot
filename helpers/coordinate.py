import math

from helpers.window import CELL_PIXEL_SIZE


class Coordinate():
  def __init__(self, x, y, _type="game"):
    self.x = x
    self.y = y
    self.type = _type

  def __str__(self):
    return f"({self.x}, {self.y}, {self.type})"

  def distance_to(self, target):
    dx = self.x - target.x
    dy = self.y - target.y

    return math.sqrt(dx**2 + dy**2)

  def to_screen(self, game):
    if self.type == "screen":
      return
    else:
      pos = game.window.translate_to_screen_coords(game.world.player.coordinates(), self)
      self.x = pos.x
      self.y = pos.y
      self.type = "game"

  def to_game(self):
    pass
