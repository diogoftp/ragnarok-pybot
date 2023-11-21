from helpers.addresses import (
  CAMERA_ANGLE_HORIZONTAL,
  CAMERA_ANGLE_VERTICAL,
  CAMERA_ZOOM
)

DEFAULT_CAMERA_ANGLE_HORIZONTAL = 0
DEFAULT_CAMERA_ANGLE_VERTICAL = -50
DEFAULT_CAMERA_ZOOM = 400


class View():
  def __init__(self, game, base):
    self.game = game
    self.base = base

  def horizontal_camera_angle(self):
    return int(self.game.process.memory.read_float(self.base + CAMERA_ANGLE_HORIZONTAL))

  def vertical_camera_angle(self):
    return int(self.game.process.memory.read_float(self.base + CAMERA_ANGLE_VERTICAL))

  def camera_zoom(self):
    return self.game.process.memory.read_float(self.base + CAMERA_ZOOM)

  def set_default_camera_angles(self):
    self.game.process.memory.write_float(DEFAULT_CAMERA_ANGLE_HORIZONTAL, self.base + CAMERA_ANGLE_HORIZONTAL)
    self.game.process.memory.write_float(DEFAULT_CAMERA_ANGLE_VERTICAL, self.base + CAMERA_ANGLE_VERTICAL)
    self.game.process.memory.write_float(DEFAULT_CAMERA_ZOOM, self.base + CAMERA_ZOOM)
