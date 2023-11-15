class Coordinate():
  def __init__(x, y, _type="game"):
    self.x = x
    self.y = y
    self.type = _type

  def __str__(self):
    return f"({self.x}, {self.y}, {self.type})"

  def to_screen(self, game):
    if self.type == "screen":
      return
    else:
      player_x, player_y = game.player.coordinates()
      # Distance vector from center
      distance_x, distance_y = (self.x - player_x, -(self.y - player_y))

      # Rotate the distance vector acording to the horizontal camera angle rotation
      angle_radians = math.radians(game.view.horizontal_camera_angle())
      target_x = distance_x * math.cos(angle_radians) + distance_y * math.sin(angle_radians)
      target_y = -distance_x * math.sin(angle_radians) + distance_y * math.cos(angle_radians)

      # Calculate the distance in pixels
      center_x, center_y = self.center()
      target_x = center_x + target_x * CELL_PIXEL_SIZE[0]
      target_y = center_y + target_y * CELL_PIXEL_SIZE[1]

      self.x = int(round(target_x))
      self.y = int(round(target_y))
      self.type = "game"

  def to_game(self):
    pass
