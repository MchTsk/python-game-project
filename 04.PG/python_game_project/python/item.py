import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import sgs
from . import config as C


# ******************** アイテムの使用 ********************
def use_item(key):
    
    # 赤プレイヤー（壁破壊）
    if C.course > 5 and key[pygame.K_1] == True and C.pl_item[C.COLOR_RED] > 0 and C.pl_col != C.COLOR_RED:
        C.se_pl_red.play()
        item_disable()
        C.pl_item[C.COLOR_RED] -= 1
        C.pl_col = C.COLOR_RED
        C.item_use = True
        C.item_time = C.FPS * 8
        C.pl_wallbreak = 3
    # 青プレイヤー（無敵）
    if C.course > 10 and key[pygame.K_2] == True and C.pl_item[C.COLOR_BLUE] > 0 and C.pl_col != C.COLOR_BLUE:
        C.se_pl_blue.play()
        item_disable()
        C.pl_item[C.COLOR_BLUE] -= 1
        C.pl_col = C.COLOR_BLUE
        C.item_use = True
        C.item_time = C.FPS * 18
    # 緑プレイヤー（ポイント2倍）
    if C.course > 15 and key[pygame.K_3] == True and C.pl_item[C.COLOR_GREEN] > 0 and C.pl_col != C.COLOR_GREEN:
        C.se_pl_green.play()
        item_disable()
        C.pl_item[C.COLOR_GREEN] -= 1
        C.pl_col = C.COLOR_GREEN
        C.item_use = True
        C.item_time = C.FPS * 10
    # 黄プレイヤー（視界範囲拡大）
    if C.course > 20 and key[pygame.K_4] == True and C.pl_item[C.COLOR_YELLOW] > 0 and C.pl_col != C.COLOR_YELLOW:
        C.se_pl_yellow.play()
        item_disable()
        C.pl_item[C.COLOR_YELLOW] -= 1
        C.pl_col = C.COLOR_YELLOW
        C.pl_fov = 1
        C.item_use = True
        C.item_time = C.FPS * 17
    # 橙プレイヤー（オールエネミースタン）
    if C.course > 25 and key[pygame.K_5] == True and C.pl_item[C.COLOR_ORANGE] > 0 and C.pl_col != C.COLOR_ORANGE:
        C.se_pl_orange.play()
        item_disable()
        C.pl_item[C.COLOR_ORANGE] -= 1
        C.pl_col = C.COLOR_ORANGE
        C.item_use = True
        C.item_time = C.FPS * 7

        
# ******************** アイテムの効果を解除 ********************
def item_disable():

    C.item_use = False
    C.item_time = 0
    C.pl_col = C.COLOR_BLACK
    C.pl_fov = 0


# ******************** アイテムを生成するか判定 -> 生成を行う ********************
def chk_and_gen_item():

    # フィールド上のアイテムの数をカウント
    count_item = 0
    for y in range(C.block_num):
        for x in range(C.block_num):
            if math.ceil(C.field[y][x]) == C.ITEM:
                count_item += 1

    # アイテムが最大数までない + アイテムの再生成時間がある
    if count_item < C.item_max and C.item_generate_time > 0:
        C.item_generate_time -= 1
    # アイテムが最大数までない + アイテムの再生成時間が0 -> アイテムの生成
    elif count_item < C.item_max and C.item_generate_time == 0:
        sgs.set_object(C.ITEM)
        C.item_generate_time = C.FPS * 15


# ******************** アイテムの種類番号を取得 ********************
def get_item_num(item_num):

    # [小数点以下の数字-1]を抽出
    str_item_num = str(item_num)
    idx_item = str_item_num.find('.')
    idx_itm_list = int(str_item_num[idx_item+1:])

    return idx_itm_list
