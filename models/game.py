import os
import ctypes
from time import sleep
from pygame import mixer

from helpers.process import Process
from helpers.window import Window
from helpers.input import Input
from helpers.map import Map
from actions.walk import Walk
from models.world import World
from models.player import Player
from models.macro import Macro
from models.action import Action
from models.inventory import Inventory
from actions.fight import MIN_DISTANCE_TO_ATTACK


class Game():
  def __init__(self):
    self.process = Process()
    self.base = self.process.base
    self.running = True
    self.active = False
    self.world = World(self)
    self.inventory = Inventory(self, self.process)
    self.window = Window(self)
    self.input = Input(self)
    self.macro = Macro(self)
    self.map = Map(self)
    self.action = Action(self)
    self.world.view.set_default_camera_angles()

  def __str__(self):
    coords = self.world.player.coordinates()
    game_string = ""
    game_string += f"Player name: {self.world.player.name()} ({self.world.player.current_action}), walking to {self.action.walk.destination}\n"
    game_string += f"Player HP and SP: {self.world.player.hp()}/{self.world.player.max_hp()} | {self.world.player.sp()}/{self.world.player.max_sp()}\n"
    game_string += f"Player state: {self.world.player.state()} ({self.world.player.state_map.get(self.world.player.state(), "unknown")})\n"
    game_string += f"Map name: {self.world.player.map_name()} {coords} {self.world.player.screen_coordinates()}\n"
    game_string += f"Is cell walkable? {self.map.walkable(coords)} (type {self.map.read_coords(coords)}) ({self.map.width}, {self.map.height})\n"
    game_string += f"Is talking to npc? {self.world.player.is_talking_to_npc()}\n"
    game_string += f"Mouse pos: {self.input.mouse.get_current_mouse_pos()}. Locked? {self.input.mouse.mouse_blocker.is_running()}\n"
    game_string += f"View: {self.world.view.horizontal_camera_angle()}, {self.world.view.vertical_camera_angle()}, {self.world.view.camera_zoom()}\n"
    game_string += f"Macro active?: {self.macro.active}\n"
    game_string += f"Bot active?: {self.active}\n"
    game_string += f"Currently fighting: {self.action.fight.fighting_entity}\n"
    game_string += str(self.world.entity_list)
    game_string += str(self.inventory)
    return game_string

  def loop(self):
    while(self.running):
      self.refresh_game_data()
      self.print_game_state()
      self.input.keyboard.listen_keys()
      self.check_safety_conditions()

      if self.active or self.macro.active:
        self.world.player.current_action = self.set_current_state()
        self.execute_actions()

      if self.world.player.current_action == "healing":
        self.action.heal.heal()

      sleep(0.1)

    self.macro.stop()

  def refresh_game_data(self):
    self.map.reload()
    self.action.fight.update_monster_list()

  def print_game_state(self):
    os.system("cls")
    print(self)

  def check_safety_conditions(self):
    self.map.check_is_allowed_map()

    if self.world.player.is_talking_to_npc() and (not self.map.is_safe_map()):
      self.macro.stop()
      self.active = False
      mixer.init()
      mixer.music.load("cops.mp3")
      mixer.music.play()
      sleep(1)
      return

  def set_current_state(self):
    if self.action.heal.should_heal():
      return "healing"
    if self.action.restock_arrow.should_restock():
      return "restocking_arrow"
    if not self.macro.active and len(self.map.map) > 0 and len(self.action.fight.monster_list) == 0:
      return "walking"
    if not self.macro.active and len(self.action.fight.monster_list) > 0 and self.action.fight.fighting_entity is None:
      return "finding_monster"
    if not self.macro.active and len(self.map.map) > 0 and self.action.fight.fighting_entity is not None and self.action.fight.distance_to_entity() > MIN_DISTANCE_TO_ATTACK:
      return "walking_to_monster"
    if not self.macro.active and self.action.fight.fighting_entity is not None and self.action.fight.distance_to_entity() <= MIN_DISTANCE_TO_ATTACK:
      return "fighting"

    return "idle"

  def execute_actions(self):
    if self.world.player.current_action == "restocking_arrow":
      self.action.restock_arrow.restock()
    if self.world.player.current_action == "walking":
      self.action.walk.step()
    if self.world.player.current_action == "finding_monster":
      self.action.fight.find_target()
    if self.world.player.current_action == "walking_to_monster":
      self.action.walk.calculate_route_to(self.action.fight.fighting_entity.coords())
      sleep(0.1)
      self.action.walk.step()
      sleep(0.1)
    if self.world.player.current_action == "fighting":
      self.action.fight.fight()

  def toggle_bot(self, active=None):
    if active is None:
      self.active = not self.active
    elif active:
      self.active = True
    else:
      self.active = False

    if self.active:
      self.world.view.set_default_camera_angles()
