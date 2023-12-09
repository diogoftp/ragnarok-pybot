import win32con
import win32gui

from ctypes import WINFUNCTYPE, c_int, Structure, cast, POINTER, windll
from ctypes.wintypes import LPARAM, WPARAM, DWORD, PULONG, LONG
from helpers.window import WINDOW_NAME


def genStruct(name="Structure", **kwargs):
  return type(name, (Structure,), dict(
    _fields_=list(kwargs.items()),
    __str__=lambda self: "%s(%s)" % (name, ",".join("%s=%s" % (k, getattr(self, k)) for k in kwargs))
  ))

# Blocks mouse movent from being sent to the game window
class MouseBlocker():
  @WINFUNCTYPE(LPARAM, c_int, WPARAM, LPARAM)
  def hookProc(nCode, wParam, lParam):
    HookStruct = genStruct("Hook", pt=genStruct("Point", x=LONG, y=LONG), mouseData=DWORD, flags=DWORD, time=DWORD, dwExtraInfo=PULONG)
    msg = cast(lParam, POINTER(HookStruct))[0]
    # msgDict = {v: k for k, v in win32con.__dict__.items() if k.startswith("WM_")}
    # print(wParam, msgDict[wParam], msg)

    if nCode < 0:
      return windll.user32.CallNextHookEx(None, nCode, WPARAM(wParam), LPARAM(lParam))
    elif wParam == win32con.WM_MOUSEMOVE:
      handle = win32gui.WindowFromPoint((msg.pt.x, msg.pt.y))

      if win32gui.GetWindowText(handle) == WINDOW_NAME:
        return 1

    return windll.user32.CallNextHookEx(None, nCode, WPARAM(wParam), LPARAM(lParam))

  def __init__(self):
    self.hook = None
    self.start()

  def __del__(self):
    self.stop()
    self.hook = None

  def start(self):
    if self.hook is None:
      self.hook = windll.user32.SetWindowsHookExW(win32con.WH_MOUSE_LL, MouseBlocker.hookProc, None, 0)

    win32gui.PumpMessages()

  def stop(self):
    windll.user32.UnhookWindowsHookEx(self.hook)
    self.hook = None
