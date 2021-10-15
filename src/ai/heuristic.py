import random
from time import time

from src.constant import ShapeConstant, ColorConstant
from src.model import State

from typing import Tuple, List


# state, position, bentuk, warna
def heuristicValue(position: Tuple[int, int], shape: ShapeConstant, color: ColorConstant):

    # shapeEvaluate
    shapeValue = shapeEvaluate(position, shape)

    # colorEvaluate
    colorValue = colorEvaluate(position, color)

    # total value
    totalValue = shapeValue + colorValue
    
    return totalValue


def shapeEvaluate(position: Tuple[int, int], shape: ShapeConstant):
    state = State()

    shapeValue = 0
    
    return shapeValue

def colorEvaluate(position: Tuple[int, int], color: ColorConstant):
    state = State()
    
    colorValue = 0
    
    return colorValue