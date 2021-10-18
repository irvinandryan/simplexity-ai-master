import random
from time import time
from src.ai.heuristic import *
from src.model import board
from src.model.piece import Piece

from src.constant import GameConstant, ShapeConstant
from src.model import State

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        playing = whoseTurn(state)

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

        possibleMoves = getPossibleMoves(state)
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

        # jangan lupa bestMove nya diubah ke Tuple[str,str]

        return bestMove

    def minimize(self, state: State, position: Tuple[int,int], depth, a, b, playing: GameConstant) -> int:
        possibleMoves = getPossibleMoves(state)

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
            return heuristicValue(state, position, shape, color)

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
        possibleMoves = getPossibleMoves(state)

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
            return heuristicValue(state, position, shape, color)

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
        
