from time import sleep

from helpers.addresses import (
  WORLD_BASE_INTERMED_OFFSET,
  WORLD_BASE_OFFSET,
  VIEW_OFFSET,
  CHAT_BAR_ENABLED_OFFSET
)
from models.player import Player
from models.entity import EntityList
from models.view import View


class World():
  def __init__(self, game):
    self.game = game
    self.player = Player(self.game, self.base())
    self.entity_list = EntityList(self.game.process, self.game)
    self.view = View(self.game)

  def intermed_base(self):
    return self.game.process.memory.read_ptr(self.game.base + WORLD_BASE_INTERMED_OFFSET)

  def base(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + WORLD_BASE_INTERMED_OFFSET, [WORLD_BASE_OFFSET])

  def enable_chat_bar(self):
    if not self.is_chat_bar_enbaled():
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.ENTER)

  def disable_chat_bar(self):
    if self.is_chat_bar_enbaled():
      self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.ENTER)

  def is_chat_bar_enbaled(self):
    return self.game.process.memory.read_byte(self.game.base + CHAT_BAR_ENABLED_OFFSET) == 1

  def write_to_chat_bar(self, string):
    self.game.input.keyboard.send_string(string)
    sleep(0.1)
    self.game.input.keyboard.send_key(self.game.input.keyboard.VKEYS.ENTER)
