import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import bfs
from . import sgs
from . import config as C


# ******************** エネミーの初期化 ********************
def init_enemy():
    
    C.emy_f = [False]*C.emy_max
    C.emy_col = [0]*C.emy_max
    C.emy_x = [0]*C.emy_max
    C.emy_y = [0]*C.emy_max
    C.emy_d = [0]*C.emy_max
    C.emy_s = [0]*C.emy_max
        

# ******************** エネミーを出す ********************
def bring_enemy():

    # エネミーの配置：ランダム選択
    while True:
        emy_x = random.randint(1, C.block_num-2)
        emy_y = random.randint(1, C.block_num-2)
        # 位置が通路(ポイントを含む)の場合 -> ok
        if C.field[emy_y][emy_x] == C.ROAD or C.field[emy_y][emy_x] == C.POINT:
            # プレイヤーと離れている -> ok
            if (emy_x < C.pl_x-5 or C.pl_x+5 < emy_x) and (emy_y < C.pl_y-5 or C.pl_y+5 < emy_y):
                break

    # エネミーの色：ランダム選択
    emy_col = random.randint(C.COLOR_BLACK, C.COLOR_ORANGE)

    # エネミーの移動スピード(色で判別)
    if emy_col == C.COLOR_BLACK:      # 黒
        emy_s = C.ENEMY_HIGH_SPEED
    elif emy_col == C.COLOR_RED:      # 赤
        emy_s = C.ENEMY_NORMAL_SPEED
    else:                           # 青、黄、緑、橙
        emy_s = C.ENEMY_LOW_SPEED

    # エネミーを配置
    set_enemy(emy_x, emy_y, emy_s, emy_col)


# ******************** エネミーをセット ********************
def set_enemy(x, y, s, col):

    while True:
        # messagebox.askokcancel('test', C.emy_no)
        if C.emy_f[C.emy_no] == False:
            C.emy_f[C.emy_no] = True
            C.emy_col[C.emy_no] = col
            C.emy_x[C.emy_no] = x
            C.emy_y[C.emy_no] = y
            C.emy_s[C.emy_no] = s
            break
        C.emy_no = (C.emy_no+1) % C.emy_max


# ******************** エネミーの移動 ********************
def move_enemy():

    for n in range(C.emy_max):
        # エネミーが存在しない(要素の)場合はとばす
        if C.emy_f[n] == False:
            continue

        # エネミーの移動スピード
        if C.tmr%C.emy_s[n] != 0:
            continue
        
        emy_dir = -1

        # エネミーの色：黒 -> 移動方向：プレイヤーのいる方向 or ランダム
        if C.emy_col[n] == C.COLOR_BLACK:
            # 移動方向：プレイヤーの方向
            if C.emy_y[n] > C.pl_y:
                emy_dir = C.DIR_UP    # 上方向
            if C.emy_y[n] < C.pl_y:
                emy_dir = C.DIR_DOWN  # 下方向
            if C.emy_x[n] < C.pl_x:
                emy_dir = C.DIR_RIGHT # 右方向
            if C.emy_x[n] > C.pl_x:
                emy_dir = C.DIR_LEFT  # 左方向

            if emy_dir == -1:
                emy_dir = random.randint(C.DIR_UP, C.DIR_LEFT)  # 移動方向：ランダム選択

            # 移動できたかどうか -> 移動可能ならば移動(Trueを返す)
            move_ok = move_check_to_move(emy_dir, n)

            # 移動できていない場合 -> ランダム
            if move_ok == False:
                while True:
                    emy_dir = random.randint(C.DIR_UP, C.DIR_LEFT)  # 移動方向：ランダム選択
                    move_ok = move_check_to_move(emy_dir, n)    # 移動できたかどうか -> 移動可能ならば移動(Trueを返す)

                    # 移動できるまで繰り返す
                    if move_ok == True:
                        break

        # エネミーの色：青、赤、黄、緑、橙 -> 移動方向：目標へ移動(追尾)
        else:
            # 青、赤：プレイヤーを追尾
            if C.emy_col[n] == C.COLOR_BLUE or C.emy_col[n] == C.COLOR_RED:
                bfs.BFS(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)                         # 幅優先探索法でプレイヤーの位置までの最短ルートを算出
                next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)   # 幅優先探索法で求めたルートから次の移動方向を取得
                
            # 黄：ゴールへ移動 or プレイヤーを追尾
            elif C.emy_col[n] == C.COLOR_YELLOW:
                # ゴールが存在する：ゴールへ移動
                if sgs.search_object(C.GOAL) == True:
                    goal_x, goal_y = sgs.get_object_xy(C.GOAL)                              # ゴールのx,y座標を取得
                    bfs.BFS(C.emy_x[n], C.emy_y[n], goal_x, goal_y)                         # 幅優先探索法でゴールの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], goal_x, goal_y)   # 幅優先探索法で求めたルートから次の移動方向を取得
                # ゴールが存在しない：プレイヤーを追尾
                else:
                    bfs.BFS(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)                         # 幅優先探索法でプレイヤーの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)   # 幅優先探索法で求めたルートから次の移動方向を取得

            # 緑：ポイントへ移動 or プレイヤーを追尾（フィールド上の全ポイントがなくなり次第追従）
            elif C.emy_col[n] == C.COLOR_GREEN:
                # ポイントが存在する：ポイントへ移動
                if sgs.search_object(C.POINT) == True:
                    point_x, point_y = sgs.get_object_xy(C.POINT)                             # ポイントのx,y座標を取得
                    bfs.BFS(C.emy_x[n], C.emy_y[n], point_x, point_y)                         # 幅優先探索法でポイントの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], point_x, point_y)   # 幅優先探索法で求めたルートから次の移動方向を取得
                # ポイントが存在しない：プレイヤーを追尾
                else:
                    bfs.BFS(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)                         # 幅優先探索法でプレイヤーの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)   # 幅優先探索法で求めたルートから次の移動方向を取得
            
            # 橙：アイテムへ移動 or プレイヤーを追尾
            elif C.emy_col[n] == C.COLOR_ORANGE:
                # アイテムが存在する：アイテムへ移動
                if sgs.search_object(C.ITEM) == True:
                    item_x, item_y = sgs.get_object_xy(C.ITEM)                              # アイテムのx,y座標を取得
                    bfs.BFS(C.emy_x[n], C.emy_y[n], item_x, item_y)                         # 幅優先探索法でアイテムの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], item_x, item_y)   # 幅優先探索法で求めたルートから次の移動方向を取得
                # アイテムが存在しない：プレイヤーを追尾
                else:
                    bfs.BFS(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)                         # 幅優先探索法でプレイヤーの位置までの最短ルートを算出
                    next_dir = bfs.next_direction(C.emy_x[n], C.emy_y[n], C.pl_x, C.pl_y)   # 幅優先探索法で求めたルートから次の移動方向を取得

            # 移動
            if next_dir == C.DIR_UP:      # 上方向
                C.emy_y[n] -= 1
                C.emy_d[n] = C.DIR_UP
            elif next_dir == C.DIR_RIGHT: # 右方向
                C.emy_x[n] += 1
                C.emy_d[n] = C.DIR_RIGHT
            elif next_dir == C.DIR_DOWN:  # 下方向
                C.emy_y[n] += 1
                C.emy_d[n] = C.DIR_DOWN
            elif next_dir == C.DIR_LEFT:  # 左方向
                C.emy_x[n] -= 1
                C.emy_d[n] = C.DIR_LEFT
        
    
