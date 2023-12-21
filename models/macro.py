from threading import Thread
from time import sleep
import random

from helpers.coordinate import Coordinate


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

      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F2)
      coords = self.game.world.player.screen_coordinates()
      coords.x += random.randint(-10, 10)
      coords.y += random.randint(-10, 10)
      self.game.input.mouse.set_game_mouse_pos(coords, game_coords=False)
      self.game.input.mouse.send_click()
      sleep(0.02)
      self.game.input.mouse.send_click()
      sleep(0.1)
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F1)
      sleep(0.05)

    self.thread = None
