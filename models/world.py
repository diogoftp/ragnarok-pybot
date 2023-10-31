from helpers.addresses import (
  GAME_BASE,
  WORLD_BASE_INTERMED_OFFSET,
  WORLD_BASE_OFFSET
)

from models.player import Player
from models.entity import EntityList


class World():
  def __init__(self, process):
    self.process = process

    world_base_addr = GAME_BASE + WORLD_BASE_INTERMED_OFFSET
    world_base = self.process.memory.read_ptr(world_base_addr)
    self.base = self.process.memory.read_ptr(world_base, WORLD_BASE_OFFSET)

    self.player = Player(self.process, self.base)
    self.entity_list = EntityList(self.process, self.base)
