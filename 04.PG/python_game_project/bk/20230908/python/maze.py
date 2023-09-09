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


# ******************** 迷路の初期化 ********************
def init_maze():

    # 迷路の大きさを拡大
    C.maze_num += 1

    # 迷路の初期化
    C.maze = []
    for y in range(C.maze_num):
        # 配列の中にC.maze_num分の「0」の配列を作成。for文でC.maze_num分作成。各マスの情報が格納される
        C.maze.append([0]*C.maze_num)

# ******************** 迷路の自動生成  ********************
def make_maze():
    
    # 迷路の初期化
    init_maze()

    # 方向：上、右、下、左
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    # フィールド端を壁にする
    for x in range(C.maze_num):
        C.maze[0][x] = C.EDGE
        C.maze[C.maze_num-1][x] = C.EDGE
    for y in range(C.maze_num-1):
        C.maze[y][0] = C.EDGE
        C.maze[y][C.maze_num-1] = C.EDGE

    # フィールドの中（端以外）を全て通路にする
    for y in range(1, C.maze_num-1):
        for x in range(1, C.maze_num-1):
            C.maze[y][x] = C.ROAD

    # 【棒倒し方で迷路を作成】
    # 等間隔に壁を作る
    for y in range(2, C.maze_num-2, 2):
        for x in range(2, C.maze_num-2, 2):
            C.maze[y][x] = C.WALL
    
    # 等間隔に作った壁の隣に、壁を作る
    for y in range(2, C.maze_num-2, 2):
        for x in range(2, C.maze_num-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            C.maze[y+YP[d]][x+XP[d]] = C.WALL
