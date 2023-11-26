from threading import Thread
from time import sleep
import random


class Macro():
  def __init__(self, game):
    self.thread_running = True
    self.active = False
    self.game = game

    self.thread = Thread(target=self.macro_loop)
    self.thread.start()

  def stop(self):
    self.active = False
    self.thread_running = False

  def macro_loop(self):
    while self.thread_running:
      print("Macro thread running")
      if self.active:
        self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F2)
        sleep(0.1)
        rand = (random.randint(-10, 10), random.randint(-10, 10))
        coords = tuple(map(sum,zip(self.game.world.player.screen_coordinates(), rand)))
        self.game.input.mouse.set_game_mouse_pos(coords + rand, game_coords=False)
        sleep(0.1)
        self.game.input.mouse.send_click()
        self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F1)
        sleep(0.1)
      sleep(0.1)
