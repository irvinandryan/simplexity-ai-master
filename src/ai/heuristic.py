import random
from time import time

from src.constant import GameConstant, ShapeConstant, ColorConstant, Direction
from src.model import State
# import src.ai.objective

from typing import Tuple, List


# state, position, bentuk, warna
def heuristicValue(state: State, position: Tuple[int, int], shape: ShapeConstant, color: ColorConstant):
    # input : -> state    : state sekarang
    #         -> position : posisi yang mau dihitung nilai heuristic nya
    #         -> shape    : bentuk dari piece yang mau diletakkan
    #         -> color    : warna dari piece yang mau diletakkan  
    
    # total value
    totalValue = 0
    totalValueAdded = 0 # jika sampai 4 iterative berhenti

    # whose turn
    playing = whoseTurn(state)

    # list posisi yang dapat menguntungkan player
    nearbyGoodSpace = listNearbyGoodSpace(state, position, playing)
    
    # ALGORITMA
    # posisi sekarang
    xposition = position[0] 
    yposition = position[1]

    
    # posisi yang akan di cek
    xcheck = position[0]
    ycheck = position[1]

    # heuristicnya
    


    return totalValue

def shapeEvaluate(state: State, position: Tuple[int, int], shape: ShapeConstant) -> int:
    
    shapeValue = 0

    # whose turn
    playing = whoseTurn(state)

    # list posisi yang dapat menguntungkan player
    nearbyGoodSpace = listNearbyShape(state, position, playing)

    # posisi sekarang
    xposition = position[0] 
    yposition = position[1]
    
    # posisi yang akan di cek
    xcheck = position[0]
    ycheck = position[1]

    
    


    return shapeValue

def colorEvaluate(state: State, position: Tuple[int, int], color: ColorConstant) -> int:
    
    colorValue = 0

    playing = whoseTurn(state)

    nearbySameColor = listNearbyColor(state, position, playing)

    #for pos in nearbySameColor:


    xposition = position[0]
    yposition = position[1]

    xcheck = position[0]
    ycheck = position[1]

    
    

    return colorValue

def isPieceP1Shape(state: State, position: Tuple[int, int]) -> bool:
    # Cek apakah shape milik player 1

    piece = state.board.__getitem__([position[0], position[1]])
    if piece.shape == GameConstant.PLAYER1_SHAPE:
        return True
    else:
        return False

def isPieceP1Color(state: State, position: Tuple[int, int]) -> bool:
    # Cek apakah color milik player 1

    piece = state.board.__getitem__([position[0], position[1]])
    if piece.color == GameConstant.PLAYER1_COLOR:
        return True
    else:
        return False

def isBlank(state: State, position: Tuple[int, int]) -> bool:
    # cek apakah cell kosong
    piece = state.board[position[0], position[1]]

    # true jika SELAIN ada isinya. Selain BLANK juga true
    if piece.shape == ShapeConstant.CIRCLE or piece.shape == ShapeConstant.CROSS:
        return False
    else:
        return True

def whoseTurn(state: State) -> GameConstant:
    # round genap -> P1
    # round ganjil -> P2
    if (state.round % 2 == 0):
        return GameConstant.PLAYER1
    else:
        return GameConstant.PLAYER2

def listNearbyFilledSpace(state: State, position: Tuple[int, int]) -> list:
    # Mencari posisi-posisi berdekatan yang tidak kosong
    
    # array of position
    nearbyFilledSpace = []
    
    # array of x
    posX = [-1, 0, 1]
    
    # array of y
    posY = [-1, 0, 1]

    for x in posX:
        for y in posY:
            newPosition = (position[0]+x, position[1]+y)
            if (not isBlank(state, newPosition) and newPosition != position):
                nearbyFilledSpace.append(newPosition)
    
    return nearbyFilledSpace

def listNearbyShape(state: State, position: Tuple[int, int], playing: GameConstant) -> list:
    # Mencari posisi" yang shape nya sama

    # selected position nearby same shape
    nearbySameShape = []
    # selected position nearby filled space 
    nearbyFilledSpace = listNearbyFilledSpace(state, position)

    for space in nearbyFilledSpace:

        piece = state.board.__getitem__([space[0], space[1]])
        nearbyShapePos = (space[0], space[1])

        if (playing == GameConstant.PLAYER1):
            if (piece.shape == GameConstant.PLAYER1_SHAPE):
                nearbySameShape.append(nearbyShapePos)
        else:
            if (piece.shape == GameConstant.PLAYER2_SHAPE):
                nearbySameShape.append(nearbyShapePos)

    return nearbySameShape

def listNearbyColor(state: State, position: Tuple[int, int], playing: GameConstant) -> list:
    # Mencari posisi" yang color nya sama

    # selected position nearby same shape
    nearbySameColor = []
    # selected position nearby filled space 
    nearbyFilledSpace = listNearbyFilledSpace(state, position)

    for space in nearbyFilledSpace:

        piece = state.board.__getitem__([space[0], space[1]])
        nearbyColorPos = (space[0], space[1])

        if (playing == GameConstant.PLAYER1):
            if (piece.color == GameConstant.PLAYER1_COLOR):
                nearbySameColor.append(nearbyColorPos)
        else:
            if (piece.color == GameConstant.PLAYER2_COLOR):
                nearbySameColor.append(nearbyColorPos)

    return nearbySameColor

def listNearbyGoodSpace(state: State, position: Tuple[int, int], playing: GameConstant) -> list:
    # Mencari posisi" yang dapat menambah poin
    # P1 berarti mencari RED atau CIRCLE
    # P2 berarti mencari BLUE atau CROSS

    # selected position nearby same shape
    nearbyGoodSpace = []
    
    # selected position nearby filled space 
    nearbyFilledSpace = listNearbyFilledSpace(state, position)

    for space in nearbyFilledSpace:

        piece = state.board.__getitem__([space[0], space[1]])
        nearbyGoodPos = (space[0], space[1])

        if (playing == GameConstant.PLAYER1):
            # player 1 turn
            if (piece.shape == GameConstant.PLAYER1_SHAPE or piece.color == GameConstant.PLAYER1_COLOR):
                nearbyGoodSpace.append(nearbyGoodPos)
        else:       
            # player 2 turn
            if (piece.shape == GameConstant.PLAYER2_SHAPE or piece.color == GameConstant.PLAYER2_COLOR):
                nearbyGoodSpace.append(nearbyGoodPos)

    return nearbyGoodSpace

def direction(position1: Tuple[int,int], position2: Tuple[int,int]) -> Direction:
    # posisi 2 sebelah kanan
    if position2[0] - position1[0] == 1:
        # atas
        if position2[1] - position1[1] == 1:
            return Direction.NE
        # tengah
        elif position2[1] - position1[1] == 0:
            return Direction.E
        # bawah
        elif position2[1] - position1[1] == -1:
            return Direction.SE

    # posisi 2 sebelah kiri
    elif position2[0] - position1[0] == -1:
        # atas
        if position2[1] - position1[1] == 1:
            return Direction.NW
        # tengah
        elif position2[1] - position1[1] == 0:
            return Direction.W
        # bawah
        elif position2[1] - position1[1] == -1:
            return Direction.SW

    # posisi 2 ditengah (selisih koor X = 0)
    elif position2[0] - position1[0] == 0:
        if position2[1] - position1[1] == 1:
            return Direction.N
        elif position2[1] - position1[1] == 0:
            return Direction.O
        elif position2[1] - position1[1] == -1:
            return Direction.S
        


