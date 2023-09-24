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
from . import item as I
from . import sgs
from . import config as C


# ******************** ゲームの初期化 ********************
def init_game():

    # フィールドの１辺のブロック数
    C.block_num = 17

    # コースの階層
    C.course = 0

    # プレイヤー情報
    C.pl_life = 2
    C.pl_item = [2]*6
    C.pl_point = 0
    C.pl_muteki = 0
    C.pl_wallbreak = 0

    # アイテムの効果を無効
    I.item_disable()
    

# ******************** ゲームの初期配置／設定 ********************
def init_game_place():

    # エネミー
    C.emy_max = C.block_num // 5     # エネミーの最大数（C.block_num：初期は17+1）
    C.emy_num_max = False         # エネミーが最大数いるか(初期時はいない)
    C.emy_time = C.FPS * 20         # エネミーを再生成するまでの時間
    enemy.init_enemy()                # エネミーの初期化

    # アイテム
    C.item_max = C.block_num // 5        # アイテムの最大数
    C.item_generate_time = C.FPS * 20   # アイテムを再生成するまでの時間
    if C.course > 1:
        # アイテムの種類をランダムで決定
        rr_item = random.randrange(len(C.img_item))
        # アイテムを１追加
        C.pl_item[rr_item+1] += 1

    # プレイヤーの配置
    while True:
        C.pl_x = random.randint(1, C.block_num-2)
        C.pl_y = random.randint(1, C.block_num-2)
        if C.field[C.pl_y][C.pl_x] == C.ROAD:
            break

    # エネミーの配置
    for i in range(C.block_num // 10):
        enemy.bring_enemy()

    # ゴールの配置
    sgs.set_object(C.GOAL)
    C.goal_f = True

    # アイテムの配置
    for n in range(C.block_num // 10):
        sgs.set_object(C.ITEM)
        
    # ポイントの配置
    for y in range(C.block_num):
        for x in range(C.block_num):
            if C.field[y][x] == C.ROAD:
                C.field[y][x] = C.POINT


# ******************** ゴールを生成するか判定 -> 生成を行う ********************
def chk_and_gen_goal():
    
    # ゴールがない + ゴールの再生成時間がある
    if C.goal_f == False and C.goal_generate_time > 0:
        C.goal_generate_time -= 1
    # ゴールがない + ゴールの再生成時間が0 -> ゴールの生成
    elif C.goal_f == False and C.goal_generate_time == 0:
        sgs.set_object(C.GOAL)
        C.goal_f = True


# ******************** 各種オブジェクトのヒット判定 ********************
def hit_object():

    # プレイヤー：ポイントを拾う
    if C.field[C.pl_y][C.pl_x] == C.POINT:
        C.se_point.play()
        C.field[C.pl_y][C.pl_x] = C.ROAD
        C.pl_point += 1
        C.point_all += 1
        # ライフ増加判定
        inc_pl_life()

        # 緑プレイヤーの場合 -> ポイントを更に加算する
        if C.pl_col == C.COLOR_GREEN:
            C.pl_point += 1
            C.point_all += 1
            # ライフ増加判定
            inc_pl_life()

    # プレイヤー：アイテムを拾う（負の数のため、math.ceilで小数点以下を切り上げ）
    if math.ceil(C.field[C.pl_y][C.pl_x]) == C.ITEM:
        C.se_item.play()
        # 取得するアイテムの種類を小数点以下の数字から設定
        C.pl_item[I.get_item_num(C.field[C.pl_y][C.pl_x])] += 1
        C.field[C.pl_y][C.pl_x] = C.ROAD

    # エネミー
    for n in range(C.emy_max):
        # エネミーが存在しない場合はとばす
        if C.emy_f[n] == False:
            continue
        
        # エネミー：プレイヤーと衝突
        if C.emy_x[n] == C.pl_x and C.emy_y[n] == C.pl_y:
            # プレイヤー：青プレイヤーの時 -> エネミーを倒す
            if C.pl_col == C.COLOR_BLUE:
                C.se_attack.play()
                C.emy_f[n] = False
            else:
                # プレイヤーが無敵状態ではない場合
                if C.pl_muteki == 0:
                    C.se_damage.play()
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
                    C.se_attack.play()
                    C.emy_f[n] = False

        # ゴールブレイクエネミー
        if C.emy_col[n] == C.COLOR_YELLOW and C.field[C.emy_y[n]][C.emy_x[n]] == C.GOAL:
            C.field[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # ゴールをなくす
            C.goal_f = False                      # ゴールがないフラグ
            C.goal_generate_time = C.FPS * 5       # ゴールを再生成するまでの時間
            C.se_break_goal.play()

        # ポイントバイトエネミー
        if C.emy_col[n] == C.COLOR_GREEN  and C.field[C.emy_y[n]][C.emy_x[n]] == C.POINT:
            C.field[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # ポイントをなくす

        # アイテムデリートエネミー（負の数のため、math.ceilで小数点以下を切り上げ）
        if C.emy_col[n] == C.COLOR_ORANGE and math.ceil(C.field[C.emy_y[n]][C.emy_x[n]]) == C.ITEM:
            C.field[C.emy_y[n]][C.emy_x[n]] = C.ROAD     # アイテムをなくす
            C.se_delete_item.play()


# ******************** ライフ増加判定 -> ライフを増やす********************
def inc_pl_life():
    # ポイントを[pll_inc_point]数集める -> ライフが1増える
    if C.course <= 5:
        if C.pl_point >= C.pll_inc_point_1:
            C.pl_life += 1
            C.pl_point -= C.pll_inc_point_1
    elif 6 <= C.course <= 10:
        if C.pl_point >= C.pll_inc_point_2:
            C.pl_life += 1
            C.pl_point -= C.pll_inc_point_2
    elif 11 <= C.course <= 15:
        if C.pl_point >= C.pll_inc_point_3:
            C.pl_life += 1
            C.pl_point -= C.pll_inc_point_3
    elif C.course >= 16:
        if C.pl_point >= C.pll_inc_point_4:
            C.pl_life += 1
            C.pl_point -= C.pll_inc_point_4
