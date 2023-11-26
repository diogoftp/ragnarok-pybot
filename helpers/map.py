import struct
import winsound

# For zoom = 400 and vertical angle = -50
CELL_PIXEL_SIZE = (31, 25)
ALLOWED_MAPS = ["moc_fild13", "abyss_04", "moscovia"]


class Map():
  def __init__(self, game):
    self.game = game
    self.current_map = None
    self.map = []
    self.width = None
    self.height = None
    self.last_map_unallowed = False
    self.last_bot_status = self.game.active
    self.last_macro_status = self.game.macro.active
    self.reload()

  def load_file(self):
    try:
      file_path = f"./maps/{self.current_map}.gat"
      return open(file_path, "rb")
    except FileNotFoundError:
      return None

  def reload(self):
    if self.current_map == self.game.world.player.map_name():
      return

    self.map = []

    self.current_map = self.game.world.player.map_name()
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

  def check_is_allowed_map(self):
    if (self.current_map not in ALLOWED_MAPS) and (not self.last_map_unallowed):
      winsound.PlaySound("unallowed_map.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
      self.last_bot_status = self.game.active
      self.last_macro_status = self.game.macro.active
      self.last_map_unallowed = True
      self.game.toggle_bot(active=False)
      self.game.macro.active = False
    elif (self.current_map in ALLOWED_MAPS) and (self.last_map_unallowed):
      self.last_map_unallowed = False
      self.game.toggle_bot(active=self.last_bot_status)
      self.game.macro.active = self.last_macro_status

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
