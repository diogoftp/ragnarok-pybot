import psutil
import struct
import win32api
import win32process
import win32
import ctypes
from ctypes import wintypes
from datetime import datetime

kernel32 = ctypes.windll.kernel32
CHAR_SIZE = 1
FLOAT_SIZE = 4
EXECUTABLE_NAME = "ragna4th.exe"


class Memory(object):
  def __init__(self, process):
    self.process = process

  def read(self, result, addr: int):
    kernel32.ReadProcessMemory(self.process, addr, ctypes.byref(result), ctypes.sizeof(result), 0)

    return result.value

  def write(self, c_type, value, addr: int):
    WriteProcessMemory = kernel32.WriteProcessMemory
    WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, c_type, ctypes.POINTER(c_type)]
    WriteProcessMemory.restypes = wintypes.BOOL

    # Arrays/buffers must be passed as ctypes, other values can be casted here
    if not isinstance(value, ctypes.Array):
      value = c_type(value)

    bytes_to_write = ctypes.sizeof(value)
    bytes_written = c_type(0)
    WriteProcessMemory(self.process, addr, ctypes.addressof(value), bytes_to_write, ctypes.byref(bytes_written))

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

  def write_u_int(self, value, addr: int):
    return self.write(ctypes.c_ulong, value, addr)

  # For some reason it doesn't work writing float to the game.
  # Probably because the game is 32-bit and I'm using a 64-bit Python interpreter.
  # So this function is a wrapper to the write_byte_array function.
  # Writing it at byte level works :D
  def write_float(self, value, addr: int):
    byte_array = struct.pack("f", value)
    buffer = ctypes.c_buffer(FLOAT_SIZE)
    buffer.value = byte_array

    return self.write_byte_array(buffer, addr)

  def write_byte_array(self, buffer, addr: int):
    return self.write(ctypes.c_byte, buffer, addr)


class Process(object):
  PROCESS_VM_READ = 0x0010
  PROCESS_VM_WRITE = 0x0020
  PROCESS_VM_OPERATION = 0x0008

  def __init__(self, open_privileges=None):
    self.name = EXECUTABLE_NAME
    self.handle = None
    self.memory = None
    self.pid = None
    self.base = None
    self.get_pid()
    self.open(self.PROCESS_VM_OPERATION | self.PROCESS_VM_READ | self.PROCESS_VM_WRITE)
    self.get_base_address()

  def __del__(self):
    if self.handle is not None:
      self.close()

  def exists(self):
    return self.get_pid() > 0

  def open(self, privileges):
    if self.pid == 0:
      raise RuntimeError("Process could not be opened")

    self.handle = kernel32.OpenProcess(privileges, 0, self.pid)
    self.memory = Memory(self.handle)

  def close(self):
    kernel32.CloseHandle(self.handle)
    self.handle = None

  def get_pid(self):
    processes_found = []

    for process in psutil.process_iter():
      if process.name() == self.name:
        processes_found.append(process)

    if len(processes_found) == 1:
      self.pid = processes_found[0].pid
      return
    elif len(processes_found) > 1:
      for index, process in enumerate(processes_found):
        print(f"[{index}] {process.name()} started {datetime.fromtimestamp(process._create_time)}")

      selected_index = input("Type the number of the process you would like to bot:")
      self.pid = processes_found[int(selected_index)].pid
      return

    raise RuntimeError("Failed to get process PID")

  def get_base_address(self):
    modules = win32process.EnumProcessModules(self.handle)

    for module in modules:
      module_name = str(win32process.GetModuleFileNameEx(self.handle, module))

      if module_name.split("\\")[-1] == EXECUTABLE_NAME:
        self.base = module
        return

    raise RuntimeError("Failed to get process base address")
