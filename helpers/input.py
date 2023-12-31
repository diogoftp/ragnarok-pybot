import win32api
import win32gui
import win32.lib.win32con as win32con
import random
from time import sleep
from ctypes import windll

from helpers.addresses import MOUSE_POS_X_OFFSET, MOUSE_POS_Y_OFFSET
from helpers.mouse_blocker import MouseBlocker
from helpers.coordinate import Coordinate


class Input():
  def __init__(self, game):
    self.game = game
    self.keyboard = Keyboard(self.game)
    self.mouse = Mouse(self.game)


class Keyboard():
  class VKEYS():
    F1 = 0x70
    F2 = 0x71
    F6 = 0x75
    Z = 0x5A
    A = 0x41
    END = 0x23
    HOME = 0x24
    ENTER = 0x0D
    LSHIFT = 0xA0
    PGUP = 0x21
    PGDOWN = 0x22

  def __init__(self, game):
    self.game = game
    self.last_key_states = {}

  def listen_keys(self):
    if self.pressed(self.VKEYS.END):
      self.game.running = False
    if self.pressed(self.VKEYS.F1):
      self.game.macro.toggle()
    if self.pressed(self.VKEYS.HOME):
      self.game.toggle_bot()
    if self.pressed(self.VKEYS.PGUP):
      self.game.input.mouse.mouse_blocker.toggle()

  def pressed(self, key):
    key_state = win32api.GetKeyState(key)

    if key_state == 0 or key_state == 1:
      if key not in self.last_key_states:
        self.last_key_states[key] = key_state
        return False
      elif self.last_key_states[key] != key_state:
        self.last_key_states[key] = key_state
        return True

    return False

  def send_key(self, key):
    win32api.PostMessage(self.game.window.handle, win32con.WM_KEYDOWN, key, 0x00000001)
    # Sleep randomly between 0.15 and 0.2 seconds
    rand = round(random.uniform(0.15, 0.2), 10)
    sleep(rand)
    win32api.PostMessage(self.game.window.handle, win32con.WM_KEYUP, key, 0xC0000001)

  def send_string(self, string):
    for key in string:
      if key == "@":
        win32api.PostMessage(self.game.window.handle, win32con.WM_CHAR, 0x40, 30001) # Reproduce message captured using Spy++
      else:
        self.send_key(self.char_to_vkey(key))

  def char_to_vkey(self, char):
    result = windll.User32.VkKeyScanW(ord(char))
    shift_state = (result & 0xFF00) >> 8
    return result & 0xFF

class Mouse():
  def __init__(self, game):
    self.game = game
    self.mouse_blocker = MouseBlocker()

  def get_current_mouse_pos(self):
    return win32gui.ScreenToClient(self.game.window.handle, win32api.GetCursorPos())

  def get_game_mouse_pos(self):
    x = self.game.window.view.process.memory.read_u_int(self.game.base + MOUSE_POS_X_OFFSET)
    y = self.game.window.view.process.memory.read_u_int(self.game.base + MOUSE_POS_Y_OFFSET)
    return (x, y)

  def set_game_mouse_pos(self, pos, game_coords=True):
    if game_coords:
      pos = self.game.window.translate_to_screen_coords(self.game.world.player.coordinates(), pos)

    self.game.process.memory.write_u_int(pos.x, self.game.base + MOUSE_POS_X_OFFSET)
    self.game.process.memory.write_u_int(pos.y, self.game.base + MOUSE_POS_Y_OFFSET)

  def send_click(self, destination:Coordinate=None):
    lParam = 0

    if destination != None:
      if destination.type == "game":
        destination.to_screen(self.game)

      lParam = win32api.MAKELONG(destination.x, destination.y)

    win32gui.PostMessage(self.game.window.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.05)
    win32gui.PostMessage(self.game.window.handle, win32con.WM_LBUTTONUP, 0, lParam)
