import win32api
import win32gui
import win32.lib.win32con as win32con
from time import sleep


class Input():
  def __init__(self, window):
    self.window = window
    self.keyboard = Keyboard(self.window)
    self.mouse = Mouse(self.window)


class Keyboard():
  class VKEYS():
    F1 = 0x70
    Z = 0x5A
    A = 0x41
    END = 0x23

  def __init__(self, window):
    self.window = window
    self.handle = self.window.handle
    self.KILL_SWITCH_KEY = self.VKEYS.END

  def pressed(self, key):
    return win32api.GetAsyncKeyState(key) != 0

  def send_key(self, key):
    win32api.PostMessage(self.handle, win32con.WM_KEYDOWN, key, 0)
    sleep(0.05)
    win32api.PostMessage(self.handle, win32con.WM_KEYUP, key, 0)


class Mouse():
  def __init__(self, window):
    self.window = window
    self.handle = self.window.handle

  def get_current_mouse_pos(self):
    return win32gui.ScreenToClient(self.handle, win32api.GetCursorPos())

  def send_click(self, destination=None):
    lParam = 0

    if destination != None:
      destination = self.window.translate_to_screen_coords(destination)
      screen_destination = win32gui.ClientToScreen(self.handle, destination)
      win32api.SetCursorPos(screen_destination)
      lParam = win32api.MAKELONG(screen_destination[0], screen_destination[1])

    win32gui.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.05)
    win32gui.PostMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
