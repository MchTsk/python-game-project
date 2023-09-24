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


# ******************** フィールドの描画 ********************
def draw_field(sc):
    
    # プレイヤーを中心に、画面の端から端までの情報を取得し、画面描画する
    for y in range(C.sc_min, C.sc_max):
        for x in range(C.sc_min, C.sc_max):
            X = (x + C.sc_x) * C.block_size
            Y = (y + C.sc_y) * C.block_size
            # プレイヤーが軸
            mx = C.pl_x + x
            my = C.pl_y + y
            
            if 0 <= mx < C.block_num and 0 <= my < C.block_num:
                # 壁
                if C.field[my][mx] == C.EDGE or C.field[my][mx] == C.WALL:
                    sc.blit(C.img_wall, [X, Y])
                 # 通路
                if C.field[my][mx] == C.ROAD:
                    sc.blit(C.img_road, [X, Y])

                # ゴール
                if C.field[my][mx] == C.GOAL:
                    sc.blit(C.img_goal, [X, Y])
                # ポイント
                if C.field[my][mx] == C.POINT:
                    sc.blit(C.img_point, [X, Y])
                # アイテム（負の数のため、math.ceilで小数点以下を切り上げ）
                if math.ceil(C.field[my][mx]) == C.ITEM:
                    # C.img_itemのリストから描画画像を設定
                    sc.blit(C.img_item[I.get_item_num(C.field[my][mx]) - 1], [X, Y])
                # エネミー
                for n in range(C.emy_max):
                    if C.emy_f[n] == False:
                        continue
                    if C.emy_x[n] == mx and C.emy_y[n] == my:
                        # エネミーの種類番号
                        sc.blit(C.img_enemy[C.emy_col[n]], [X, Y])
            
            # プレイヤーの口の動きの設定(FPSの設定に合わせる)
            if C.tmr%3 == 0:
                C.plm_tmr += 1
                        
            # プレイヤー
            if x == 0 and y == 0:
                if C.pl_muteki%2 == 0:
                    img_rz = pygame.transform.rotozoom(C.img_player[C.pl_col*2+C.plm_tmr%2], C.pl_d*(-90), 1.0)
                    # アイテム使用中 + 使用時間切れ間近
                    if C.item_use == True and C.item_time < C.FPS*3:
                        if C.tmr%3 == 0:
                            sc.blit(img_rz, [X, Y])
                    else:
                        sc.blit(img_rz, [X, Y])

    # 視界制限
    if 21 <= C.course <= 25:
        if C.pl_fov == 0:
            draw_img(sc, C.img_fov[C.pl_fov+1], C.SCREEN_SIZE/1.2, C.SCREEN_SIZE/2)
    elif C.course >= 26:
        draw_img(sc, C.img_fov[C.pl_fov], C.SCREEN_SIZE/1.2, C.SCREEN_SIZE/2)

    # 枠組み
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 40, 180, 240])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 300, 180, 220])
    pygame.draw.rect(sc, C.WHITE, [C.SCREEN_SIZE-725, 570, 180, 160])


    # 色別のエネミーの数
    count_enemy_color = [0]*6
    for n in range(C.emy_max):
        if C.emy_f[n] == False:
            continue
        # 色別にカウント
        count_enemy_color[C.emy_col[n]] += 1

    # エネミーの情報
    for i in range(len(C.img_enemy)):
        # 画像の描画
        img_rz = pygame.transform.rotozoom(C.img_enemy[i], 0, 0.6)
        sc.blit(img_rz, [C.SCREEN_SIZE-685, 50+37*i])
        # 文字の描画
        draw_text(sc, "X   " + str(count_enemy_color[i]), C.SCREEN_SIZE-635, 60+37*i, 30, C.BLACK, False)

    # 所持アイテムの情報
    for i in range(1, 6):
        if C.course > i*5:
            # 画像の描画
            img_rz = pygame.transform.rotozoom(C.img_player[i*2], -270, 0.7)
            sc.blit(img_rz, [C.SCREEN_SIZE-663, 263+42*i])
            # 文字の描画
            draw_text(sc, "[" + str(i) + "]:", C.SCREEN_SIZE-705, 275+42*i, 30, C.BLACK, False)
            draw_text(sc, "X  " + str(C.pl_item[i]), C.SCREEN_SIZE-605, 275+42*i, 30, C.BLACK, False)
        else:
            # 画像の描画
            img_uk = pygame.transform.rotozoom(C.img_unknown, 0, 0.5)
            sc.blit(img_uk, [C.SCREEN_SIZE-657, 268+42*i])
            draw_text(sc, "[?]:", C.SCREEN_SIZE-705, 275+42*i, 30, C.BLACK, False)
            draw_text(sc, "X  " + str(C.pl_item[i]), C.SCREEN_SIZE-605, 275+42*i, 30, C.BLACK, False)
    
    # COIN：獲得ポイント数 / ライフ増加のための必要ポイント数
    if C.course <= 5:
        str_pll_inc_point = str(C.pll_inc_point_1)
    elif 6 <= C.course <= 10:
        str_pll_inc_point = str(C.pll_inc_point_2)
    elif 11 <= C.course <= 20:
        str_pll_inc_point = str(C.pll_inc_point_3)
    elif C.course >= 21:
        str_pll_inc_point = str(C.pll_inc_point_4)

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

    # ゲームの情報
    draw_text(sc, "LEVEL :  " + str(C.course) + " / " + str(C.course_max), C.SCREEN_SIZE-715, 590, 30, C.BLACK, False)
    draw_text(sc, "TIME   :  ", C.SCREEN_SIZE-715, 625, 30, C.BLACK, False)
    draw_text(sc, str(time_limit - tmr_now)[2:], C.SCREEN_SIZE-630, 625, 30, wk_color, False)
    draw_text(sc, "LIFE    :  " + str(C.pl_life), C.SCREEN_SIZE-715, 660, 30, C.BLACK, False)
    draw_text(sc, "POINT :  " + str(C.pl_point) + " / " + str_pll_inc_point, C.SCREEN_SIZE-715, 695, 30, C.BLACK, False)

    if C.tmr % C.FPS <= 10:
        draw_text(sc, "[ESCAPE] TO MANUAL", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, C.BLACK, True)

