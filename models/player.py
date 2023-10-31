from helpers.addresses import (
  GAME_BASE,
  # PLAYER_BASE,
  PLAYER_NAME_OFFSET,
  PLAYER_CURRENT_HP_OFFSET,
  PLAYER_MAX_HP_OFFSET,
  PLAYER_COORDINATE_X_OFFSET,
  PLAYER_COORDINATE_Y_OFFSET,
  MAP_NAME_OFFSET
)


class Player():
  def __init__(self, process, world_base):
    self.process = process
    # self.base = self.process.memory.read_ptr(world_base, PLAYER_BASE)

  def name(self):
    return self.process.memory.read_str(GAME_BASE + PLAYER_NAME_OFFSET)

  def hp(self):
    return self.process.memory.read_u_int(GAME_BASE + PLAYER_CURRENT_HP_OFFSET)

  def max_hp(self):
    return self.process.memory.read_u_int(GAME_BASE + PLAYER_MAX_HP_OFFSET)

  def map_name(self):
    name = self.process.memory.read_str(GAME_BASE + MAP_NAME_OFFSET)

    if name:
      return name.split(".rsw")[0]

    return None

  def coordinates(self):
    return (self.process.memory.read_u_int(GAME_BASE + PLAYER_COORDINATE_X_OFFSET), self.process.memory.read_u_int(GAME_BASE + PLAYER_COORDINATE_Y_OFFSET))
