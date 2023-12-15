from time import sleep

from helpers.map import TARGET_MAP, TOWN

class RestockArrow():
  def __init__(self, game):
    self.game = game

  def should_restock(self):
    return self.game.inventory.item_quantity(1772) < 1000

  def restock(self):
    for _ in range(2):
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.F6)
      sleep(0.8)
