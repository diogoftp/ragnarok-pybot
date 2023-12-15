import os
import ctypes
import math
import random

from helpers.coordinate import Coordinate

WALKABLE_BLOCKS = [0, 3]


class PathMetadata(ctypes.Structure):
  _fields_ = [("path", ctypes.POINTER(ctypes.c_int32)), ("size", ctypes.c_size_t)]

class Walk():
  def __init__(self, game):
    self.game = game
    self.last_action = self.game.world.player.current_action
    self.lib = self.load_library()
    self.current_path = []
    self.destination = None

  def load_library(self):
    lib_path = os.path.abspath("./helpers/shortest_path.dll")
    return ctypes.windll.LoadLibrary(lib_path)

  def calculate_random_coordinate(self):
    if len(self.game.map.map) == 0:
      return None

    random_coord = Coordinate(random.randrange(self.game.map.width), random.randrange(self.game.map.height))

    while not self.game.map.walkable(random_coord):
      random_coord = Coordinate(random.randrange(self.game.map.width), random.randrange(self.game.map.height))

    return random_coord

  def calculate_route_to(self, dest):
    if len(self.game.map.map) == 0:
      self.current_path = []
      return

    map_array = (ctypes.c_int32 * len(self.game.map.map))(*self.game.map.map)
    player_coords = self.game.world.player.coordinates()
    self.lib.My_ShortestPath.restype = PathMetadata
    result = self.lib.My_ShortestPath(map_array, self.game.map.width, self.game.map.height, player_coords.x, player_coords.y, dest.x, dest.y)
    self.destination = dest
    self.current_path = [result.path[i:i+2] for i in range(0, result.size, 2)]

  def step(self):
    if len(self.current_path) == 0:
      self.destination = None
      self.destination = self.calculate_random_coordinate()
      self.calculate_route_to(self.destination)
      return

    player_coords = self.game.world.player.coordinates()
    current_dest = Coordinate(self.current_path[0][0], self.current_path[0][1])
    distance = player_coords.distance_to(current_dest)

    # Check if is close enough to current step
    if distance <= 3:
      del self.current_path[:3]

    if len(self.current_path) > 0:
      # Walk
      self.game.input.mouse.set_game_mouse_pos(Coordinate(self.current_path[0][0], self.current_path[0][1]), game_coords=True)
      self.game.input.mouse.send_click()
