from helpers.process import Process
from models.world import World
from models.player import Player
from models.window import Window
from models.macro import Macro
from helpers.input import Input
from helpers.map import Map
from time import sleep
import os

from models.entity import EntityList, Entity


class Bot():
  def __init__(self):
    self.process = Process("ragna4th.exe", Process.PROCESS_VM_READ)
    self.world = World(self.process)
    self.window = Window(self.world.player)
    self.input = Input(self.window)
    self.macro = Macro(self.window, self.input)
    self.map = Map(self.world.player)
    self.start_game_loop()

  def print_game_state(self):
    print(f"PLayer name: {self.world.player.name()}")
    print(f"Player HP: {self.world.player.hp()}/{self.world.player.max_hp()}")
    coords = self.world.player.coordinates()
    print(f"Map name: {self.world.player.map_name()} {coords}")
    print(f"Is cell walkable? {self.map.walkable(coords)} (type {self.map.read_coords(coords)}) ({self.map.width}, {self.map.height})")
    print(f"Mouse pos: {self.input.mouse.get_current_mouse_pos()}")
    print(f"View: {self.world.view.horizontal_camera_angle()}, {self.world.view.vertical_camera_angle()}, {self.world.view.camera_zoom()}")
    print(self.world.entity_list)

  def start_game_loop(self):
    while(True):
      if self.input.keyboard.pressed(self.input.keyboard.KILL_SWITCH_KEY):
        break

      os.system("cls")
      self.print_game_state()
      self.map.reload()
      self.macro.loop()
      sleep(0.1)

    self.macro.stop()