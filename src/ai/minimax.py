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

        #minimax algorithm
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        
        playing = self.whoseTurn(state)
        if playing == GameConstant.PLAYER1:
            playingShape = GameConstant.PLAYER1_SHAPE
            enemyShape = GameConstant.PLAYER2_SHAPE
        else:
            playingShape = GameConstant.PLAYER2_SHAPE
            enemyShape = GameConstant.PLAYER1_SHAPE

        # bestPosition = self.minimax(state, playing)

        # bestColumn = bestPosition[1]

        if state.players[n_player].quota[playingShape] > 0:
            chosenShape = playingShape
        else:
            chosenShape = enemyShape

        best_movement = self.minimaxjo(state, 3, -99999, 99999, playing)[0], chosenShape

        return best_movement

    # def minimax3(self, state: State, depth: int, playing: GameConstant) -> Tuple[int,int]:

    #     possibleMoves = self.getPossibleMoves(state)
    #     playing = self.whoseTurn(state)

    #     if playing == GameConstant.PLAYER1:
    #         playingShape = GameConstant.PLAYER1_SHAPE
    #         playingColor = GameConstant.PLAYER1_COLOR
    #         enemyShape = GameConstant.PLAYER2_SHAPE
    #         enemyShape = GameConstant.PLAYER2_COLOR
    #     else:
    #         playingShape = GameConstant.PLAYER2_SHAPE
    #         playingColor = GameConstant.PLAYER2_COLOR
    #         enemyShape = GameConstant.PLAYER1_SHAPE
    #         enemyShape = GameConstant.PLAYER1_COLOR

    #     for move in possibleMoves:
    #         # basis
    #         if (depth == 0 or is_win(state.board)):
    #             return self.heuristicValue(state, move, playingShape, playingColor)
                
    #         # rekursif
    #         if (playing == GameConstant.PLAYER1):
    #             # maximizing
    #             value = -9999
                
    #             pass
    #         else:
    #             # minimizing
    #             pass


    def minimax(self, state: State, depth: int, playing: GameConstant) -> Tuple[int,int]:
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

        if is_full(state.board):
            return ()
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
            n_player = 0
            playingShape = GameConstant.PLAYER1_SHAPE
            playingColor = GameConstant.PLAYER1_COLOR
        else:
            tempPiece = Piece(GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)
            n_player = 1
            playingShape = GameConstant.PLAYER2_SHAPE
            playingColor = GameConstant.PLAYER2_COLOR
        tempState = state
        tempState.round += 1
        # tempState.board.set_piece(position[0], position[1], tempPiece)
        if tempState.board[position[0], position[1]].shape == ShapeConstant.BLANK:
            piece = Piece(playingShape, GameConstant.PLAYER_COLOR[n_player])
            tempState.board.set_piece(position[0], position[1], piece)
            tempState.players[n_player].quota[playingShape] -= 1
        return tempState
        
    # state, position, bentuk, warna
    def heuristicValue(self, state: State):
        # input : -> state    : state sekarang
        #         -> player   : player yang bermain sekarang
        
        # total value
        totalValue = self.shapeEvaluate(state) + self.colorEvaluate(state)

        return totalValue

    def shapeEvaluate(self, state: State) -> int:
        playingShapeStreak = [0, 0]
        enemyShapeStreak = [0, 0]

        for row in range(state.board.row):
            for col in range(state.board.col):
                if (not self.isBlank(state, [row,col])):
                    piece = state.board[row, col]

                    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                    mark = 0
                    enemyMark = 0
                    for row_ax, col_ax in streak_way:
                        row_ = row + row_ax
                        col_ = col + col_ax
                        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                            if (is_out(state.board, row_, col_)):
                                break
                            row_ += row_ax
                            col_ += col_ax
                            if (piece.shape == GameConstant.PLAYER1_SHAPE):
                                mark += 1
                            elif (piece.shape == GameConstant.PLAYER2_SHAPE):
                                enemyMark += 1

                        if (mark == 3):
                            playingShapeStreak[1] += 1
                        elif (mark == 2):
                            playingShapeStreak[0] += 1

                        if (enemyMark == 3):
                            enemyShapeStreak[1] += 1
                        elif (enemyMark == 2):
                            enemyShapeStreak[0] += 1

                        mark = 0
                        enemyMark = 0
                    
                    playingShapeValue = playingShapeStreak[0] * 5 + playingShapeStreak[1] * 10
                    enemyShapeValue = enemyShapeStreak[0] * 5 + enemyShapeStreak[1] * 10
                    shapeStreak = playingShapeValue - enemyShapeValue
                    return shapeStreak

    def colorEvaluate(self, state: State) -> int:
        playingColorStreak = [0, 0]
        enemyColorStreak = [0, 0]

        for row in range(state.board.row):
            for col in range(state.board.col):
                if (not self.isBlank(state, [row,col])):
                    piece = state.board[row, col]

                    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                    mark = 0
                    enemyMark = 0
                    for row_ax, col_ax in streak_way:
                        row_ = row + row_ax
                        col_ = col + col_ax
                        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                            if (is_out(state.board, row_, col_)):
                                break
                            row_ += row_ax
                            col_ += col_ax
                            if (piece.color == GameConstant.PLAYER1_COLOR):
                                mark += 1
                            elif (piece.color == GameConstant.PLAYER2_COLOR):
                                enemyMark += 1

                        if (mark == 3):
                            playingColorStreak[1] += 1
                        elif (mark == 2):
                            playingColorStreak[0] += 1

                        if (enemyMark == 3):
                            enemyColorStreak[1] += 1
                        elif (enemyMark == 2):
                            enemyColorStreak[0] += 1

                        mark = 0
                        enemyMark = 0
                    
                    playingColorValue = playingColorStreak[0] * 3 + playingColorStreak[1] * 7
                    enemyColorValue = enemyColorStreak[0] * 3 + enemyColorStreak[1] * 7
                    ColorStreak = playingColorValue - enemyColorValue
                    return ColorStreak


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
                if (self.isBlank(state, piecePos) and not self.isOutOfRange(state,[x,y])):
                    possibleMoves.append(piecePos)
                    break
        print(possibleMoves)
        # for move in possibleMoves:
        #     print(type(move[1]))
        return possibleMoves


    def minimax3(self, state: State, depth: int, playing: GameConstant) -> Tuple[int,int]:

        possibleMoves = self.getPossibleMoves(state)
        playing = self.whoseTurn(state)

        if playing == GameConstant.PLAYER1:
            playingShape = GameConstant.PLAYER1_SHAPE
            playingColor = GameConstant.PLAYER1_COLOR
            enemyShape = GameConstant.PLAYER2_SHAPE
            enemyShape = GameConstant.PLAYER2_COLOR
        else:
            playingShape = GameConstant.PLAYER2_SHAPE
            playingColor = GameConstant.PLAYER2_COLOR
            enemyShape = GameConstant.PLAYER1_SHAPE
            enemyShape = GameConstant.PLAYER1_COLOR

        for move in possibleMoves:
            # basis
            if (depth == 0 or is_win(state.board)):
                return self.heuristicValue(state, move, playingShape, playingColor)
                
            # rekursif
            if (playing == GameConstant.PLAYER1):
                self.maximizing3(state, 3, playing)
            else:
                self.minimizing3(state, 3, playing)


    def minimaxjo(self, state: State, depth: int, alpha: int, beta: int, playing: GameConstant) -> tuple[int,int]:
        if (playing == GameConstant.PLAYER1):
            enemy = GameConstant.PLAYER2
        else:
            enemy = GameConstant.PLAYER1

        possibleMoves = self.getPossibleMoves(state)
        iswin = is_win(state.board)
        if (depth == 0 or iswin or is_full(state.board)):
            if iswin:
                if (iswin[0] == GameConstant.PLAYER1_SHAPE):
                    return (None, 99999)
                elif (iswin[0] == GameConstant.PLAYER2_SHAPE):
                    return (None, -99999)
            elif is_full(state.board):
                return (None, 0)
            else: 
                # depth == 0
                return (None, self.heuristicValue(state))

        if (playing == GameConstant.PLAYER1):
            # maximizing
            value = -99999
            column = random.choice(possibleMoves)[1]
            for row, col in possibleMoves:
                tempState = self.tempMove(state, [row,col], playing)
                new_score = self.minimaxjo(tempState, depth-1, alpha, beta, enemy)[1]

                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else: # player 2
            # minimizing
            value = 99999
            column = random.choice(possibleMoves)
            for row, col in possibleMoves:
                tempState = self.tempMove(state, [row,col], playing)
                new_score = self.minimaxjo(tempState, depth-1, alpha, beta, enemy)[1]

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

