from helpers.addresses import (
  CAMERA_ANGLE_HORIZONTAL,
  CAMERA_ANGLE_VERTICAL,
  CAMERA_ZOOM
)


class View():
  def __init__(self, process, base):
    self.process = process
    self.base = base

  def horizontal_camera_angle(self):
    return int(self.process.memory.read_float(self.base + CAMERA_ANGLE_HORIZONTAL))

  def vertical_camera_angle(self):
    return int(self.process.memory.read_float(self.base + CAMERA_ANGLE_VERTICAL))

  def camera_zoom(self):
    return self.process.memory.read_float(self.base + CAMERA_ZOOM)
