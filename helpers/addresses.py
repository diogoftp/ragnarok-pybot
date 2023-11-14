# Base address where the game is loaded
GAME_BASE = 0x400000

# Static addresses offsets
MOUSE_POS_X_OFFSET = 0xB47F60
MOUSE_POS_Y_OFFSET = 0xB47F64

# From game base address
WORLD_BASE_INTERMED_OFFSET = 0xB3D1D4
PLAYER_NAME_OFFSET = 0xDD43E8
PLAYER_CURRENT_HP_OFFSET = 0xDD1A04
PLAYER_MAX_HP_OFFSET = 0xDD1A08
PLAYER_COORDINATE_X_OFFSET = 0xDBA5A0
PLAYER_COORDINATE_Y_OFFSET = 0xDBA5A4
MAP_NAME_OFFSET = 0xB3D1D8

# From world base intermed address
WORLD_BASE_OFFSET = 0xCC

# From world base address
# PLAYER_BASE = 0x2C
ENTITY_LIST_OFFSET = 0x10
VIEW_OFFSET = 0xD0

# From entity list address
ENTITY_OFFSET = 0x8

# From entity base address
ID_OFFSET = 0x10C
COORDINATE_X_OFFSET = 0x16C
COORDINATE_Y_OFFSET = 0x170

# From view address
CAMERA_ANGLE_HORIZONTAL = 0x48
CAMERA_ANGLE_VERTICAL = 0x44
CAMERA_ZOOM = 0x4C
