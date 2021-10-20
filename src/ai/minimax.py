import random
from time import time
from src.model import board
from src.model.piece import Piece
from src.utility import *

from src.constant import GameConstant, ShapeConstant, ColorConstant, Direction
from src.model import State

from typing import Tuple, List


class MinimaxGroup39:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        #minimax algorithm
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        
        if n_player == 0:
            playing = GameConstant.PLAYER1
        else:
            playing = GameConstant.PLAYER2
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

        if n_player == 0:
            best_movement = self.minimax(state.board, 5, -99999, 99999, True)[0], chosenShape
        else:
            best_movement = self.minimax(state.board, 5, -99999, 99999, False)[0], chosenShape

        return best_movement
        
    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool) -> tuple[int,int]:
        possibleMoves = self.getPossibleMoves(board)
        iswin = is_win(board)
        # basis
        if (depth == 0 or iswin or is_full(board)):
            if iswin:
                if (iswin[0] == GameConstant.PLAYER1_SHAPE or iswin[1] == GameConstant.PLAYER1_COLOR):
                    return (None, 99999)
                elif (iswin[0] == GameConstant.PLAYER2_SHAPE or iswin[1] == GameConstant.PLAYER2_COLOR):
                    return (None, -99999)
            elif is_full(board):
                return (None, 0)
            else: 
                # depth == 0
                return (None, self.heuristicValue(board))

        if maximizingPlayer:
            # maximizing
            value = -99999
            column = random.choice(possibleMoves)[1]
            for row, col in possibleMoves:
                tempBoard = self.copyBoard(board)
                tempBoard.set_piece(row,col,Piece(GameConstant.PLAYER1_SHAPE,GameConstant.PLAYER1_COLOR))
                
                new_score = self.minimax(tempBoard, depth-1, alpha, beta, False)[1]
                if new_score >= value:
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
                tempBoard = self.copyBoard(board)
                tempBoard.set_piece(row,col,Piece(GameConstant.PLAYER2_SHAPE,GameConstant.PLAYER2_COLOR))
                new_score = self.minimax(tempBoard, depth-1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha > beta:
                    break
            return column, value

    def heuristicValue(self, board: Board):
        # input : -> state    : state sekarang
        #         -> player   : player yang bermain sekarang
        
        # total value
        totalValue = self.shapeEvaluate(board) + self.colorEvaluate(board)

        return totalValue

    def shapeEvaluate(self, board: Board) -> int:
        playingShapeStreak = [0, 0]
        enemyShapeStreak = [0, 0]

        for row in range(board.row):
            for col in range(board.col):
                if (not self.isBlank(board, [row,col])):
                    piece = board[row, col]

                    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                    mark = 0
                    enemyMark = 0
                    for row_ax, col_ax in streak_way:
                        row_ = row + row_ax
                        col_ = col + col_ax
                        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                            if (is_out(board, row_, col_)):
                                break
                            
                            if (piece.shape == GameConstant.PLAYER1_SHAPE):
                                mark += 1
                            elif (piece.shape == GameConstant.PLAYER2_SHAPE):
                                enemyMark += 1
                            if piece.shape != board[row_, col_].shape:
                                break
                            row_ += row_ax
                            col_ += col_ax

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
                    
                    playingShapeValue = playingShapeStreak[0] * 50 + playingShapeStreak[1] * 109
                    enemyShapeValue = enemyShapeStreak[0] * 50 + enemyShapeStreak[1] * 500
                    shapeStreak = playingShapeValue - enemyShapeValue
                    return shapeStreak

    def colorEvaluate(self, board: Board) -> int:
        playingColorStreak = [0, 0]
        enemyColorStreak = [0, 0]

        for row in range(board.row):
            for col in range(board.col):
                if (not self.isBlank(board, [row,col])):
                    piece = board[row, col]

                    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                    mark = 0
                    enemyMark = 0
                    for row_ax, col_ax in streak_way:
                        row_ = row + row_ax
                        col_ = col + col_ax
                        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                            if (is_out(board, row_, col_)):
                                break   
                            if (piece.color == GameConstant.PLAYER1_COLOR):
                                mark += 1
                            elif (piece.color == GameConstant.PLAYER2_COLOR):
                                enemyMark += 1
                            if piece.color != board[row_, col_].shape:
                                break
                            row_ += row_ax
                            col_ += col_ax

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
                    
                    playingColorValue = playingColorStreak[0] * 25 + playingColorStreak[1] * 75
                    enemyColorValue = enemyColorStreak[0] * 25 + enemyColorStreak[1] * 500
                    ColorStreak = playingColorValue - enemyColorValue
                    return ColorStreak

    def isBlank(self, board: Board, position: Tuple[int, int]) -> bool:
        # cek apakah cell kosong
        piece = board[position[0], position[1]]
        # true jika BLANK
        if piece.shape == ShapeConstant.BLANK:
            return True
        else:
            return False
   
    def getPossibleMoves(self, board: Board) -> list:
        # menentukan posisi-posisi yang bisa ditempati

        possibleMoves = []
        totalColumn = board.col
        totalRow = board.row
        for x in range (0, totalColumn, 1): # 0,1,2,3,4,5,6
            for y in range (totalRow-1, -1, -1): # 5,4,3,2,1,0
                piecePos = (y,x)
                if (self.isBlank(board, piecePos) and not is_out(board,y,x)):
                    possibleMoves.append(piecePos)
                    break
        # print(possibleMoves)
        # for move in possibleMoves:
        #     print(type(move[1]))
        return possibleMoves

    def copyBoard(self, board: Board) -> Board:
        boardCopy = Board(board.row, board.col)
        for x in range(board.row):
            for y in range(board.col):
                boardCopy.set_piece(x,y,board[x,y])
        return boardCopy