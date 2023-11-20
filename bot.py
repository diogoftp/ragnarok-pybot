from models.game import Game


class Bot():
  def __init__(self):
    self.game = Game()
    self.game.loop()
