import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import config as C


# ******************** フィールドの初期化 ********************
def init_field():

    # フィールドの１辺のブロック数を増加
    C.block_num += 1

    # フィールドの初期化
    C.field = []
    for y in range(C.block_num):
        # 配列の中にC.block_num分の「0」の配列を作成。for文でC.block_num分作成。各マスの情報が格納される
        C.field.append([0]*C.block_num)

# ******************** フィールドの自動生成  ********************
def make_field():
    
    # フィールドの初期化
    init_field()

    # 方向：上、右、下、左
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    # フィールド端を壁にする
    for x in range(C.block_num):
        C.field[0][x] = C.EDGE
        C.field[C.block_num-1][x] = C.EDGE
    for y in range(C.block_num-1):
        C.field[y][0] = C.EDGE
        C.field[y][C.block_num-1] = C.EDGE

    # フィールドの中（端以外）を全て通路にする
    for y in range(1, C.block_num-1):
        for x in range(1, C.block_num-1):
            C.field[y][x] = C.ROAD

    # 【棒倒し方でフィールドを作成】
    # 等間隔に壁を作る
    for y in range(2, C.block_num-2, 2):
        for x in range(2, C.block_num-2, 2):
            C.field[y][x] = C.WALL
    
    # 等間隔に作った壁の隣に、壁を作る
    for y in range(2, C.block_num-2, 2):
        for x in range(2, C.block_num-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            C.field[y+YP[d]][x+XP[d]] = C.WALL
