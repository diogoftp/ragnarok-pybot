import math
from time import sleep


class Fight():
  def __init__(self, game):
    self.game = game
    self.fighting_entity = None
    self.distance_to_entity = None

  def find_target(self):
    self.game.world.entity_list.update_array()

    if len(self.game.world.entity_list.entity_array) < 1:
      return

    monsters = []

    for entity in self.game.world.entity_list.entity_array:
      if entity.id() > 999 and entity.id() < 50000:
        monsters.append(entity)

    # find closest monster
    if len(monsters) == 0:
      return

    closest = monsters[0]
    player_coords = self.game.world.player.coordinates()
    closest_distance = player_coords.distance_to(closest.coords())

    for monster in monsters:
      distance = player_coords.distance_to(monster.coords())
      if distance < closest_distance:
        closest = monster
        closest_distance = distance

    self.distance_to_entity = closest_distance
    self.fighting_entity = closest

  def fight(self):
    self.game.world.entity_list.update_array()
    if self.fighting_entity is None:
      self.find_target()

    if (self.fighting_entity is None) or (not any(self.fighting_entity.base == entity.base for entity in self.game.world.entity_list.entity_array)):
      self.fighting_entity = None
      self.distance_to_entity = None
      return

    if (self.fighting_entity is not None) and (self.game.world.player.state() not in [2, 5, 7, 9]):
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.Z)
      self.game.input.mouse.set_game_mouse_pos(self.fighting_entity.screen_coords(), game_coords=False)
      self.game.input.mouse.send_click()
      sleep(0.1)
