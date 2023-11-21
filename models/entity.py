from helpers.addresses import (
  ENTITY_LIST_OFFSET,
  ENTITY_OFFSET,
  ID_OFFSET,
  COORDINATE_X_OFFSET,
  COORDINATE_Y_OFFSET,
  SCREEN_COORDINATE_X_OFFSET,
  SCREEN_COORDINATE_Y_OFFSET,
  C_SPR_RES_OFFSET,
  SPRITE_NAME_OFFSET
)


class EntityList():
  def __init__(self, process, world_base):
    self.process = process
    self.base = self.process.memory.read_ptr(world_base, ENTITY_LIST_OFFSET)
    self.current = self.first()
    self.first_address = self.current
    self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))
    self.entity_array = []

  def __iter__(self):
    return self

  def __next__(self):
    # Check if list is empty, otherwise it is going to return memory garbage
    # Stop if first address changed, avoiding infinite loop while teleporting in the game
    if (self.first() == self.base or self.first_address != self.first()):
      self.first_address = self.first()
      self.reset()
      raise StopIteration

    if self.current is not None:
      current_instance = self.current_entity_instance
      self.find_next()
      return current_instance

    self.reset()
    raise StopIteration

  def update_array(self):
    self.entity_array = []

    for entity in self:
      self.entity_array.append(entity)

  def first(self):
    return self.process.memory.read_ptr(self.base, 0x0)

  def last(self):
    return self.process.memory.read_ptr(self.base, 0x4)

  def reset(self):
    self.current = self.first()
    self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))

  def find_next(self):
    if self.current == self.last():
      self.current = None
      self.current_entity_instance = None
    else:
      self.current = self.process.memory.read_ptr(self.current, 0x0)
      self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))

  def __str__(self):
    entity_list_string = "Entity list:\n"

    for entity in self:
      entity_list_string += f"{entity}\n"

    return entity_list_string

# id 0 = player
# id <= 1000 npc / portal
# id > 1000 monster / pet
# TODO: try to find a better way to distinguish them
class Entity():
  def __init__(self, process, base):
    self.process = process
    self.base = base

  def __str__(self):
    return f"{self.id()} | {self.name()} | {self.coords()} | {self.screen_coords()}"

  def id(self):
    return self.process.memory.read_u_int(self.base + ID_OFFSET)

  def coords(self):
    return (self.process.memory.read_u_int(self.base + COORDINATE_X_OFFSET), self.process.memory.read_u_int(self.base + COORDINATE_Y_OFFSET))

  def screen_coords(self):
    return (self.process.memory.read_u_int(self.base + SCREEN_COORDINATE_X_OFFSET), self.process.memory.read_u_int(self.base + SCREEN_COORDINATE_Y_OFFSET))

  def name(self):
    cspr_res_address = self.process.memory.read_ptr(self.base + C_SPR_RES_OFFSET)
    return self.process.memory.read_str(cspr_res_address + SPRITE_NAME_OFFSET).strip("\\").split(".spr")[0]
