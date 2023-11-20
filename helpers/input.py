import win32api
import win32gui
import win32.lib.win32con as win32con
from time import sleep

from helpers.addresses import GAME_BASE, MOUSE_POS_X_OFFSET, MOUSE_POS_Y_OFFSET


class Input():
  def __init__(self, game):
    self.game = game
    self.keyboard = Keyboard(self.game)
    self.mouse = Mouse(self.game)


class Keyboard():
  class VKEYS():
    F1 = 0x70
    Z = 0x5A
    A = 0x41
    END = 0x23
    HOME = 0x24

  def __init__(self, game):
    self.game = game

  def listen_keys(self):
    if self.pressed(self.VKEYS.END):
      self.game.running = False
    if self.pressed(self.VKEYS.F1):
      self.game.macro.active = not self.game.macro.active
    if self.pressed(self.VKEYS.HOME):
      self.game.paused = not self.game.paused

  def pressed(self, key):
    return win32api.GetAsyncKeyState(key) != 0

  def send_key(self, key):
    win32api.PostMessage(self.game.window.handle, win32con.WM_KEYDOWN, key, 0)
    sleep(0.05)
    win32api.PostMessage(self.game.window.handle, win32con.WM_KEYUP, key, 0)


class Mouse():
  def __init__(self, game):
    self.game = game

  def get_current_mouse_pos(self):
    return win32gui.ScreenToClient(self.game.window.handle, win32api.GetCursorPos())

  def get_game_mouse_pos(self):
    x = self.game.window.view.process.memory.read_u_int(GAME_BASE + MOUSE_POS_X_OFFSET)
    y = self.game.window.view.process.memory.read_u_int(GAME_BASE + MOUSE_POS_Y_OFFSET)
    return (x, y)

  def set_game_mouse_pos(self, pos, game_coords=True):
    if game_coords:
      pos = self.game.window.translate_to_screen_coords(self.game.world.player.coordinates(), pos)

    self.game.process.memory.write_u_int(pos[0], GAME_BASE + MOUSE_POS_X_OFFSET)
    self.game.process.memory.write_u_int(pos[1], GAME_BASE + MOUSE_POS_Y_OFFSET)

  def send_click(self, destination=None):
    lParam = 0

    if destination != None:
      destination = self.game.window.translate_to_screen_coords(self.game.world.player.coordinates(), destination)
      screen_destination = win32gui.ClientToScreen(self.game.window.handle, destination)
      win32api.SetCursorPos(screen_destination)
      lParam = win32api.MAKELONG(screen_destination[0], screen_destination[1])

    win32gui.PostMessage(self.game.window.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.05)
    win32gui.PostMessage(self.game.window.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
