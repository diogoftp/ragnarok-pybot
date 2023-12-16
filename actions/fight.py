import math
from time import sleep

MIN_DISTANCE_TO_ATTACK = 7
MONSTERS_NOT_TO_ATTACK = [1081]


class Fight():
  def __init__(self, game):
    self.game = game
    self.fighting_entity = None
    self.monster_list = []

  def update_monster_list(self):
    entity_list = list(self.game.world.entity_list)
    self.monster_list = []

    for entity in entity_list:
      if entity.id() > 999 and entity.id() < 50000 and entity.id() not in MONSTERS_NOT_TO_ATTACK:
        self.monster_list.append(entity)

  def find_target(self):
    self.fighting_entity = None

    if len(self.monster_list) == 0:
      return

    closest = self.monster_list[0]
    player_coords = self.game.world.player.coordinates()
    closest_distance = player_coords.distance_to(closest.coords())

    for monster in self.monster_list:
      distance = player_coords.distance_to(monster.coords())
      if distance < closest_distance:
        closest = monster
        closest_distance = distance

    self.fighting_entity = closest

  def fight(self):
    entity_list = list(self.game.world.entity_list)

    if (self.fighting_entity is None) or (not any(self.fighting_entity.base == entity.base for entity in entity_list)):
      self.fighting_entity = None
      return

    if (self.fighting_entity is not None) and (self.game.world.player.state() not in [2, 5, 7, 9]):
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.Z)
      self.game.input.mouse.set_game_mouse_pos(self.fighting_entity.screen_coords(), game_coords=False)
      self.game.input.mouse.send_click()
      sleep(0.1)

  def distance_to_entity(self):
    if self.fighting_entity is None:
      return

    return self.game.world.player.coordinates().distance_to(self.fighting_entity.coords())
