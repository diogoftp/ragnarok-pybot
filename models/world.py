from helpers.addresses import (
  GAME_BASE,
  WORLD_BASE_INTERMED_OFFSET,
  WORLD_BASE_OFFSET,
  VIEW_OFFSET
)

from models.player import Player
from models.entity import EntityList
from models.view import View


class World():
  def __init__(self, process):
    self.process = process

    world_base_addr = GAME_BASE + WORLD_BASE_INTERMED_OFFSET
    world_base = self.process.memory.read_ptr(world_base_addr)
    self.base = self.process.memory.read_ptr(world_base, WORLD_BASE_OFFSET)
    self.view_base = self.process.memory.read_ptr(world_base, VIEW_OFFSET)

    self.player = Player(self.process, self.base)
    self.entity_list = EntityList(self.process, self.base)
    self.view = View(self.process, self.view_base)