# ******************** 取得した移動方向に移動可能か確認 -> 可能ならば移動(True) ********************
def move_check_to_move(emy_dir, no):

    # 移動可能か確認 -> 移動
    move_ok = False
    
    # 上方向に移動 + 移動可否の確認
    if emy_dir == C.DIR_UP and (C.field[C.emy_y[no]-1][C.emy_x[no]] != C.WALL and C.field[C.emy_y[no]-1][C.emy_x[no]] != C.EDGE):
        C.emy_d[no] = C.DIR_UP
        C.emy_y[no] -= 1
        move_ok = True
    # 右方向に移動 + 移動可否の確認
    if emy_dir == C.DIR_RIGHT and (C.field[C.emy_y[no]][C.emy_x[no]+1] != C.WALL and C.field[C.emy_y[no]][C.emy_x[no]+1] != C.EDGE):
        C.emy_d[no] = C.DIR_RIGHT
        C.emy_x[no] += 1
        move_ok = True
    # 下方向に移動 + 移動可否の確認
    if emy_dir == C.DIR_DOWN and (C.field[C.emy_y[no]+1][C.emy_x[no]] != C.WALL and C.field[C.emy_y[no]+1][C.emy_x[no]] != C.EDGE):
        C.emy_d[no] = C.DIR_DOWN
        C.emy_y[no] += 1
        move_ok = True
    # 左方向に移動 + 移動可否の確認
    if emy_dir == C.DIR_LEFT and (C.field[C.emy_y[no]][C.emy_x[no]-1] != C.WALL and C.field[C.emy_y[no]][C.emy_x[no]-1] != C.EDGE):
        C.emy_d[no] = C.DIR_LEFT
        C.emy_x[no] -= 1
        move_ok = True

    return move_ok


# ******************** ゲーム上にエネミーが最大数いるか調べる ********************
def enemy_num_max_check():

    # エネミーの最大数分を繰り返す
    for n in range(C.emy_max):
        # エネミーが最大数分いない場合
        if C.emy_f[n] == False:
            C.emy_num_max = False
            C.emy_time = C.FPS * 20
            break

# ******************** エネミーを生成するか判定 -> 生成を行う ********************
def chk_and_gen_enemy():
    
    # エネミーの最大数いる -> 最大数いるか判定
    if C.emy_num_max == True:
        enemy_num_max_check()
    # エネミーが最大数いない + エネミーの再生成時間が0より大きい
    elif C.emy_num_max == False and C.emy_time > 0:
        C.emy_time -= 1
    # エネミーが最大数いない + エネミーの際生成時間が0 -> エネミーを生成
    elif C.emy_num_max == False and C.emy_time == 0:
        bring_enemy()
        C.emy_num_max = True
        C.se_enemy.play()
