from helpers.addresses import (
  INVENTORY_BASE_OFFSET,
  INVENTORY_QUANTITY_OFFSET,
  FIRST_ITEM_INVENTORY_OFFSET,
  LAST_ITEM_INVENTORY_OFFSET,
  ITEM_NEXT_OFFSET,
  ITEM_PREV_OFFSET,
  ITEM_QUANTITY_OFFSET,
  ITEM_ID_OFFSET
)


class Inventory():
  def __init__(self, game, process):
    self.process = process
    self.game = game
    self.current = None

  def quantity(self):
    return self.process.memory.read_u_int(self.game.base + INVENTORY_QUANTITY_OFFSET)

  def __iter__(self):
    self.current = self.first()
    return self

  def __next__(self):
    if (self.current == self.last()):
      self.reset()
      raise StopIteration

    self.current = self.process.memory.read_ptr(self.current)

    return Item(self.process, self.current)

  def first(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + INVENTORY_BASE_OFFSET, [FIRST_ITEM_INVENTORY_OFFSET])

  def last(self):
    return self.game.process.memory.read_ptr_chain(self.game.base + INVENTORY_BASE_OFFSET, [LAST_ITEM_INVENTORY_OFFSET])

  def reset(self):
    self.current = self.first()

  def __str__(self):
    inventory_string = f"Inventory ({self.quantity()}):\n"

    for item in self:
      inventory_string += f"{item}\n"

    return inventory_string

  def item_quantity(self, item_id):
    for item in self:
      if item.id() == item_id:
        return item.quantity()

    return 0


class Item():
  def __init__(self, process, base):
    self.process = process
    self.base = base

  def __str__(self):
    return f"{self.id()} ({self.quantity()})"

  def id(self):
    # Must remove '\0' from the end of string to cast to int
    try:
      return int(self.process.memory.read_str(self.base + ITEM_ID_OFFSET)[:-1])
    except ValueError:
      return -1

  def quantity(self):
    return self.process.memory.read_u_int(self.base + ITEM_QUANTITY_OFFSET)
