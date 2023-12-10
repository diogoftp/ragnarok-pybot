from time import sleep

from helpers.map import TARGET_MAP, TOWN

class Heal():
  def __init__(self, game):
    self.game = game

  def should_heal(self):
    return self.game.world.player.hp_percent() < 0.2 or self.game.world.player.sp_percent() < 0.1

  def heal(self):
    self.game.world.player.current_action = "healing"

    if self.game.macro.active:
      self.game.macro.stop()

    # Go to town
    if (self.game.world.player.map_name() == TARGET_MAP) and self.should_heal():
      self.game.world.enable_chat_bar()
      sleep(0.3)
      self.game.world.write_to_chat_bar("@go 18")
      sleep(0.8)
      self.game.world.disable_chat_bar()
      sleep(0.1)

    # Talk to healer
    if (self.game.world.player.map_name() == TOWN) and self.should_heal():
      self.game.world.entity_list.update_array()
      for entity in self.game.world.entity_list:
        if entity.name() == "f_leedsh":
          self.game.input.mouse.set_game_mouse_pos(entity.screen_coords(), game_coords=False)
          self.game.input.mouse.send_click()
      sleep(1)

    # Go back to map
    if (self.game.world.player.map_name() == TOWN) and not self.should_heal():
      self.game.world.entity_list.update_array()
      for entity in self.game.world.entity_list:
        if entity.name() == "ep18_miriam":
          self.game.input.mouse.set_game_mouse_pos(entity.screen_coords(), game_coords=False)
          self.game.input.mouse.send_click()
          sleep(1)
          self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.ENTER)
      sleep(1)

    if (self.game.world.player.map_name() == TARGET_MAP) and not self.should_heal():
      self.game.macro.start()
      self.game.world.player.current_action = "idle"
