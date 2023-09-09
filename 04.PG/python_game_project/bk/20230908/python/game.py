import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import enemy
from . import item
from . import sgs
from . import config as C


# ******************** ゲームの初期化 ********************
def init_game():

    # 迷路の数
    C.maze_num = 17

    # コースの階層
    C.course = 0

    # プレイヤー情報
    C.pl_life = 2
    C.pl_item = [2]*6
    C.pl_coin = 0
    C.pl_muteki = 0
    C.pl_wallbreak = 0

    # アイテムの効果を無効
    item.item_effect_off()
    

# ******************** ゲームの初期配置／設定 ********************
def init_game_place():

    # エネミー
    C.emy_max = C.maze_num // 5     # エネミーの最大数（C.maze_num：初期は17+1）
    C.emy_num_max = False         # エネミーが最大数いるか(初期時はいない)
    C.emy_time = C.FPS * 20         # エネミーを再生成するまでの時間
    enemy.init_enemy()                # エネミーの初期化

    # アイテム
    C.item_max = C.maze_num // 5        # アイテムの最大数
    C.item_generate_time = C.FPS * 60   # アイテムを再生成するまでの時間

    # プレイヤーの配置
    while True:
        C.pl_x = random.randint(1, C.maze_num-2)
        C.pl_y = random.randint(1, C.maze_num-2)
        if C.maze[C.pl_y][C.pl_x] == C.ROAD:
            break

    # エネミーの配置
    for i in range(C.maze_num // 10):
        enemy.bring_enemy()

    # ゴールの配置
    sgs.set_target(C.GOAL)
    C.goal_f = True

    # アイテムの配置
    for n in range(C.maze_num // 10):
        sgs.set_target(C.ITEM)
        
    # コインの配置
    for y in range(C.maze_num):
        for x in range(C.maze_num):
            if C.maze[y][x] == C.ROAD:
                C.maze[y][x] = C.COIN

# ******************** ゴールを生成するか判定 -> 生成を行う ********************
def chk_and_gen_goal():
    
    # ゴールがない + ゴールの再生成時間がある
    if C.goal_f == False and C.goal_generate_time > 0:
        C.goal_generate_time -= 1
    # ゴールがない + ゴールの再生成時間が0 -> ゴールの生成
    elif C.goal_f == False and C.goal_generate_time == 0:
        sgs.set_target(C.GOAL)
        C.goal_f = True


# ******************** ヒットチェック ********************
def hit_check():

    # プレイヤー：コインを拾う
    if C.maze[C.pl_y][C.pl_x] == C.COIN:
        C.snd_get_coin.play()
        C.maze[C.pl_y][C.pl_x] = C.ROAD
        C.pl_coin += 1
        C.point += 1
        # コインを[pll_inc_coin]枚集める -> ライフが1増える
        if C.course <= 5:
            if C.pl_coin >= C.pll_inc_coin_1:
                C.pl_life += 1
                C.pl_coin -= C.pll_inc_coin_1
        elif 6 <= C.course <= 10:
            if C.pl_coin >= C.pll_inc_coin_2:
                C.pl_life += 1
                C.pl_coin -= C.pll_inc_coin_2
        elif 11 <= C.course <= 15:
            if C.pl_coin >= C.pll_inc_coin_3:
                C.pl_life += 1
                C.pl_coin -= C.pll_inc_coin_3
        elif C.course >= 16:
            if C.pl_coin >= C.pll_inc_coin_4:
                C.pl_life += 1
                C.pl_coin -= C.pll_inc_coin_4
        
    # if C.maze[C.pl_y][C.pl_x] == C.GOAL:
    #     C.maze[C.pl_y][C.pl_x] = C.ROAD

    # プレイヤー：アイテムを拾う
    if C.maze[C.pl_y][C.pl_x] == C.ITEM:
        C.snd_get_item.play()
        C.maze[C.pl_y][C.pl_x] = C.ROAD
        # 取得するアイテムの種類をランダムに選定
        item = random.randint(1, 5)
        C.pl_item[item] += 1

    # エネミー
    for n in range(C.emy_max):
        # エネミーが存在しない場合はとばす
        if C.emy_f[n] == False:
            continue
        
        # エネミー：プレイヤーと衝突
        if C.emy_x[n] == C.pl_x and C.emy_y[n] == C.pl_y:
            # プレイヤー：赤色のパックマンの時 -> エネミーを倒す
            if C.pl_col == C.COLOR_BLUE:
                C.snd_player_attack.play()
                C.emy_f[n] = False
            else:
                # プレイヤーが無敵状態ではない場合
                if C.pl_muteki == 0:
                    C.snd_player_damage.play()
                    # レベルごとに無敵時間を変える
                    if C.course <= 10:
                        C.pl_muteki = C.FPS * 1
                    elif 11 <= C.course <= 20:
                        C.pl_muteki = C.FPS * 2
                    elif 21 <= C.course <= 30:
                         C.pl_muteki = C.FPS * 3
                    C.pl_life -= 1
                    C.emy_f[n] = False
                else:
                    C.emy_f[n] = False

        # エネミー：黄 -> ゴールへ到達
        if C.emy_col[n] == C.COLOR_YELLOW and C.maze[C.emy_y[n]][C.emy_x[n]] == C.GOAL:
            C.maze[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # ゴールをなくす
            C.goal_f = False                      # ゴールがないフラグ
            C.goal_generate_time = C.FPS * 5       # ゴールを再生成するまでの時間

        # エネミー：緑 -> コインへ到達
        if C.emy_col[n] == C.COLOR_GREEN  and C.maze[C.emy_y[n]][C.emy_x[n]] == C.COIN:
            C.maze[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # コインをなくす

        # エネミー：茶 -> アイテムへ到達
        if C.emy_col[n] == C.COLOR_BROWN and C.maze[C.emy_y[n]][C.emy_x[n]] == C.ITEM:
            C.maze[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # アイテムをなくす
