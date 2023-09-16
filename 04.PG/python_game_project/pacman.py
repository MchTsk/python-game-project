# ******************** ↓タスク↓ ********************
# ・コースクリア時、アイテムを一つ追加
# ・解説画面（ESCAPE）の作成
# ・アイテムの上限を設定

# ・タイトル、使用画像、サウンドを変更
# ・設計書に落とし込む
# ******************** ↑タスク↑ ********************

import pygame
import sys
import random
import math
import logging
import datetime
from collections import deque
from tkinter import messagebox
import logging

from python import draw
from python import maze
from python import player
from python import enemy
from python import item
from python import game
from python import sgs
from python import config as C

# ============================================================
#                          グローバル変数
# ============================================================
# ******************** 画像の読込 ********************
img_road = C.img_road
img_wall = C.img_wall
img_scope = C.img_scope
img_player = C.img_player
img_pl_title = C.img_pl_title
img_enemy = C.img_enemy
img_goal = C.img_goal
img_coin = C.img_coin
img_arrow = C.img_arrow
img_unknown = C.img_unknown
img_manual = C.img_manual

# ******************** COLOR ********************
WHITE = C.WHITE
BLACK = C.BLACK
RED = C.RED
PINK = C.PINK
BLUE = C.BLUE
GREEN = C.GREEN

# ============================================================
#                           MAIN
# ============================================================

