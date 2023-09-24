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


# ******************** 指定のオブジェクトが存在するか探す ********************
def search_object(dov):

    # 指定のオブジェクトが存在するか
    result = False

    # 指定のオブジェクトを探す
    for y in range(C.block_num):
        for x in range(C.block_num):
            if dov == C.ITEM:
                if math.ceil(C.field[y][x]) == dov:
                    result = True
            else:
               if C.field[y][x] == dov:
                    result = True 

    return result


# ******************** 指定のオブジェクトのX、Y軸座標の情報を取得 ********************
def get_object_xy(dov):

    # 指定のオブジェクトのx,y座標
    dov_x = 0
    dov_y = 0

    # 指定のオブジェクトの座標を探す
    for y in range(C.block_num):
        for x in range(C.block_num):
            if dov == C.ITEM:
                if math.ceil(C.field[y][x]) == dov:
                    dov_x = x
                    dov_y = y
            else:
                if C.field[y][x] == dov:
                    dov_x = x
                    dov_y = y

    return dov_x, dov_y


# ******************** オブジェクトセット ********************
def set_object(dov):
    
    # 取得するx,y座標
    x = 0
    y = 0
    # プレイヤーから離す距離
    dis = C.block_num // 4

    if dov == C.ITEM:
        # アイテムの種類をランダムで決定
        rr_item = random.randrange(len(C.pl_item) - 1)
        # アイテム定義(負の数)-アイテム種類(小数1桁)（例：-3.1、-3.2...）
        dov = C.ITEM - ((rr_item + 1) / 10)
    
    while True:
        # x,y座標 -> ランダム選択
        x = random.randint(1, C.block_num-2)
        y = random.randint(1, C.block_num-2)
        # x,y座標 -> 通路 or ポイント
        if C.field[y][x] == C.ROAD or C.field[y][x] == C.POINT:
            # プレイヤーと離れている -> ok
            if (x < C.pl_x-dis or C.pl_x+dis < x) and (y < C.pl_y-dis or C.pl_y+dis < y):
                C.field[y][x] = dov
                break
