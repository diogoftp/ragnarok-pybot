from helpers.addresses import (
  WORLD_BASE_INTERMED_OFFSET,
  WORLD_BASE_OFFSET,
  PLAYER_BASE,
  PLAYER_NAME_OFFSET,
  PLAYER_CURRENT_HP_OFFSET,
  PLAYER_MAX_HP_OFFSET,
  PLAYER_CURRENT_SP_OFFSET,
  PLAYER_MAX_SP_OFFSET,
  PLAYER_COORDINATE_X_OFFSET,
  PLAYER_COORDINATE_Y_OFFSET,
  PLAYER_SCREEN_COORD_X_OFFSET,
  PLAYER_SCREEN_COORD_Y_OFFSET,
  MAP_NAME_OFFSET,
  STATE_OFFSET,
  IS_TALKING_TO_NPC_OFFSET,
  IS_IN_DELAY_OFFSET
)
from helpers.coordinate import Coordinate


class Player():
  state_map = {
    0: "idle",
    1: "walking",
    2: "attacking",
    5: "looting",
    6: "sitting",
    7: "delay",
    9: "attacking"
  }

  def __init__(self, game, world_base):
    self.game = game
    self.current_action = "idle"

  def base(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + WORLD_BASE_INTERMED_OFFSET, [WORLD_BASE_OFFSET, PLAYER_BASE])

  def name(self):
    return self.game.process.memory.read_str(self.game.base + PLAYER_NAME_OFFSET)

  def hp(self):
    return self.game.process.memory.read_u_int(self.game.base + PLAYER_CURRENT_HP_OFFSET)

  def max_hp(self):
    return self.game.process.memory.read_u_int(self.game.base + PLAYER_MAX_HP_OFFSET)

  def hp_percent(self):
    return self.hp() / self.max_hp()

  def sp(self):
    return self.game.process.memory.read_u_int(self.game.base + PLAYER_CURRENT_SP_OFFSET)

  def max_sp(self):
    return self.game.process.memory.read_u_int(self.game.base + PLAYER_MAX_SP_OFFSET)

  def sp_percent(self):
    return self.sp() / self.max_sp()

  def map_name(self):
    name = self.game.process.memory.read_str(self.game.base + MAP_NAME_OFFSET)

    if name:
      return name.split(".rsw")[0]

    return None

  def coordinates(self):
    x = self.game.process.memory.read_u_int(self.game.base + PLAYER_COORDINATE_X_OFFSET)
    y = self.game.process.memory.read_u_int(self.game.base + PLAYER_COORDINATE_Y_OFFSET)
    return Coordinate(x, y)

  def screen_coordinates(self):
    x = self.game.process.memory.read_u_int(self.base() + PLAYER_SCREEN_COORD_X_OFFSET)
    y = self.game.process.memory.read_u_int(self.base() + PLAYER_SCREEN_COORD_Y_OFFSET)
    return Coordinate(x, y, _type="screen")

  def state(self):
    return self.game.process.memory.read_u_int(self.base() + STATE_OFFSET)

  def is_talking_to_npc(self):
    return bool(self.game.process.memory.read_u_int(self.game.world.intermed_base() + IS_TALKING_TO_NPC_OFFSET))

  def is_in_delay(self):
    return bool(self.game.process.memory.read_u_int(self.game.base + IS_IN_DELAY_OFFSET))
