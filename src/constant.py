import os


class ColorConstant:
    RED = "RED"
    BLUE = "BLUE"
    BLACK = "BLACK"


class ShapeConstant:
    CROSS = "X"
    CIRCLE = "O"
    BLANK = "-"


class GameConstant:
    SHAPE = "SHAPE"
    COLOR = "COLOR"
    WIN_PRIOR = [SHAPE, COLOR]
    PLAYER_COLOR = [ColorConstant.RED, ColorConstant.BLUE]
    N_COMPONENT_STREAK = 4

    PLAYER1 = "P1"
    PLAYER2 = "P2"
    PLAYER1_COLOR = ColorConstant.RED
    PLAYER1_SHAPE = ShapeConstant.CIRCLE
    PLAYER2_COLOR = ColorConstant.BLUE
    PLAYER2_SHAPE = ShapeConstant.CROSS

    BVB = 0  # Bot vs Bot
    PVB = 1  # Player vs Bot
    PVP = 2  # Player vs 
    

class Direction:
    N = (0,1)
    S = (0,-1)
    E = (1,0)
    W = (-1,0)

    NE = (1,1)
    NW = (-1,1)
    SE = (1,-1)
    SW = (-1,-1)

    O = (0,0)


class Path:
    PLAYER1 = 0
    PLAYER2 = 1
    FOLDER = "bin"
    BVB_FOLDER = "bvb"
    PVB_FOLDER = "pvb"
    BVB_P1 = os.path.join(FOLDER, BVB_FOLDER, "{}")
    BVB_P2 = os.path.join(FOLDER, BVB_FOLDER, "{}")
    PVB = os.path.join(FOLDER, PVB_FOLDER, "{}")