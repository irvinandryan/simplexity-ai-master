import random
from time import time
from src.model import board
from src.model.piece import Piece
from src.utility import *

from src.constant import GameConstant, ShapeConstant, ColorConstant, Direction
from src.model import State

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        playing = self.whoseTurn(state)

        #minimax algorithm
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        
        # best_movement = self.minimax(state, 3, playing)

        return best_movement

    def minimax(self, state: State, depth: int, playing: GameConstant) -> Tuple[str,str]:
        # Minimax Alpha Beta Pruning

        if (playing == GameConstant.PLAYER1):
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        possibleMoves = self.getPossibleMoves(state)
        bestMove = possibleMoves[0]
        bestScore = -9999

        # 9999 untuk menggantikan infinity
        alpha = -9999
        beta = 9999

        for move in possibleMoves:
            tempState = self.tempMove(state, move, playing)
            boardScore = self.minimize(tempState, move, depth - 1, alpha, beta, enemy)

            if boardScore > bestScore:
                bestScore = boardScore
                bestMove = move

        theBestMove = (bestMove[1], random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        return theBestMove

    def minimize(self, state: State, position: Tuple[int,int], depth, a, b, playing: GameConstant) -> int:
        possibleMoves = self.getPossibleMoves(state)

        if (playing == GameConstant.PLAYER1):
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        # basis
        if (depth == 0 or len(possibleMoves) == 0):
            if (playing == GameConstant.PLAYER1):
                shape = GameConstant.PLAYER1_SHAPE
                color = GameConstant.PLAYER1_COLOR
            else :
                shape = GameConstant.PLAYER1_SHAPE
                color = GameConstant.PLAYER1_COLOR
            return self.heuristicValue(state, position, shape, color)

        # rekursif
        # Player 2 (BLUE, CROSS)
        beta = b
        for move in possibleMoves:
            posScore = 9999
            if (a < beta):
                tempState = self.tempMove(state, move, playing)
                # create tempState
                posScore = self.maximaze(tempState, move, depth - 1, a, b, enemy)

            if (posScore < beta):
                beta = posScore
        return beta

    def maximaze(self, state: State, position: Tuple[int,int], depth, a, b, playing: GameConstant) -> int:
        possibleMoves = self.getPossibleMoves(state)

        if (playing == GameConstant.PLAYER1):
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        # basis
        if (depth == 0 or len(possibleMoves) == 0):
            if (playing == GameConstant.PLAYER1):
                shape = GameConstant.PLAYER1_SHAPE
                color = GameConstant.PLAYER1_COLOR
            else :
                shape = GameConstant.PLAYER1_SHAPE
                color = GameConstant.PLAYER1_COLOR
            return self.heuristicValue(state, position, shape, color)

        # rekursif
        # Player 1 (RED, CIRCLE)
        alpha = a
        for move in possibleMoves:
            posScore = -9999
            if (alpha < b):
                tempState = self.tempMove(state, move, playing)
                posScore = self.minimize(tempState, move, depth - 1, a, b, enemy)

            if (posScore > a):
                a = posScore
        return a

    def tempMove(self, state: State, position: Tuple[int,int], playing: GameConstant) -> State:
        if (playing == GameConstant.PLAYER1):
            tempPiece = Piece(GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)
        else:
            tempPiece = Piece(GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)
        tempState = state
        tempState.round += 1
        tempState.board.set_piece(position[1], position[0], tempPiece)
        return tempState
        
    # state, position, bentuk, warna
    def heuristicValue(self, state: State, position: Tuple[int, int], shape: ShapeConstant, color: ColorConstant):
        # input : -> state    : state sekarang
        #         -> position : posisi yang mau dihitung nilai heuristic nya
        #         -> shape    : bentuk dari piece yang mau diletakkan
        #         -> color    : warna dari piece yang mau diletakkan  
        
        # total value
        totalValue = 0
        totalValue = self.shapeEvaluate(state, position, shape) + self.colorEvaluate(state, position, color)

        return totalValue

    def shapeEvaluate(self, state: State, position: Tuple[int, int], shape: ShapeConstant) -> int:
        playing = self.whoseTurn(state)
        if playing == GameConstant.PLAYER1:
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        #playing adalah pemain yang sedang turn-nya

        #mendata posisi mana saja yang bentuknya sama dengan playing
        nearbyPlayingShape = self.listNearbyShape(state, position, playing)
        #mendata posisi mana saja yang warnanya sama dengan musuh
        nearbyEnemyShape = self.listNearbyShape(state, position, enemy)

        playingShapeStreak = 0
        enemyShapeStreak = 0

        #cek streak untuk playing
        for playingCheck in nearbyPlayingShape:
            arah = self.direction(position, playingCheck)
            playingCheckPos = list(playingCheck)
            piece = state.board.__getitem__([playingCheck[0], playingCheck[1]])
            while(self.isPiecePlayingShape(state, playingCheckPos) and shape == piece.shape):
                playingShapeStreak += 1
                if not is_out(state.board, playingCheckPos[0]+arah[0], playingCheckPos[1]+arah[1]):
                    playingCheckPos[0] += arah[0]
                    playingCheckPos[1] += arah[1]
                else:
                    break

        #cek streak untuk enemy
        for enemyCheck in nearbyEnemyShape:
            arah = self.direction(position, enemyCheck)
            enemyCheckPos = list(enemyCheck)
            piece = state.board.__getitem__([enemyCheck[0], enemyCheck[1]])
            while(not self.isPiecePlayingShape(state, enemyCheckPos) and  not shape == piece.shape ):
                enemyShapeStreak += 1 
                if not is_out(state.board , enemyCheckPos[0]+arah[0], enemyCheckPos[1]+arah[1]):
                    enemyCheckPos[0] += arah[0]
                    enemyCheckPos[1] += arah[1]
                else:
                    break
        
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

    def colorEvaluate(self, state: State, position: Tuple[int, int], color: ColorConstant) -> int:
        playing = self.whoseTurn(state)
        if playing == GameConstant.PLAYER1:
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        #playing adalah pemain yang sedang turn-nya

        #mendata posisi mana saja yang warnanya sama dengan playing
        nearbyPlayingColor = self.listNearbyColor(state, position, playing)
        #mendata posisi mana saja yang warnanya sama dengan musuh
        nearbyEnemyColor = self.listNearbyColor(state, position, enemy)

        playingColorStreak = 0
        enemyColorStreak = 0

        #cek streak untuk playing jika dipilih position sebagai next step
        for playingCheck in nearbyPlayingColor:
            arah = self.direction(position, playingCheck)
            playingCheckPos = list(playingCheck)
            piece = state.board.__getitem__([playingCheck[0], playingCheck[1]])
            while(self.isPiecePlayingColor(state, playingCheckPos) and color == piece.color):
                playingColorStreak += 1
                if not is_out(state.board, playingCheckPos[0]+arah[0], playingCheckPos[1]+arah[1]):
                    playingCheckPos[0] += arah[0]
                    playingCheckPos[1] += arah[1]
                else:
                    break

        #cek streak untuk enemy jika enemy memilih position sebagai next step
        for enemyCheck in nearbyEnemyColor:
            arah = self.direction(position, enemyCheck)
            enemyCheckPos = list(enemyCheck)
            piece = state.board.__getitem__([enemyCheck[0], enemyCheck[1]])
            while(not self.isPiecePlayingColor(state, enemyCheckPos) and  not color == piece.color  ):
                enemyColorStreak += 1 
                if not is_out(state.board , enemyCheckPos[0]+arah[0], enemyCheckPos[1]+arah[1]):
                    enemyCheckPos[0] += arah[0]
                    enemyCheckPos[1] += arah[1]
                else:
                    break

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

    def isPiecePlayingColor(self, state: State, position: Tuple[int, int]) -> bool:
        playing = self.whoseTurn(state)
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

    def isPiecePlayingShape(self, state: State, position: Tuple[int, int]) -> bool:
        playing = self.whoseTurn(state)
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

    def isPieceP1Shape(self, state: State, position: Tuple[int, int]) -> bool:
        # Cek apakah shape milik player 1

        piece = state.board.__getitem__([position[0], position[1]])
        if piece.shape == GameConstant.PLAYER1_SHAPE:
            return True
        else:
            return False

    def isPieceP1Color(self, state: State, position: Tuple[int, int]) -> bool:
        # Cek apakah color milik player 1

        piece = state.board.__getitem__([position[0], position[1]])
        if piece.color == GameConstant.PLAYER1_COLOR:
            return True
        else:
            return False

    def isBlank(self, state: State, position: Tuple[int, int]) -> bool:
        # cek apakah cell kosong
        piece = state.board.__getitem__(position)
        # true jika BLANK
        if piece.shape == ShapeConstant.BLANK:
            return True
        else:
            return False

    def isOutOfRange(self, state: State, position: Tuple[int,int]) -> bool:
        # if (position[0] < 0 or position[0] > 6 or position[1] < 0 or position[1] > 5):
        #     return True
        # piece = state.board.__getitem__([position[1], position[0]])
        # # true jika selain CIRCLE, CROSS, dan BLANK
        
        # if piece.shape != ShapeConstant.BLANK and piece.shape != ShapeConstant.CIRCLE and piece.shape != ShapeConstant.CROSS:
        #     return True
        # else:
        #     return False
        
        outOfRange = is_out(state.board, position[0], position[1])
        return outOfRange

    def whoseTurn(self, state: State) -> GameConstant:
        # round genap -> P1
        # round ganjil -> P2
        if (state.round % 2 != 0):
            return GameConstant.PLAYER1
        else:
            return GameConstant.PLAYER2

    def listNearbyFilledSpace(self, state: State, position: Tuple[int, int]) -> list:
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
                if ( not self.isOutOfRange(state, newPosition) and not self.isBlank(state, newPosition) and newPosition != position):
                    nearbyFilledSpace.append(newPosition)
        
        return nearbyFilledSpace

    def listNearbyShape(self, state: State, position: Tuple[int, int], playing: GameConstant) -> list:
        # Mencari posisi" yang shape nya sama

        # selected position nearby same shape
        nearbySameShape = []
        # selected position nearby filled space 
        nearbyFilledSpace = self.listNearbyFilledSpace(state, position)

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

    def listNearbyColor(self, state: State, position: Tuple[int, int], playing: GameConstant) -> list:
        # Mencari posisi" yang color nya sama

        # selected position nearby same shape
        nearbySameColor = []
        # selected position nearby filled space 
        nearbyFilledSpace = self.listNearbyFilledSpace(state, position)

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

    def listNearbyGoodSpace(self, state: State, position: Tuple[int, int], playing: GameConstant) -> list:
        # Mencari posisi" yang dapat menambah poin
        # P1 berarti mencari RED atau CIRCLE
        # P2 berarti mencari BLUE atau CROSS

        # selected position nearby same shape
        nearbyGoodSpace = []
        
        # selected position nearby filled space 
        nearbyFilledSpace = self.listNearbyFilledSpace(state, position)

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

    def direction(self, position1: Tuple[int,int], position2: Tuple[int,int]) -> Direction:
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
            
    def getPossibleMoves(self, state: State) -> list:
        # menentukan posisi-posisi yang bisa ditempati

        possibleMoves = []
        totalColumn = 7
        totalRow = 6
        for x in range (totalRow):
            for y in range (totalColumn):
                piecePos = (x,y)
                if (self.isBlank(state, piecePos) and not self.isOutOfRange(state,[y,x])):
                    possibleMoves.append(piecePos)
                    break
        print(possibleMoves)
        # for move in possibleMoves:
        #     print(type(move[1]))
        return possibleMoves