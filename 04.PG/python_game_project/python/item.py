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


# ******************** アイテムの使用 ********************
def use_item(key):
    
    # 赤色のパックマン（壁破壊）
    if C.course >= 5 and key[pygame.K_1] == True and C.pl_item[C.COLOR_RED] > 0 and C.pl_col != C.COLOR_RED:
        C.snd_pacman_red.play()
        item_effect_off()
        C.pl_item[C.COLOR_RED] -= 1
        C.pl_col = C.COLOR_RED
        C.item_use = True
        C.item_time = C.FPS * 8
        C.pl_wallbreak = 3
    # 青色のパックマン（無敵）
    if C.course >= 10 and key[pygame.K_2] == True and C.pl_item[C.COLOR_BLUE] > 0 and C.pl_col != C.COLOR_BLUE:
        C.snd_pacman_blue.play()
        item_effect_off()
        C.pl_item[C.COLOR_BLUE] -= 1
        C.pl_col = C.COLOR_BLUE
        # C.pl_fast = True
        C.item_use = True
        C.item_time = C.FPS * 18
    # 緑色のパックマン（ゴール矢印）
    if C.course >= 15 and key[pygame.K_3] == True and C.pl_item[C.COLOR_GREEN] > 0 and C.pl_col != C.COLOR_GREEN:
        C.snd_pacman_green.play()
        item_effect_off()
        C.pl_item[C.COLOR_GREEN] -= 1
        C.pl_col = C.COLOR_GREEN
        C.item_use = True
        C.item_time = C.FPS * 23
    # 黄色のパックマン（視界範囲拡大）
    if C.course >= 20 and key[pygame.K_4] == True and C.pl_item[C.COLOR_YELLOW] > 0 and C.pl_col != C.COLOR_YELLOW:
        C.snd_pacman_yellow.play()
        item_effect_off()
        C.pl_item[C.COLOR_YELLOW] -= 1
        C.pl_col = C.COLOR_YELLOW
        C.pl_scope = 1
        C.item_use = True
        C.item_time = C.FPS * 17
    # 茶色のパックマン（オールエネミースタン）
    if C.course >= 25 and key[pygame.K_5] == True and C.pl_item[C.COLOR_BROWN] > 0 and C.pl_col != C.COLOR_BROWN:
        C.snd_pacman_brown.play()
        item_effect_off()
        C.pl_item[C.COLOR_BROWN] -= 1
        C.pl_col = C.COLOR_BROWN
        C.item_use = True
        C.item_time = C.FPS * 7

        
# ******************** アイテムの効果を解除 ********************
def item_effect_off():

    # アイテムの使用中：False ／ 使用時間：0
    C.item_use = False
    C.item_time = 0

    # パックマンの色：黒 ／ 移動速度：通常 ／ 視野の範囲：通常
    C.pl_col = C.COLOR_BLACK
    C.pl_fast = False
    C.pl_scope = 0


# ******************** アイテムを生成するか判定 -> 生成を行う ********************
def chk_and_gen_item():

    # 迷路上のアイテムの数をカウント
    count_item = 0
    for y in range(C.maze_num):
        for x in range(C.maze_num):
            if C.maze[y][x] == C.ITEM:
                count_item += 1
                
    # アイテムが最大数までない + アイテムの再生成時間がある
    if count_item < C.item_max and C.item_generate_time:
        C.item_generate_time -= 1
    # アイテムが最大数までない + アイテムの再生成時間が0 -> アイテムの生成
    elif count_item < C.item_max and C.item_generate_time == 0:
        sgs.set_target(C.ITEM)
        C.item_generate_time = C.FPS * 15
