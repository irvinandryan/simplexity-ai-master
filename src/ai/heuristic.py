import random
from time import time

from src.constant import GameConstant, ShapeConstant, ColorConstant, Direction
from src.model import State, piece
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
    totalValue = shapeEvaluate(state, position, shape) + colorEvaluate(state, position, color)

    return totalValue

def shapeEvaluate(state: State, position: Tuple[int, int], shape: ShapeConstant) -> int:
    playing = whoseTurn(state)
    if playing == GameConstant.PLAYER1:
        enemy = GameConstant.PLAYER2
    else:
        enemy = GameConstant.PLAYER1

    #playing adalah pemain yang sedang turn-nya

    #mendata posisi mana saja yang bentuknya sama dengan playing
    nearbyPlayingShape = listNearbyShape(state, position, playing)
    #mendata posisi mana saja yang warnanya sama dengan musuh
    nearbyEnemyShape = listNearbyShape(state, position, enemy)

    playingShapeStreak = 0
    enemyShapeStreak = 0

    #cek streak untuk playing
    for playingCheck in nearbyPlayingShape:
        arah = direction(position, playingCheck)
        while(isPiecePlayingShape(state, playingCheck) and shape == state.board.__getitem__([playingCheck[0], playingCheck[1]]).shape):
            playingShapeStreak += 1
            playingCheck[0] += arah[0]
            playingCheck[1] += arah[1]

    #cek streak untuk enemy
    for enemyCheck in nearbyEnemyShape:
        arah = direction(position, enemyCheck)
        while(not(isPiecePlayingShape(state, enemyCheck) and shape == state.board.__getitem__([playingCheck[0], playingCheck[1]])).shape):
            enemyShapeStreak += 1
            enemyCheck[0] += arah[0]
            enemyCheck[1] += arah[1]
    
    if playingShapeStreak == 3:
        playingShapeStreak *= 200
    else:
        playingShapeStreak *= 20
    if enemyShapeStreak == 3:
        enemyShapeStreak *= 150
    else:
        enemyShapeStreak *= 20
    
    shapeStreak = playingShapeStreak + enemyShapeStreak
    return shapeStreak

def colorEvaluate(state: State, position: Tuple[int, int], color: ColorConstant) -> int:
    playing = whoseTurn(state)
    if playing == GameConstant.PLAYER1:
        enemy = GameConstant.PLAYER2
    else:
        enemy = GameConstant.PLAYER1

    #playing adalah pemain yang sedang turn-nya

    #mendata posisi mana saja yang warnanya sama dengan playing
    nearbyPlayingColor = listNearbyColor(state, position, playing)
    #mendata posisi mana saja yang warnanya sama dengan musuh
    nearbyEnemyColor = listNearbyColor(state, position, enemy)

    playingColorStreak = 0
    enemyColorStreak = 0

    #cek streak untuk playing jika dipilih position sebagai next step
    for playingCheck in nearbyPlayingColor:
        arah = direction(position, playingCheck)
        while(isPiecePlayingColor(state, playingCheck) and color == state.board.__getitem__([playingCheck[0], playingCheck[1]]).color):
            playingColorStreak += 1
            playingCheck[0] += arah[0]
            playingCheck[1] += arah[1]

    #cek streak untuk enemy jika enemy memilih position sebagai next step
    for enemyCheck in nearbyEnemyColor:
        arah = direction(position, enemyCheck)
        while(not(isPiecePlayingColor(state, enemyCheck)) and color == state.board.__getitem__([playingCheck[0], playingCheck[1]]).color):
            enemyColorStreak += 1
            enemyCheck[0] += arah[0]
            enemyCheck[1] += arah[1]

    if playingColorStreak == 3:
        playingColorStreak *= 100
    else:
        playingColorStreak *= 10
    if enemyColorStreak == 3:
        enemyColorStreak *= 50
    else:
        enemyColorStreak *= 10
    
    colorStreak = playingColorStreak + enemyColorStreak
    return colorStreak

def isPiecePlayingColor(state: State, position: Tuple[int, int]) -> bool:
    playing = whoseTurn(state)
    piece = state.board.__getitem__([position[0], position[1]])
    if playing == GameConstant.PLAYER1:
        if piece.color == GameConstant.PLAYER1_COLOR:
            return True
        else:
            return False
    else: #playing giliran player 2
        if piece.color == GameConstant.PLAYER2_COLOR:
            return True
        else:
            return False

def isPiecePlayingShape(state: State, position: Tuple[int, int]) -> bool:
    playing = whoseTurn(state)
    piece = state.board.__getitem__([position[0], position[1]])
    if playing == GameConstant.PLAYER1:
        if piece.shape == GameConstant.PLAYER1_SHAPE:
            return True
        else:
            return False
    else: #playing giliran player 2
        if piece.shape == GameConstant.PLAYER2_SHAPE:
            return True
        else:
            return False

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
    piece = state.board.__getitem__([position[0], position[1]])

    # true jika BLANK
    if piece.shape == ShapeConstant.BLANK:
        return True
    else:
        return False

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
        
def getPossibleMoves(state: State) -> list:
    # menentukan posisi-posisi yang bisa ditempati

    possibleMoves = []
    totalColumn = 7  
    totalRow = 6
    for x in range (totalColumn):
        for y in range (totalRow):
            piecePos = (x,y)
            if (isBlank(state, piece)):
                possibleMoves.append(piecePos)
                break
    return possibleMoves

