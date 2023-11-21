from helpers.addresses import (
  WORLD_BASE_INTERMED_OFFSET,
  WORLD_BASE_OFFSET,
  VIEW_OFFSET
)
from models.player import Player
from models.entity import EntityList
from models.view import View


class World():
  def __init__(self, game):
    self.game = game

    world_base_addr = self.game.base + WORLD_BASE_INTERMED_OFFSET
    world_base = self.game.process.memory.read_ptr(world_base_addr)
    self.base = self.game.process.memory.read_ptr(world_base, WORLD_BASE_OFFSET)
    self.view_base = self.game.process.memory.read_ptr(world_base, VIEW_OFFSET)

    self.player = Player(self.game, self.base)
    self.entity_list = EntityList(self.game.process, self.base)
    self.view = View(self.game, self.view_base)
