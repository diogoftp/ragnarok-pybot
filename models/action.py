from helpers.addresses import (
  GAME_BASE,
  PLAYER_BASE,
  PLAYER_NAME_OFFSET,
  PLAYER_CURRENT_HP_OFFSET,
  PLAYER_MAX_HP_OFFSET,
  PLAYER_COORDINATE_X_OFFSET,
  PLAYER_COORDINATE_Y_OFFSET,
  MAP_NAME_OFFSET,
  STATE_OFFSET
)
from time import sleep


class Action():
  def __init__(self, world, _input, _map):
    self.world = world
    self.input = _input
    self.map = _map
    self.fighting_entity = None

  def find_target(self):
    if self.world.player.current_action != "idle":
      return

    self.world.player.current_action = "finding_target"
    self.world.entity_list.update_array()

    for entity in self.world.entity_list.entity_array:
      if entity.id() > 999:
        self.fighting_entity = entity
        return self.fight()

    self.world.player.current_action = "idle"

  def fight(self):
    self.world.player.current_action = "fighting"
    self.world.entity_list.update_array()

    if (self.fighting_entity is None) or (not any(self.fighting_entity.base == entity.base for entity in self.world.entity_list.entity_array)):
      self.world.player.current_action = "idle"
      self.fighting_entity = None
      return

    if (self.fighting_entity is not None) and (self.world.player.state() != 2):
      self.input.keyboard.send_key(self.input.keyboard.VKEYS.Z)
      self.input.mouse.set_game_mouse_pos(self.fighting_entity.coords())
      self.input.mouse.send_click()
      sleep(1)
