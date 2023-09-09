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
    # test
    a = 10
    b = 11
    for y in range(-a, b):
        for x in range(-a, b):
            X = (x+a) * C.maze_size
            Y = (y+a) * C.maze_size
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
                # 描画：アイテム
                if C.maze[my][mx] == C.ITEM:
                    sc.blit(C.img_item, [X, Y])
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
            draw_img(sc, C.img_scope[C.pl_scope+1], C.SCREEN_SIZE/2, C.SCREEN_SIZE/2)
    elif C.course >= 26:
        draw_img(sc, C.img_scope[C.pl_scope], C.SCREEN_SIZE/2, C.SCREEN_SIZE/2)

    # 枠組み
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 30, 240, 340])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+270, 20, 200, 230])
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 400, 240, 290])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+270, 270, 200, 230])
    # pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+30, 720, 240, 150])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE+270, 520, 200, 210])


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
        img_rz = pygame.transform.rotozoom(C.img_enemy[i*4], 0, 0.8)
        # sc.blit(img_rz, [C.SCREEN_SIZE+70, 50+50*i])
        sc.blit(img_rz, [C.SCREEN_SIZE+320, 35+50*i])
        # 文字の描画
        # draw_text(sc, "X   " + str(count_enemy_color[i]), C.SCREEN_SIZE+150, 60+50*i, 35, C.BLACK, False)
        draw_text(sc, "X   " + str(count_enemy_color[i]), C.SCREEN_SIZE+350, 45+50*i, 35, C.BLACK, False)

    # パックマン(効果)の情報
    for i in range(1, 6):
        if C.course >= i*5:
            # 画像の描画
            img_rz = pygame.transform.rotozoom(C.img_player[i*2], -90, 0.8)
            # sc.blit(img_rz, [C.SCREEN_SIZE+110, 370+50*i])
            sc.blit(img_rz, [C.SCREEN_SIZE+110, 325+50*i])
            # 文字の描画
            # draw_text(sc, "[" + str(i) + "]:", C.SCREEN_SIZE+50, 380+50*i, 35, C.BLACK, False)
            draw_text(sc, "[" + str(i) + "]:", C.SCREEN_SIZE+50, 335+50*i, 35, C.BLACK, False)
            # draw_text(sc, "X   " + str(C.pl_item[i]), C.SCREEN_SIZE+180, 380+50*i, 35, C.BLACK, False)
            draw_text(sc, "X   " + str(C.pl_item[i]), C.SCREEN_SIZE+180, 335+50*i, 35, C.BLACK, False)
        else:
            # 画像の描画
            img_uk = pygame.transform.rotozoom(C.img_unknown, 0, 0.6)
            sc.blit(img_uk, [C.SCREEN_SIZE+115, 328+50*i])
            draw_text(sc, "[?]:", C.SCREEN_SIZE+50, 335+50*i, 35, C.BLACK, False)
            draw_text(sc, "X   " + str(C.pl_item[i]), C.SCREEN_SIZE+180, 335+50*i, 35, C.BLACK, False)
    
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
    # hh:mm:ssのmm:ss部分のみ表示
    str_tmr = str(datetime.timedelta(seconds=tmr_sec))[2:]

    # 各コース（レベル）の制限時間
    if C.course <= 10:
        str_time_limit = str(C.time_limit_1_10)[2:]
    elif 11 <= C.course <= 20:
        str_time_limit = str(C.time_limit_11_20)[2:]
    elif 21 <= C.course <= 25:
        str_time_limit = str(C.time_limit_21_25)[2:]
    elif 26 <= C.course <= 29:
        str_time_limit = str(C.time_limit_26_29)[2:]
    elif C.course >= 30:
        str_time_limit = str(C.time_limit_30)[2:]

    # プレイヤーの情報
    draw_text(sc, "LEVEL    :   " + str(C.course), C.SCREEN_SIZE+40, 680, 35, C.BLACK, False)
    draw_text(sc, "TIME       :   " + str_tmr, C.SCREEN_SIZE+40, 715, 35, C.BLACK, False)
    draw_text(sc, "LIMIT      :   " + str_time_limit, C.SCREEN_SIZE+40, 750, 35, C.BLACK, False)
    draw_text(sc, "LIFE        :   " + str(C.pl_life), C.SCREEN_SIZE+40, 785, 35, C.BLACK, False)
    draw_text(sc, "COIN       :   " + str(C.pl_coin) + " / " + str_pll_inc_coin, C.SCREEN_SIZE+40, 820, 35, C.BLACK, False)
    # draw_text(sc, "POINT      :   " + str(point), C.SCREEN_SIZE+40, 850, 35, C.BLACK, False)


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