# ******************** メインループ ********************
def main():
    
    # pygameモジュールの初期化 ／ タイトル設定
    pygame.init()
    pygame.display.set_caption("PAC-MAN")

    # スクリーンの初期化 ／ クロックオブジェクト作成
    screen = pygame.display.set_mode((C.SCREEN_SIZE+500, C.SCREEN_SIZE))
    clock = pygame.time.Clock()

    # 効果音
    C.snd_pacman_blue = pygame.mixer.Sound("sound/pacman_blue.mp3")
    C.snd_pacman_red = pygame.mixer.Sound("sound/pacman_red.mp3")
    C.snd_pacman_yellow = pygame.mixer.Sound("sound/pacman_yellow.mp3")
    C.snd_pacman_green = pygame.mixer.Sound("sound/pacman_green.mp3")
    C.snd_pacman_brown = pygame.mixer.Sound("sound/pacman_brown.mp3")
    C.snd_player_attack = pygame.mixer.Sound("sound/player_attack.mp3")
    C.snd_player_damage = pygame.mixer.Sound("sound/player_damage.mp3")
    C.snd_break_wall = pygame.mixer.Sound("sound/break_wall.mp3")
    C.snd_arrive_goal = pygame.mixer.Sound("sound/arrive_goal.mp3")
    C.snd_get_coin = pygame.mixer.Sound("sound/get_coin.mp3")
    C.snd_get_item = pygame.mixer.Sound("sound/get_item.mp3")

    while True:

        if C.idx != 2:
            C.tmr = C.tmr + 1
        if C.idx == 1:
            C.tmr_all = C.tmr_all + 1
    
        # プログラムの終了
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # ESCAPEキー押下で終了ポップアップ表示
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if C.idx != 1:
                        ret = messagebox.askokcancel('確認', 'ゲームを終了しますか？')
                        if ret == True:
                            pygame.quit()
                            sys.exit()
                    else:
                        if C.idx == 1:
                            C.idx = 2
                        elif C.idx == 2:
                            C.idx = 1
                # SPACEキー押下でゲーム終了
                # elif event.key == pygame.K_SPACE:
                #     if C.idx == 2:
                #         pygame.quit()
                #         sys.exit()

        # スクリーン ／ キー入力
        screen.fill(PINK)
        key = pygame.key.get_pressed()

        # タイトル
        if C.idx == 0:
            # 音楽をかける
            if C.tmr == 1:
                pygame.mixer.music.load("music/Stellar_Wind-Unicorn_Heads.mp3")
                pygame.mixer.music.play(-1)
            
            screen.fill(PINK)

            # スペースを押下した場合 かつ 0.5秒後(二度押し防止)
            if key[pygame.K_SPACE] == 1 and C.tmr >= (C.FPS/2):
                # 音楽をかける
                pygame.mixer.music.load("music/Zoom_Vibe_Tracks.mp3")
                pygame.mixer.music.play(-1)
                # ゲームの初期化
                game.init_game()
                C.idx = 1
                C.tmr = 0
                C.tmr_all = 0
                C.point = 0
                C.plm_tmr = 0
                C.tmr_pause = 0
            
            # img_playerのインデックスリスト（偶数）を作成
            if C.tmr == 1 or C.tmr % C.FPS == 0:
                img_pl_list = []
                for c in range(len(img_player)):
                    if c % 2 == 0:
                        img_pl_list.append(c) 
                
                # インデックスリストをランダムで取得（重複なし）
                C.plt_col = random.sample(img_pl_list, 6)

            # プレイヤーの口の動きの設定(FPSの設定に合わせる)
            if C.tmr%3 == 0:
                C.plm_tmr += 1

            # タイトル画面にタイトルを描画
            draw.draw_text(screen, "PAC-MAN", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/3, 150, BLACK, True)

            # タイトル画面にパックマンを描画
            for plc in range(len(C.plt_col)):
                if C.plt_col[plc] % 2 == 1:
                    plt_num = C.plt_col[plc] - 1
                else:
                    plt_num = C.plt_col[plc]
                img_plt = pygame.transform.rotozoom(img_player[plt_num+C.plm_tmr%2], -270, 1.7)
                screen.blit(img_plt, [C.SCREEN_SIZE-440+100*plc, 360])
            
            # タイトル画面にキー案内を描画
            if C.tmr % C.FPS <= 10:
                draw.draw_text(screen, "[ESCAPE] TO END", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, RED, True)
                draw.draw_text(screen, "PUSH  [ SPACE ]  TO  START", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/1.2, 60, BLACK, True)

        # ゲームプレイ
        elif C.idx == 1:

            # 迷路を生成、初期設定
            if C.tmr == 1:
                C.course += 1
                # レベル30クリアでゲーム終了
                if C.course > 30:
                    C.idx = 3
                    C.tmr = 0
                    continue
                maze.make_maze()
                game.init_game_place()
                
            # プレイ中
            else:
                player.move_player(key)    # プレイヤーの動き
                if C.pl_col != C.COLOR_BROWN:
                    enemy.move_enemy()        # エネミーの動き（スタン中の場合以外）
                item.use_item(key)       # アイテムの使用
                game.hit_check()         # ヒットチェック

                enemy.chk_and_gen_enemy()   # 生成判定（エネミー） ⇒ 生成
                game.chk_and_gen_goal()    # 生成判定（ゴール） ⇒ 生成
                item.chk_and_gen_item()    # 生成判定（アイテム） ⇒ 生成

                # アイテムを使用中の場合
                if C.item_use == True:
                    C.item_time -= 1
                    # アイテムの使用時間が切れた場合
                    if C.item_time == 0:
                        item.item_effect_off()

                # プレイヤーが無敵状態の場合
                if C.pl_muteki > 0:
                    C.pl_muteki -= 1

                # ライフが0になるとゲームオーバー
                if C.pl_life <= 0:
                    C.idx = 4
                    C.tmr = 0
                
                # 制限時間に達するとゲームオーバー
                tmr_sec = math.floor(C.tmr / C.FPS)
                tmr_now = datetime.timedelta(seconds = tmr_sec)
                if C.course <= 10 and tmr_now >= C.time_limit_1_10:
                    C.idx = 4
                    C.tmr = 0
                elif 11 <= C.course <= 20 and tmr_now >= C.time_limit_11_20:
                    C.idx = 4
                    C.tmr = 0
                elif 21 <= C.course <= 25 and tmr_now >= C.time_limit_21_25:
                    C.idx = 4
                    C.tmr = 0
                elif 26 <= C.course <= 29 and tmr_now >= C.time_limit_26_29:
                    C.idx = 4
                    C.tmr = 0
                elif C.course >= 30 and tmr_now >= C.time_limit_30:
                    C.idx = 4
                    C.tmr = 0

                # ゴールすると次のコースへ
                if C.maze[C.pl_y][C.pl_x] == C.GOAL:
                    C.snd_arrive_goal.play()
                    C.tmr = 0
        
        # pause画面
        elif C.idx == 2:
            C.tmr_pause += 1

            # マニュアル表示
            screen.blit(img_manual, [C.SCREEN_SIZE-700, 40])

            # pause画面にキー案内を描画
            if C.tmr_pause % C.FPS <= 10:
                draw.draw_text(screen, "[ESCAPE] TO END", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, RED, True)
                draw.draw_text(screen, "PUSH  [ SPACE ]  TO  RETURN", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/1.04, 50, BLACK, True)
            
            # スペースを押下した場合 => ゲーム画面へ
            if key[pygame.K_SPACE] == 1:
                C.idx = 1
        
        # 全コースクリア
        elif C.idx == 3:
            tmr_sec = math.floor(C.tmr_all / C.FPS)
            tmr_clear = datetime.timedelta(seconds = tmr_sec)
            draw.draw_text(screen, "GAME  CLEAR!!!", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/4, 100, BLACK, True)
            draw.draw_text(screen, "CLEAR TIME  : ", (C.SCREEN_SIZE-285), C.SCREEN_SIZE/2, 100, BLACK, True)
            draw.draw_text(screen, str(tmr_clear), (C.SCREEN_SIZE+130), C.SCREEN_SIZE/2, 100, GREEN, True)
            draw.draw_text(screen, "COIN POINT   : ", (C.SCREEN_SIZE-280), C.SCREEN_SIZE/1.5, 100, BLACK, True)
            draw.draw_text(screen, str(C.point), (C.SCREEN_SIZE+120), C.SCREEN_SIZE/1.5, 100, GREEN, True)

            if C.tmr % C.FPS <= 10:
                draw.draw_text(screen, "[ESCAPE] TO END", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, RED, True)
                draw.draw_text(screen, "PUSH  [ SPACE ]  TO  TITLE", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/1.2, 60, BLACK, True)

            # スペースを押下した場合 かつ 0.5秒後(二度押し防止) => タイトルへ
            if key[pygame.K_SPACE] == 1 and C.tmr >= (C.FPS/2):
                C.idx = 0
                C.tmr = 0
        
        # ゲームオーバー
        elif C.idx == 4:
            draw.draw_text(screen, "GAME  OVER", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/2, 100, RED, True)
            if C.tmr % C.FPS <= 10:
                draw.draw_text(screen, "[ESCAPE] TO END", (C.SCREEN_SIZE+500)/15, C.SCREEN_SIZE/35, 20, RED, True)
                draw.draw_text(screen, "PUSH  [ SPACE ]  TO  TITLE", (C.SCREEN_SIZE+500)/2, C.SCREEN_SIZE/1.2, 60, BLACK, True)
            
            # スペースを押下した場合 => タイトルへ
            if key[pygame.K_SPACE] == 1:
                C.idx = 0
                C.tmr = 0

        # 描画：迷路
        if C.idx == 1 and C.tmr > 0:
            draw.draw_maze(screen)
            
        pygame.display.update()
        clock.tick(C.FPS)


# ******************** ログファイル設定 ********************
def get_logger(logger_name, log_file, f_fmt='%(asctime)-15s %(message)s'):
	# ロガー作成
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG)

	# ファイルハンドラ作成
	file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(logging.Formatter(f_fmt))

	# ロガーに追加
	logger.addHandler(file_handler)

	return logger


# ============================================================
#                         MAIN呼び出し
# ============================================================
if __name__ == '__main__':
    lg = get_logger(__name__, 'log.txt')

    try:
        main()
    except:
	    lg.exception(sys.exc_info()) #エラーをlog.txtに書き込む
