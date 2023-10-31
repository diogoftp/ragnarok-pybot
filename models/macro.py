from threading import Thread
from time import sleep


class Macro():
  def __init__(self, window, _input):
    self.thread_running = True
    self.active = False
    self.window = window
    self.input = _input

    self.thread = Thread(target=self.macro_loop)
    self.thread.start()

  def stop(self):
    self.active = False
    self.thread_running = False

  def loop(self):
    print(self.active)
    if self.input.keyboard.pressed(self.input.keyboard.VKEYS.F1):
      self.active = not self.active

  def macro_loop(self):
    while self.thread_running:
      print("Macro thread running")
      if self.active:
        self.input.keyboard.send_key(self.input.keyboard.VKEYS.Z)
        sleep(0.1)
        self.input.mouse.send_click(None)
        sleep(0.1)
        self.input.keyboard.send_key(self.input.keyboard.VKEYS.A)
        sleep(0.1)
      sleep(0.1)
