from threading import Thread
from time import sleep


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

  def loop(self):
    print(self.active)
    if self.game.input.keyboard.pressed(self.game.input.keyboard.VKEYS.F1):
      self.active = not self.active

  def macro_loop(self):
    while self.thread_running:
      print("Macro thread running")
      if self.active:
        self.game.input.keyboard.send_key(self.input.keyboard.VKEYS.Z)
        sleep(0.1)
        self.game.input.mouse.send_click(None)
        sleep(0.1)
        self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.A)
        sleep(0.1)
      sleep(0.1)
