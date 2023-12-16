from time import sleep

from helpers.map import TARGET_MAP, TOWN

class Heal():
  def __init__(self, game):
    self.game = game

  def should_heal(self):
    if self.game.world.player.map_name() == TOWN:
      hp_threshold = 1
      sp_threshold = 1
    else:
      hp_threshold = 0.2
      sp_threshold = 0.1

    return self.game.world.player.hp_percent() < hp_threshold or self.game.world.player.sp_percent() < sp_threshold

  def heal(self):
    if self.game.macro.active:
      self.game.macro.stop()

    # Go to town
    if (self.game.world.player.map_name() == TARGET_MAP) and self.should_heal():
      self.game.world.enable_chat_bar()
      sleep(0.3)
      self.game.world.write_to_chat_bar("@go 18")
      sleep(0.8)
      self.game.world.disable_chat_bar()
      sleep(0.5)
      return

    # Talk to healer
    if (self.game.world.player.map_name() == TOWN) and self.should_heal():
      for entity in self.game.world.entity_list:
        if entity.name() == "f_leedsh":
          self.game.input.mouse.set_game_mouse_pos(entity.screen_coords(), game_coords=False)
          sleep(0.1)
          self.game.input.mouse.send_click()
          break
      sleep(0.5)
      return

    # Go back to map
    if (self.game.world.player.map_name() == TOWN) and not self.should_heal():
      for entity in self.game.world.entity_list:
        if entity.name() == "ep18_miriam":
          self.game.input.mouse.set_game_mouse_pos(entity.screen_coords(), game_coords=False)
          sleep(0.1)
          self.game.input.mouse.send_click()
          sleep(0.5)
          self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.ENTER)
          break
      sleep(0.5)
      return

    if (self.game.world.player.map_name() == TARGET_MAP) and not self.should_heal():
      self.game.world.disable_chat_bar()
      self.game.macro.start()
      return
