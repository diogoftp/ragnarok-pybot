from time import sleep

from helpers.addresses import (
  PLAYER_BASE,
  PLAYER_NAME_OFFSET,
  PLAYER_CURRENT_HP_OFFSET,
  PLAYER_MAX_HP_OFFSET,
  PLAYER_COORDINATE_X_OFFSET,
  PLAYER_COORDINATE_Y_OFFSET,
  MAP_NAME_OFFSET,
  STATE_OFFSET
)
from actions.heal import Heal
from actions.restock_arrow import RestockArrow
from actions.walk import Walk
from actions.fight import Fight


class Action():
  def __init__(self, game):
    self.game = game
    self.heal = Heal(self.game)
    self.restock_arrow = RestockArrow(self.game)
    self.walk = Walk(self.game)
    self.fight = Fight(self.game)
