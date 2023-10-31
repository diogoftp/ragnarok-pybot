import ctypes
import psutil

kernel32 = ctypes.windll.kernel32
CHAR_SIZE = 1


class Memory(object):
  def __init__(self, process):
    self.process = process

  def read(self, result, addr: int):
    kernel32.ReadProcessMemory(self.process, addr, ctypes.byref(result), ctypes.sizeof(result), 0)

    return result.value

  def read_u_short_int(self, addr: int):
    return self.read(ctypes.c_ushort(), addr)

  def read_u_int(self, addr: int):
    return self.read(ctypes.c_ulong(), addr)

  def read_float(self, addr: int):
    return self.read(ctypes.c_float(), addr)

  def read_byte(self, addr: int):
    return self.read(ctypes.c_byte(), addr)

  def read_str(self, addr: int):
    buffer = ""
    read_bytes = self.read(ctypes.c_byte(), addr)
    buffer += chr(read_bytes)
    addr += CHAR_SIZE

    while read_bytes != 0:
      read_bytes = self.read(ctypes.c_byte(), addr)
      buffer += chr(read_bytes)
      addr += CHAR_SIZE

    return buffer

  def read_ptr(self, addr: int, offset=0x0):
    return self.read(ctypes.c_ulong(), addr + offset)


class Process(object):
  PROCESS_VM_READ = 0x0010
  PROCESS_VM_WRITE = 0x0020

  def __init__(self, name, open_privileges=None):
    self.name = name
    self.pid = self.get_pid()
    self.handle = None
    self.memory = None
    self.base = None

    if open_privileges is not None:
      self.open(open_privileges)

  def __del__(self):
    if self.handle is not None:
      self.close()

  def exists(self):
    return self.get_pid() > 0

  def open(self, privileges):
    if self.pid == 0:
      raise RuntimeError("Process could not be opened")

    self.handle = kernel32.OpenProcess(privileges, 0, self.pid)
    # self.base = win32process.EnumProcessModules(self.handle)[0]
    self.memory = Memory(self.handle)

  def close(self):
    kernel32.CloseHandle(self.handle)
    self.handle = None

  def get_pid(self):
    for process in psutil.process_iter():
      if process.name() == self.name:
        return process.pid
    else:
      return 0
