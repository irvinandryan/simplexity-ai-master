import pickle
from typing import Tuple
from mechanic import game
from model import player
from model.config import Config
from model.player import Player

from src.model import Piece, Board, State
from src.constant import ColorConstant, ShapeConstant, GameConstant

def isMyShape(state: State, gameconstant: GameConstant, row: int, col: int):
#cek apakah shape milik player 1
    piece = state.board.__getitem__([row,col])
    if piece.shape == gameconstant.PLAYER1_SHAPE:
        return True
    else:
        return False

def isMyColor(state: State, gameconstant: GameConstant, row: int, col: int):
#cek apakah color milik player 1
    piece = state.board.__getitem__([row,col])
    if piece.color == gameconstant.PLAYER1_COLOR:
        return True
    else:
        return False

def isBlank(state: State, row: int, col: int):
#cek apakah cell kosong
    if state.board[row, col].shape == ShapeConstant.BLANK:
        return True
    else:
        return False

def findBlankRow(state: State, col: int, config: Config):
#mencari baris ke berapa yang kosong untuk setiap column
    for row in range(config.row):
        return (isBlank(state, row, col))

def evaluationFunction(state: State, gameconstant: GameConstant, config: Config):
#belom jadi    
    streak = 0
    currentRow = 0
    currentCol = 0

    while True:
        for col in range(config.col):
            for row in range(config.row):
                if isMyShape(state, gameconstant, currentCol, currentRow):
                    streak += 1
                    currentRow += 1
                    currentCol += 1

                else:
                    False