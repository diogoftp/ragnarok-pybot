from helpers.process import Process
from models.world import World
from models.player import Player
from models.macro import Macro
from models.action import Action
from helpers.window import Window
from helpers.input import Input
from helpers.map import Map
from time import sleep
import os

from models.entity import EntityList, Entity


class Bot():
  def __init__(self):
    self.process = Process("ragna4th.exe", Process.PROCESS_VM_OPERATION | Process.PROCESS_VM_READ | Process.PROCESS_VM_WRITE)
    self.world = World(self.process)
    self.window = Window(self.world.view)
    self.input = Input(self.window, self.world.player)
    self.macro = Macro(self.window, self.input)
    self.map = Map(self.world.player)
    self.action = Action(self.world, self.input, self.map)
    self.start_game_loop()

  def print_game_state(self):
    print(f"Player name: {self.world.player.name()} ({self.world.player.current_action})")
    print(f"Player HP: {self.world.player.hp()}/{self.world.player.max_hp()}")
    print(f"Player state: {self.world.player.state()} ({self.world.player.state_map.get(self.world.player.state(), "unknown")})")
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

      if self.world.player.current_action == "idle":
        self.action.find_target()
      elif self.world.player.current_action == "fighting":
        self.action.fight()
      elif self.world.player.current_action == "finding_target":
        pass

      sleep(0.1)

    self.macro.stop()
