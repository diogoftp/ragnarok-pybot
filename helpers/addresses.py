# Static addresses offsets
MOUSE_POS_X_OFFSET = 0xB47F60
MOUSE_POS_Y_OFFSET = 0xB47F64
CHAT_BAR_ENABLED_OFFSET = 0xB81390
INVENTORY_BASE_OFFSET = 0xDCDEE0
INVENTORY_QUANTITY_OFFSET = 0xDCDEE4
IS_IN_DELAY_OFFSET = 0xDD1850

# From game base address
WORLD_BASE_INTERMED_OFFSET = 0xB3D1D4
PLAYER_NAME_OFFSET = 0xDD43E8
PLAYER_CURRENT_HP_OFFSET = 0xDD1A04
PLAYER_MAX_HP_OFFSET = 0xDD1A08
PLAYER_CURRENT_SP_OFFSET = 0xDD1A0C
PLAYER_MAX_SP_OFFSET = 0xDD1A10
PLAYER_COORDINATE_X_OFFSET = 0xDBA5A0
PLAYER_COORDINATE_Y_OFFSET = 0xDBA5A4
MAP_NAME_OFFSET = 0xB3D1D8

# From world base intermed address
WORLD_BASE_OFFSET = 0xCC
IS_TALKING_TO_NPC_OFFSET = 0x258

# From world base address
PLAYER_BASE = 0x2C
ENTITY_LIST_OFFSET = 0x10
ENTITY_LIST_SIZE_OFFSET = 0x14
VIEW_OFFSET = 0xD0

# From player base address
STATE_OFFSET = 0x70
PLAYER_SCREEN_COORD_X_OFFSET = 0xAC
PLAYER_SCREEN_COORD_Y_OFFSET = 0xB0

# From entity list address
ENTITY_OFFSET = 0x8

# From entity base address
ID_OFFSET = 0x10C
COORDINATE_X_OFFSET = 0x16C
COORDINATE_Y_OFFSET = 0x170
SCREEN_COORDINATE_X_OFFSET = 0xAC
SCREEN_COORDINATE_Y_OFFSET = 0xB0
C_SPR_RES_OFFSET = 0x104

# From CSprRes address
SPRITE_NAME_OFFSET = 0x21

# From view address
CAMERA_ANGLE_HORIZONTAL = 0x48
CAMERA_ANGLE_VERTICAL = 0x44
CAMERA_ZOOM = 0x4C

# From inventory address
FIRST_ITEM_INVENTORY_OFFSET = 0x0
LAST_ITEM_INVENTORY_OFFSET = 0x04

# From item address
ITEM_NEXT_OFFSET = 0x0
ITEM_PREV_OFFSET = 0x4
# UNKNOWN_OFFSET = 0x8 # Probably related to position in inventory
# UNKNOWN_OFFSET = 0xC # Probably related to position in inventory
ITEM_QUANTITY_OFFSET = 0x18
ITEM_ID_OFFSET = 0x34
