import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import item
from . import config as C


# ******************** プレイヤーの移動 ********************
def move_player(key):
    
    # プレイヤーの移動速度
    if C.tmr%2 == 0:
        return
    
    # キー入力：上方向
    if key[pygame.K_UP] == True:
        C.pl_d = C.DIR_UP
        # 移動方向が壁以外
        if C.maze[C.pl_y-1][C.pl_x] != C.EDGE and C.maze[C.pl_y-1][C.pl_x] != C.WALL:
            C.pl_y -= 1
        # 壁 + 赤色のパックマン
        else:
            if C.pl_col == C.COLOR_RED and C.maze[C.pl_y-1][C.pl_x] == C.WALL:
                C.snd_break_wall.play()
                C.maze[C.pl_y-1][C.pl_x] = C.ROAD
                C.pl_y -= 1
                C.pl_wallbreak -= 1
                if C.pl_wallbreak == 0:
                    item.item_effect_off()
                
    # キー入力：右方向
    if key[pygame.K_RIGHT] == True:
        C.pl_d = C.DIR_RIGHT
        # 移動方向が壁以外
        if C.maze[C.pl_y][C.pl_x+1] != C.EDGE and C.maze[C.pl_y][C.pl_x+1] != C.WALL:
            C.pl_x += 1
        # 壁 + 赤色のパックマン
        else:
            if C.pl_col == C.COLOR_RED and C.maze[C.pl_y][C.pl_x+1] == C.WALL:
                C.snd_break_wall.play()
                C.maze[C.pl_y][C.pl_x+1] = C.ROAD
                C.pl_x += 1
                C.pl_wallbreak -= 1
                if C.pl_wallbreak == 0:
                    item.item_effect_off()
                
    # キー入力：下方向
    if key[pygame.K_DOWN] == True:
        C.pl_d = C.DIR_DOWN
        # 移動方向が壁以外
        if C.maze[C.pl_y+1][C.pl_x] != C.EDGE and C.maze[C.pl_y+1][C.pl_x] != C.WALL:
            C.pl_y += 1
        # 壁 + 赤色のパックマン
        else:
            if C.pl_col == C.COLOR_RED and C.maze[C.pl_y+1][C.pl_x] == C.WALL:
                C.snd_break_wall.play()
                C.maze[C.pl_y+1][C.pl_x] = C.ROAD
                C.pl_y += 1
                C.pl_wallbreak -= 1
                if C.pl_wallbreak == 0:
                    item.item_effect_off()
                
    # キー入力：左方向
    if key[pygame.K_LEFT] == True:
        C.pl_d = C.DIR_LEFT
        # 移動方向が壁以外
        if C.maze[C.pl_y][C.pl_x-1] != C.EDGE and C.maze[C.pl_y][C.pl_x-1] != C.WALL:
            C.pl_x -= 1
        # 壁 + 赤色のパックマン
        else:
            if C.pl_col == C.COLOR_RED and C.maze[C.pl_y][C.pl_x-1] == C.WALL:
                C.snd_break_wall.play()
                C.maze[C.pl_y][C.pl_x-1] = C.ROAD
                C.pl_x -= 1
                C.pl_wallbreak -= 1
                if C.pl_wallbreak == 0:
                    item.item_effect_off()
