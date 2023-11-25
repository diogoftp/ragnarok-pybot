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
    self.player = Player(self.game, self.base())
    self.entity_list = EntityList(self.game.process, self.game)
    self.view = View(self.game)

  def base(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + WORLD_BASE_INTERMED_OFFSET, [WORLD_BASE_OFFSET])
