import random
from time import time
from src.ai.heuristic import *
from src.model import board
from src.model.piece import Piece

from src.constant import ShapeConstant, GameConstant
from src.model import State

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        playing = whoseTurn(state)
        if playing == GameConstant.PLAYER1:
            shape = GameConstant.PLAYER1_SHAPE
            enemyShape = GameConstant.PLAYER2_SHAPE
        else:
            shape = GameConstant.PLAYER2_SHAPE
            enemyShape = GameConstant.PLAYER1_SHAPE

        bestPosition = self.stochasticHC(state, playing)
        bestColumn = str(bestPosition[1])

        if state.players[n_player].quota[shape] > 0:
            chosenShape = shape
        else:
            chosenShape = enemyShape

        #best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        best_movement = (bestColumn, chosenShape)
        return best_movement
    
    def stochasticHC(self, state: State, playing: GameConstant) -> Tuple[int,int]:
        playing = whoseTurn(state)
        if (playing == GameConstant.PLAYER1):   
            shape = GameConstant.PLAYER1_SHAPE
            color = GameConstant.PLAYER1_COLOR
        else:
            shape = GameConstant.PLAYER2_SHAPE
            color = GameConstant.PLAYER2_COLOR

        posibleMoves = getPossibleMoves(state)
        posibleMovesValue = []

        for position in posibleMoves:
            positionValue = heuristicValue(state, posibleMoves[position], shape, color)
            posibleMovesValue.append(positionValue)

        highestValue = max(posibleMovesValue)
        highestValueIdx = posibleMovesValue.index(highestValue)
        nextMove = posibleMoves[highestValueIdx]
        return nextMove
