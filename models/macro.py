from threading import Thread
from time import sleep
import random


class Macro():
  def __init__(self, game):
    self.game = game
    self.active = False
    self.last_active = self.active
    self.start()

  def toggle(self):
    self.last_active = not self.active

    if self.active:
      self.stop()
    else:
      self.start(from_user=True)

  def start(self, from_user=False):
    if from_user or self.last_active:
      self.active = True
      self.thread = Thread(target=self.macro_loop, daemon=True)
      self.thread.start()

  def stop(self):
    self.active = False

  def macro_loop(self):
    while self.active:
      if self.game.world.player.is_in_delay():
        sleep(0.01)
        continue

      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F2, only_down=False)
      sleep(0.05)
      rand = (random.randint(-10, 10), random.randint(-10, 10))
      coords = tuple(map(sum,zip(self.game.world.player.screen_coordinates(), rand)))
      self.game.input.mouse.set_game_mouse_pos(coords + rand, game_coords=False)
      sleep(0.05)
      self.game.input.mouse.send_click()
      sleep(0.1)
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F1)
      sleep(0.05)

    self.thread = None
