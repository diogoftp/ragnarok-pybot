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
    self.process = Process("ragna4th.exe", Process.PROCESS_VM_OPERATION | Process.PROCESS_VM_READ | Process.PROCESS_VM_WRITE)
    self.world = World(self)
    self.window = Window(self)
    self.input = Input(self)
    self.macro = Macro(self)
    self.map = Map(self)
    self.action = Action(self)
    self.running = True

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
    game_string += f"Macro status: {self.macro.active}\n"
    game_string += str(self.world.entity_list)
    return game_string
