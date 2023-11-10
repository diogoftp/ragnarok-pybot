from helpers.addresses import (
  ENTITY_LIST_OFFSET,
  ENTITY_OFFSET,
  ID_OFFSET,
  COORDINATE_X_OFFSET,
  COORDINATE_Y_OFFSET
)


class EntityList():
  def __init__(self, process, world_base):
    self.process = process
    self.base = self.process.memory.read_ptr(world_base, ENTITY_LIST_OFFSET)
    self.current = self.first()
    self.first_address = self.current
    self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))

  def first(self):
    return self.process.memory.read_ptr(self.base, 0x0)

  def reset(self):
    self.current = self.first()
    self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))

  def find_next(self):
    next_entity = self.process.memory.read_ptr(self.current, 0x0)

    if next_entity != self.first():
      self.current = next_entity
      self.current_entity_instance = Entity(self.process, self.process.memory.read_ptr(self.current, ENTITY_OFFSET))
    else:
      self.current = None
      self.current_entity_instance = None

  def __str__(self):
    print("Entity list:")

    while self.current:
      # Stop if first address changed, avoiding infinite loop while teleporting in the game
      if self.first_address != self.first():
        self.first_address = self.first()
        break

      print(f"\t{hex(self.current)}, {self.current_entity_instance.id()}, {self.current_entity_instance.coords()}")
      self.find_next()

    self.reset()
    return ""


# id 0 = player
# id <= 1000 npc / portal
# id > 1000 monster / pet
# TODO: try to find a better way to distinguish them
class Entity():
  def __init__(self, process, base):
    self.process = process
    self.base = base

  def id(self):
    return self.process.memory.read_u_int(self.base + ID_OFFSET)

  def coords(self):
    return (self.process.memory.read_u_int(self.base + COORDINATE_X_OFFSET), self.process.memory.read_u_int(self.base + COORDINATE_Y_OFFSET))