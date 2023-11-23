import os
from time import sleep

from helpers.process import Process
from helpers.window import Window
from helpers.input import Input
from helpers.map import Map
from models.world import World
from models.player import Player
from models.macro import Macro
from models.action import Action


class Game():
  def __init__(self):
    self.process = Process()
    self.base = self.process.base
    self.running = True
    self.active = True
    self.world = World(self)
    self.window = Window(self)
    self.input = Input(self)
    self.macro = Macro(self)
    self.map = Map(self)
    self.action = Action(self)
    self.world.view.set_default_camera_angles()

  def __str__(self):
    coords = self.world.player.coordinates()
    game_string = ""
    game_string += f"Player name: {self.world.player.name()} ({self.world.player.current_action})\n"
    game_string += f"Player HP: {self.world.player.hp()}/{self.world.player.max_hp()}\n"
    game_string += f"Player state: {self.world.player.state()} ({self.world.player.state_map.get(self.world.player.state(), "unknown")})\n"
    game_string += f"Map name: {self.world.player.map_name()} {coords}\n"
    game_string += f"Is cell walkable? {self.map.walkable(coords)} (type {self.map.read_coords(coords)}) ({self.map.width}, {self.map.height})\n"
    game_string += f"Mouse pos: {self.input.mouse.get_current_mouse_pos()}\n"
    game_string += f"View: {self.world.view.horizontal_camera_angle()}, {self.world.view.vertical_camera_angle()}, {self.world.view.camera_zoom()}\n"
    game_string += f"Macro active?: {self.macro.active}\n"
    game_string += f"Bot active?: {self.active}\n"
    game_string += f"Currently fighting: {self.action.fighting_entity}\n"
    game_string += str(self.world.entity_list)
    return game_string

  def loop(self):
    while(self.running):
      self.refresh_game_data()
      self.print_game_state()
      self.input.keyboard.listen_keys()

      if self.active:
        self.execute_actions()

      sleep(0.1)

    self.macro.stop()

  def refresh_game_data(self):
    self.map.reload()
    self.map.check_is_allowed_map()

  def print_game_state(self):
    os.system("cls")
    print(self)

  def execute_actions(self):
    if self.world.player.current_action == "idle":
      self.action.find_target()
    elif self.world.player.current_action == "fighting":
      self.action.fight()
    elif self.world.player.current_action == "finding_target":
      pass

  def toggle_bot(self, active=None):
    if active is None:
      self.active = not self.active
    elif active:
      self.active = True
    else:
      self.active = False

    if not self.active:
      self.world.view.set_default_camera_angles()
