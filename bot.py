from models.game import Game
from time import sleep
import os


class Bot():
  def __init__(self):
    self.game = Game()
    self.start_game_loop()

  def start_game_loop(self):
    while(True):
      if self.game.input.keyboard.pressed(self.game.input.keyboard.KILL_SWITCH_KEY):
        break

      os.system("cls")
      print(self.game)
      self.game.map.reload()
      self.game.macro.loop()

      if self.game.world.player.current_action == "idle":
        self.game.action.find_target()
      elif self.game.world.player.current_action == "fighting":
        self.game.action.fight()
      elif self.game.world.player.current_action == "finding_target":
        pass

      sleep(0.1)

    self.game.macro.stop()
