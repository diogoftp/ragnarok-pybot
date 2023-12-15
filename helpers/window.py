import win32gui
import win32process
import math

from helpers.map import CELL_PIXEL_SIZE
from helpers.coordinate import Coordinate

WINDOW_NAME = "4th | Gepard Shield 3.0 (^-_-^)"


class Window():
  def __init__(self, game):
    self.game = game
    self.handle = self.get_window_handle()

  def get_window_handle(self):
    windows = []
    win32gui.EnumWindows(lambda handle, _: windows.append(handle), None)

    for handle in windows:
      _, process_id = win32process.GetWindowThreadProcessId(handle)
      window_name = win32gui.GetWindowText(handle)

      if (process_id == self.game.process.pid) and (window_name == WINDOW_NAME):
        return handle

    raise RuntimeError("Failed to get window handle")

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

  def translate_to_screen_coords(self, player_coords, target_coords):
    # Distance vector
    distance_x, distance_y = (target_coords.x - player_coords.x, -(target_coords.y - player_coords.y))

    # Rotate the distance vector acording to the horizontal camera angle rotation
    angle_radians = math.radians(self.game.world.view.horizontal_camera_angle())
    target_x = distance_x * math.cos(angle_radians) + distance_y * math.sin(angle_radians)
    target_y = -distance_x * math.sin(angle_radians) + distance_y * math.cos(angle_radians)

    # Calculate the distance in pixels
    center_x, center_y = self.center()
    target_x = center_x + target_x * CELL_PIXEL_SIZE[0]
    target_y = center_y + target_y * CELL_PIXEL_SIZE[1]

    return Coordinate(int(round(target_x)), int(round(target_y)), _type="screen")
