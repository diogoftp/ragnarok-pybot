import math

from helpers.addresses import (
  VIEW_OFFSET,
  WORLD_BASE_INTERMED_OFFSET,
  CAMERA_ANGLE_HORIZONTAL,
  CAMERA_ANGLE_VERTICAL,
  CAMERA_ZOOM
)

DEFAULT_CAMERA_ANGLE_HORIZONTAL = 0
DEFAULT_CAMERA_ANGLE_VERTICAL = -50
DEFAULT_CAMERA_ZOOM = 400


class View():
  def __init__(self, game):
    self.game = game

  def base(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + WORLD_BASE_INTERMED_OFFSET, [VIEW_OFFSET])

  def horizontal_camera_angle(self):
    value = self.game.process.memory.read_float(self.base() + CAMERA_ANGLE_HORIZONTAL)

    if math.isnan(value):
      return None

    return int(value)

  def vertical_camera_angle(self):
    value = self.game.process.memory.read_float(self.base() + CAMERA_ANGLE_VERTICAL)

    if math.isnan(value):
      return None

    return int(value)

  def camera_zoom(self):
    return self.game.process.memory.read_float(self.base() + CAMERA_ZOOM)

  def set_default_camera_angles(self):
    self.game.process.memory.write_float(DEFAULT_CAMERA_ANGLE_HORIZONTAL, self.base() + CAMERA_ANGLE_HORIZONTAL)
    self.game.process.memory.write_float(DEFAULT_CAMERA_ANGLE_VERTICAL, self.base() + CAMERA_ANGLE_VERTICAL)
    self.game.process.memory.write_float(DEFAULT_CAMERA_ZOOM, self.base() + CAMERA_ZOOM)
