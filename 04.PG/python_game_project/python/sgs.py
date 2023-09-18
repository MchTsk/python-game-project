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


# ******************** 指定のターゲットが存在するか探す ********************
def search_target(target):

    # 指定のターゲットが存在するか
    result = False

    # 指定のターゲットを探す
    for y in range(C.maze_num):
        for x in range(C.maze_num):
            if target == C.ITEM:
                if math.ceil(C.maze[y][x]) == target:
                    result = True
            else:
               if C.maze[y][x] == target:
                    result = True 

    return result


# ******************** 指定のターゲットのx,y座標の取得 ********************
def get_target_coordinate(target):

    # 指定のターゲットのx,y座標
    target_x = 0
    target_y = 0

    # 指定のターゲットの座標を探す
    for y in range(C.maze_num):
        for x in range(C.maze_num):
            if target == C.ITEM:
                if math.ceil(C.maze[y][x]) == target:
                    target_x = x
                    target_y = y
            else:
                if C.maze[y][x] == target:
                    target_x = x
                    target_y = y

    return target_x, target_y


# ******************** 目標をセット ********************
def set_target(target):
    
    # 取得するx,y座標
    x = 0
    y = 0
    # プレイヤーから離す距離
    dis = C.maze_num // 4

    if target == C.ITEM:
        # アイテムの種類をランダムで決定
        rr_item = random.randrange(len(C.pl_item) - 1)
        # アイテム定義(負の数)-アイテム種類(小数1桁)（例：-3.1、-3.2...）
        target = C.ITEM - ((rr_item + 1) / 10)
    
    while True:
        # x,y座標 -> ランダム選択
        x = random.randint(1, C.maze_num-2)
        y = random.randint(1, C.maze_num-2)
        # x,y座標 -> 通路 or コイン
        if C.maze[y][x] == C.ROAD or C.maze[y][x] == C.COIN:
            # プレイヤーと離れている -> ok
            if (x < C.pl_x-dis or C.pl_x+dis < x) and (y < C.pl_y-dis or C.pl_y+dis < y):
                C.maze[y][x] = target
                break
