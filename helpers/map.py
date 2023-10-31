import struct

CELL_PIXEL_SIZE = (24, 18)


class Map():
  def __init__(self, player):
    self.player = player
    self.current_map = None
    self.map = []
    self.width = None
    self.height = None
    self.reload()

  def load_file(self):
    try:
      file_path = f"./maps/{self.current_map}.gat"
      print(file_path)
      return open(file_path, "rb")
    except FileNotFoundError:
      return None

  def reload(self):
    if self.current_map == self.player.map_name():
      return

    self.map = []

    self.current_map = self.player.map_name()
    file = self.load_file()

    if file is None:
      return

    header = file.read(6)
    self.width, self.height = struct.unpack("II", file.read(8))

    tiles_read = 1
    block = file.read(20)
    tile_type = struct.unpack("ffffBBBB", block)[4]
    self.map.append(tile_type)

    while tiles_read < self.width * self.height:
      tiles_read += 1
      block = file.read(20)
      tile_type = struct.unpack("ffffBBBB", block)[4]
      self.map.append(tile_type)

    file.close()

  def read_coords(self, coords):
    if len(self.map) == 0:
      return None

    return self.map[coords[1] * self.width + coords[0]]

  def walkable(self, coords):
    if len(self.map) == 0:
      return None

    tile_type = self.read_coords(coords)

    return tile_type == 0 or tile_type == 3

  def route_to(self, destination):
    pass

  def walk_to(self, destination):
    pass
