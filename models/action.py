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
  def __init__(self, game):
    self.game = game
    self.fighting_entity = None

  def find_target(self):
    if self.game.world.player.current_action != "idle":
      return

    self.game.world.player.current_action = "finding_target"
    self.game.world.entity_list.update_array()

    for entity in self.game.world.entity_list.entity_array:
      if entity.id() > 999:
        self.fighting_entity = entity
        return self.fight()

    self.game.world.player.current_action = "idle"

  def fight(self):
    self.game.world.player.current_action = "fighting"
    self.game.world.entity_list.update_array()

    if (self.fighting_entity is None) or (not any(self.fighting_entity.base == entity.base for entity in self.game.world.entity_list.entity_array)):
      self.game.world.player.current_action = "idle"
      self.fighting_entity = None
      return

    if (self.fighting_entity is not None) and (self.game.world.player.state() != 2):
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.Z)
      self.game.input.mouse.set_game_mouse_pos(self.fighting_entity.coords())
      self.game.input.mouse.send_click()
      sleep(1)
