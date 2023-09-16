import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from . import item as I
from . import config as C


# ******************** 文字の描画 ********************
def draw_text(sc, txt, x, y, siz, col, center):

    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)

    # 中央揃え
    if center == True:
        # 指定文字に合わせて調整
        x = x - sur.get_width()/2
        y = y - sur.get_height()/2
    # 文字の描画
    sc.blit(sur, [x, y])
    

# ******************** 画像の描画 ********************
def draw_img(sc, img, x, y):

    # 中央揃え
    x = x - img.get_width()/2
    y = y - img.get_height()/2
    # 画像の描画
    sc.blit(img, [x, y])


# ******************** 迷路の描画 ********************
def draw_maze(sc):
    
    # プレイヤーを中心に、画面の端から端までの情報を取得し、画面描画する
    sc_min = 10
    sc_max = 11
    sc_y = 6
    for y in range(-sc_min, sc_max):
        for x in range(-sc_min, sc_max):
            X = (x+sc_min) * C.maze_size
            Y = (y+sc_y) * C.maze_size
            # プレイヤーが軸
            mx = C.pl_x + x
            my = C.pl_y + y
            
            # 描画：壁と通路
            if 0 <= mx < C.maze_num and 0 <= my < C.maze_num:
                if C.maze[my][mx] == C.EDGE or C.maze[my][mx] == C.WALL: # 壁
                    sc.blit(C.img_wall, [X, Y])
                if C.maze[my][mx] == C.ROAD: # 通路
                    sc.blit(C.img_road, [X, Y])

                # 描画：ゴール
                if C.maze[my][mx] == C.GOAL:
                    sc.blit(C.img_goal, [X, Y])
                # 描画：コイン
                if C.maze[my][mx] == C.COIN:
                    sc.blit(C.img_coin, [X, Y])
                # 描画：アイテム（負の数のため、math.ceilで小数点以下を切り上げ）
                if math.ceil(C.maze[my][mx]) == C.ITEM:
                    # C.img_itemのリストから描画画像を設定
                    sc.blit(C.img_item[I.get_item_num(C.maze[my][mx])], [X, Y])
                # 描画：エネミー
                for n in range(C.emy_max):
                    if C.emy_f[n] == False:
                        continue
                    if C.emy_x[n] == mx and C.emy_y[n] == my:
                        # エネミーの種類番号＋向き先番号
                        sc.blit(C.img_enemy[C.emy_col[n]*4 + C.emy_d[n]], [X, Y])
            
            # プレイヤーの口の動きの設定(FPSの設定に合わせる)
            if C.tmr%3 == 0:
                C.plm_tmr += 1
                        
            # 描画：プレイヤー
            if x == 0 and y == 0:
                if C.pl_muteki%2 == 0:
                    # C.img_rz = pygame.transform.rotozoom(C.img_player[C.pl_col*2+tmr%2], C.pl_d*(-90), 1.0)
                    img_rz = pygame.transform.rotozoom(C.img_player[C.pl_col*2+C.plm_tmr%2], C.pl_d*(-90), 1.0)
                    # アイテム使用中 + 使用時間切れ間近
                    if C.item_use == True and C.item_time < C.FPS*3:
                        if C.tmr%3 == 0:
                            sc.blit(img_rz, [X, Y])
                    else:
                        sc.blit(img_rz, [X, Y])

                # 緑色のパックマンの効果：矢印
                if C.pl_col == C.COLOR_GREEN and C.goal_f == True:
                    # プレイヤーからゴールの方向(角度)を取得
                    a = calc_angle_of_goal_from_player()
                    # ゴールの方向に矢印を向ける
                    img_rz = pygame.transform.rotozoom(C.img_arrow, -a, 1.0)
                    draw_img(sc, img_rz, X+C.maze_size/2, Y-C.maze_size)

    # 描画：視界エリア
    if 21 <= C.course <= 25:
        if C.pl_scope == 0:
            draw_img(sc, C.img_scope[C.pl_scope+1], C.SCREEN_SIZE/1.2, C.SCREEN_SIZE/2)
    elif C.course >= 26:
        draw_img(sc, C.img_scope[C.pl_scope], C.SCREEN_SIZE/1.2, C.SCREEN_SIZE/2)

    # 枠組み
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 30, 240, 340])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 40, 180, 240])
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 400, 240, 290])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 300, 180, 220])
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 720, 240, 150])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 570, 180, 160])


    # 色別のエネミーの数
    count_enemy_color = [0]*6
    for n in range(C.emy_max):
        if C.emy_f[n] == False:
            continue
        # 色別にカウント
        count_enemy_color[C.emy_col[n]] += 1

    # エネミーの情報
    for i in range(6):
        # 画像の描画
        img_rz = pygame.transform.rotozoom(C.img_enemy[i*4], 0, 0.6)
        # sc.blit(img_rz, [C.SCREEN_SIZE+70, 50+50*i])
        sc.blit(img_rz, [C.SCREEN_SIZE-685, 50+37*i])
        # 文字の描画
        # draw_text(sc, "X   " + str(count_enemy_color[i]), C.SCREEN_SIZE+150, 60+50*i, 35, C.BLACK, False)
        draw_text(sc, "X   " + str(count_enemy_color[i]), C.SCREEN_SIZE-635, 60+37*i, 30, C.BLACK, False)

    # パックマン(効果)の情報
    for i in range(1, 6):
        if C.course >= i*5:
            # 画像の描画
            img_rz = pygame.transform.rotozoom(C.img_player[i*2], -270, 0.7)
            # sc.blit(img_rz, [C.SCREEN_SIZE+110, 370+50*i])
            sc.blit(img_rz, [C.SCREEN_SIZE-665, 263+42*i])
            # 文字の描画
            # draw_text(sc, "[" + str(i) + "]:", C.SCREEN_SIZE+50, 380+50*i, 35, C.BLACK, False)
            draw_text(sc, "[" + str(i) + "]:", C.SCREEN_SIZE-705, 275+42*i, 30, C.BLACK, False)
            # draw_text(sc, "X   " + str(C.pl_item[i]), C.SCREEN_SIZE+180, 380+50*i, 35, C.BLACK, False)
            draw_text(sc, "X  " + str(C.pl_item[i]), C.SCREEN_SIZE-605, 275+42*i, 30, C.BLACK, False)
        else:
            # 画像の描画
            img_uk = pygame.transform.rotozoom(C.img_unknown, 0, 0.5)
            sc.blit(img_uk, [C.SCREEN_SIZE-657, 268+42*i])
            draw_text(sc, "[?]:", C.SCREEN_SIZE-705, 275+42*i, 30, C.BLACK, False)
            draw_text(sc, "X  " + str(C.pl_item[i]), C.SCREEN_SIZE-605, 275+42*i, 30, C.BLACK, False)
    
    # COIN：獲得コイン数 / ライフ増加のための必要コイン数
    if C.course <= 5:
        str_pll_inc_coin = str(C.pll_inc_coin_1)
    elif 6 <= C.course <= 10:
        str_pll_inc_coin = str(C.pll_inc_coin_2)
    elif 11 <= C.course <= 20:
        str_pll_inc_coin = str(C.pll_inc_coin_3)
    elif C.course >= 21:
        str_pll_inc_coin = str(C.pll_inc_coin_4)

    # TIME：１コースでかかっている時間
    tmr_sec = math.floor(C.tmr / C.FPS)
    # C.tmrをhh:mm:ss形式に表示
    tmr_now = datetime.timedelta(seconds=tmr_sec)

    # 各コース（レベル）の制限時間
    if C.course <= 10:
        time_limit = C.time_limit_1_10
    elif 11 <= C.course <= 20:
        time_limit = C.time_limit_11_20
    elif 21 <= C.course <= 25:
        time_limit = C.time_limit_21_25
    elif 26 <= C.course <= 29:
        time_limit = C.time_limit_26_29
    elif C.course >= 30:
        time_limit = C.time_limit_30
    
    if tmr_now >= time_limit - datetime.timedelta(seconds=5):
        wk_color = C.RED
    else:
        wk_color = C.BLACK

    # プレイヤーの情報
    draw_text(sc, "LEVEL :  " + str(C.course), C.SCREEN_SIZE-715, 590, 30, C.BLACK, False)
    draw_text(sc, "TIME   :  ", C.SCREEN_SIZE-715, 625, 30, C.BLACK, False)
    draw_text(sc, str(time_limit - tmr_now)[2:], C.SCREEN_SIZE-630, 625, 30, wk_color, False)
    # draw_text(sc, "LIMIT  :  " + str(time_limit)[2:], C.SCREEN_SIZE-715, 625, 30, C.BLACK, False)
    draw_text(sc, "LIFE    :  " + str(C.pl_life), C.SCREEN_SIZE-715, 660, 30, C.BLACK, False)
    draw_text(sc, "COIN   :  " + str(C.pl_coin) + " / " + str_pll_inc_coin, C.SCREEN_SIZE-715, 695, 30, C.BLACK, False)
    # draw_text(sc, "POINT      :   " + str(point), C.SCREEN_SIZE+40, 850, 35, C.BLACK, False)

    if C.tmr % C.FPS <= 10:
        draw_text(sc, "[ESCAPE] TO MANUAL", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, C.BLACK, True)


# ******************** プレイヤーとゴールの位置の角度を算出(緑パックマンの効果で使用) ********************
def calc_angle_of_goal_from_player():
    # 計算：プレイヤーのx,y座標
    x_pl = C.pl_x * C.maze_size + C.maze_size/2
    y_pl = C.pl_y * C.maze_size + C.maze_size/2

    # 計算：ゴールのx,y座標
    x_goal = 0
    y_goal = 0
    for y in range(C.maze_num):
        for x in range(C.maze_num):
            if C.maze[y][x] == C.GOAL:
                x_goal = x * C.maze_size + C.maze_size/2
                y_goal = y * C.maze_size + C.maze_size/2
                
    # 計算：プレイヤーとゴールのx,y方向の距離
    x_dis = x_goal - x_pl
    y_dis = y_goal - y_pl
    # 角度を計算
    ang = math.degrees(math.atan2(y_dis, x_dis))

    return ang
