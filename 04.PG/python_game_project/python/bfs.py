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


# ******************** distの初期化 ********************
def init_dist():

    # distの初期化
    C.dist = []
    for y in range(C.block_num):
        C.dist.append([0]*C.block_num)

    
# ******************** 幅優先探索法より、目的地のルートをマッピングするために使用(C.fieldのコピー) ********************
def set_dist():

    # distの初期化
    init_dist()

    # フィールドをコピー(WALL or ROADのみ)
    for y in range(C.block_num):
        for x in range(C.block_num):
            if C.field[y][x] == C.EDGE:
                C.dist[y][x] = C.EDGE
            elif C.field[y][x] == C.WALL:
                C.dist[y][x] = C.WALL
            else:
                C.dist[y][x] = C.ROAD
    

# ******************** 幅優先探索法 ********************
def BFS(start_x, start_y, end_x, end_y):

    # フィールドのコピーを作成
    set_dist()

    # ナンバリング用の数字（C.EDGE=1のため、初期は2に設定）
    dist_num = 2

    # x,y方向
    dy = (1, 0, -1, 0)
    dx = (0, 1, 0, -1)

    # キュー：初期値の追加
    C.que = deque()
    C.que.append((start_x, start_y))

    # スタート位置をナンバリング
    C.dist[start_y][start_x] = dist_num

    # 目標の位置まで探索したら、True
    target_search = False
    
    while len(C.que)>0:
        # 現在地(x,y)を取得
        now_pos = C.que.popleft()
        x, y = now_pos

        # ナンバリング
        dist_num += 1
        
        # 上下左右の4方向
        for di in range(4):
            nx = x + dx[di]
            ny = y + dy[di]
            
            # フィールドの範囲外はとばす
            if (nx<0 or nx>=C.block_num or ny<0 or ny>=C.block_num): continue
            # 壁とナンバリング済みのマスはとばす
            if (C.dist[ny][nx] >= C.WALL): continue

            # 探索終了：目標の位置にたどり着いた場合
            if nx == end_x and ny == end_y:
                # ナンバリング
                C.dist[ny][nx] = dist_num
                target_search = True
                break

            # ナンバリング
            C.dist[ny][nx] = dist_num
            # 次の探索
            C.que.append((nx, ny))

        # while文を抜ける：プレイヤーの探索をした場合
        if target_search == True:
            break


# ******************** 幅優先探索法(BFS)から次の移動方向を取得 ********************
def next_direction(start_x, start_y, end_x, end_y):
    
    dist_x = end_x
    dist_y = end_y
    dist_num = C.dist[end_y][end_x]

    # 次の移動方向
    next_dir = 0

    while True:
        # 次の移動方向
        dist_num -= 1

        # 上方向
        if C.dist[dist_y-1][dist_x] == dist_num:
            dist_y -= 1
            next_dir = C.DIR_DOWN
        # 右方向
        elif C.dist[dist_y][dist_x+1] == dist_num:
            dist_x += 1
            next_dir = C.DIR_LEFT
        # 下方向
        elif C.dist[dist_y+1][dist_x] == dist_num:
            dist_y += 1
            next_dir = C.DIR_UP
        # 左方向
        elif C.dist[dist_y][dist_x-1] == dist_num:
            dist_x -= 1
            next_dir = C.DIR_RIGHT

        # エネミーの位置まで来たらループを抜ける
        if dist_x == start_x and dist_y == start_y:
            break

    return next_dir
