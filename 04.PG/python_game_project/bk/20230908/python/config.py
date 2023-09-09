import pygame
import datetime
from collections import deque


# ******************** 定数／変数 ********************
# =============== COLOR ===============
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (254, 226, 237)
# # =============== SOUND ===============
snd_pacman_blue = None
snd_pacman_red = None
snd_pacman_yellow = None
snd_pacman_green = None
snd_pacman_brown = None
snd_player_attack = None
snd_player_damage = None
snd_break_wall = None
snd_arrive_goal = None
snd_get_coin = None
snd_get_item = None
# # =============== SIZE / FPS ===============
SCREEN_SIZE = 750   # スクリーンサイズ
FPS = 20        # フレームレート
# # =============== DIRECTION ===============
DIR_UP = 0      # 上方向
DIR_RIGHT = 1   # 右方向
DIR_DOWN = 2    # 下方向
DIR_LEFT = 3    # 左方向
# # =============== COLOR ===============
COLOR_BLACK = 0     # 黒色
COLOR_RED = 1       # 赤色
COLOR_BLUE = 2      # 青色
COLOR_GREEN = 3     # 緑色
COLOR_YELLOW = 4    # 黄色
COLOR_BROWN = 5     # 茶色
# # =============== GAME MANAGE ===============
idx = 0     # ゲーム進行のインデックス
tmr = 0     # ゲームのタイマー
tmr_all = 0 # ゲームの総プレイ時間
course = 0  # コースの回数
point = 0   # 総獲得コイン数
EDGE = 1    # フィールド端の壁
WALL = 0    # フィールド端以外の壁
ROAD = -1   # 通路
GOAL = -2   # ゴール
ITEM = -3   # アイテム
COIN = -4   # コイン
# # =============== TITLE IMG ===============
plt_col = []     # ゲームタイトル画面のプレイヤー画像のカラーインデックス
# # =============== PLAYER ===============
pl_col = 0            # パックマンの色(使用するアイテムで変化)
pl_x = 0              # x座標
pl_y = 0              # y座標
pl_d = 0              # 移動方向
pl_fast = False       # 移動スピードが早い
pl_coin = 0           # 拾ったコインの数
pl_life = 0           # 残機(100コインごとに1増える)
pl_item = [0]*6       # 各アイテムの所有数
pl_scope = 0          # 視界の広さ
pl_muteki = 0         # 無敵時間（秒）
pl_wallbreak = 0      # 壁破壊カウント
pll_inc_coin_1 = 50   # ライフを増やすためのコイン枚数（コース１～５）
pll_inc_coin_2 = 60   # ライフを増やすためのコイン枚数（コース６～１０）
pll_inc_coin_3 = 80  # ライフを増やすためのコイン枚数（コース１０～１５）
pll_inc_coin_4 = 100  # ライフを増やすためのコイン枚数（コース１６～２０）
plm_tmr = 0
# # =============== ENEMY ===============
emy_max = 0             # エネミーの最大数
emy_no = 0              # エネミーの配列の添字
emy_num_max = False     # エネミーが最大数いるか
emy_time = 0            # エネミーを生成するまでの時間
emy_f = [False]*emy_max # エネミーが存在するか
emy_col = [0]*emy_max   # エネミーの色(タイプ)
emy_x = [0]*emy_max     # x座標
emy_y = [0]*emy_max     # y座標
emy_d = [0]*emy_max     # 移動方向
emy_s = [0]*emy_max     # 移動スピード
ENEMY_HIGH_SPEED = 3    # 移動スピード：早い
ENEMY_NORMAL_SPEED = 4  # 移動スピード：普通
ENEMY_LOW_SPEED = 6     # 移動スピード：遅い
# # =============== ITEM ===============
item_use = False        # 使用中の有無
item_time = 0           # 使用時間
item_max = 0            # アイテムの最大数
item_generate_time = 0  # アイテムを生成するまでの時間
# # =============== TIME LIMIT (minutes)===============
time_limit_1_10 = datetime.timedelta(minutes = 1)
time_limit_11_20 = datetime.timedelta(minutes = 3)
time_limit_21_25 = datetime.timedelta(minutes = 3)
time_limit_26_29 = datetime.timedelta(minutes = 3)
time_limit_30 = datetime.timedelta(minutes = 1.5)
# # =============== MAZE ===============
goal_f = False          # ゴールが迷路上にあるか
goal_generate_time = 0  # ゴールを生成するまでの時間
# # =============== MAZE ===============
maze_size = 60  # 迷路の1ブロックのサイズ
maze_num = 17   # 迷路のブロック数
maze = []       # 迷路を管理
# # =============== BFS ===============
que = deque()
dist = []

# ******************** 画像の読込 ********************
img_road = pygame.image.load("image/road.png")
img_wall = pygame.image.load("image/wall.png")
img_scope = [
    pygame.image.load("image/scope_0.png"),
    pygame.image.load("image/scope_1.png")
]
img_player = [
    pygame.image.load("image/player_0.png"),
    pygame.image.load("image/player_1.png"),
    pygame.image.load("image/player_2.png"),
    pygame.image.load("image/player_3.png"),
    pygame.image.load("image/player_4.png"),
    pygame.image.load("image/player_5.png"),
    pygame.image.load("image/player_6.png"),
    pygame.image.load("image/player_7.png"),
    pygame.image.load("image/player_8.png"),
    pygame.image.load("image/player_9.png"),
    pygame.image.load("image/player_10.png"),
    pygame.image.load("image/player_11.png")
]
img_pl_title = [
    pygame.image.load("image/player_0.png"),
    pygame.image.load("image/player_2.png"),
    pygame.image.load("image/player_4.png"),
    pygame.image.load("image/player_6.png"),
    pygame.image.load("image/player_8.png"),
    pygame.image.load("image/player_10.png")
]
img_enemy = [
    pygame.image.load("image/enemy_0.png"),
    pygame.image.load("image/enemy_1.png"),
    pygame.image.load("image/enemy_2.png"),
    pygame.image.load("image/enemy_3.png"),
    pygame.image.load("image/enemy_4.png"),
    pygame.image.load("image/enemy_5.png"),
    pygame.image.load("image/enemy_6.png"),
    pygame.image.load("image/enemy_7.png"),
    pygame.image.load("image/enemy_8.png"),
    pygame.image.load("image/enemy_9.png"),
    pygame.image.load("image/enemy_10.png"),
    pygame.image.load("image/enemy_11.png"),
    pygame.image.load("image/enemy_12.png"),
    pygame.image.load("image/enemy_13.png"),
    pygame.image.load("image/enemy_14.png"),
    pygame.image.load("image/enemy_15.png"),
    pygame.image.load("image/enemy_16.png"),
    pygame.image.load("image/enemy_17.png"),
    pygame.image.load("image/enemy_18.png"),
    pygame.image.load("image/enemy_19.png"),
    pygame.image.load("image/enemy_20.png"),
    pygame.image.load("image/enemy_21.png"),
    pygame.image.load("image/enemy_22.png"),
    pygame.image.load("image/enemy_23.png")
]
img_goal = pygame.image.load("image/goal.png")
img_coin = pygame.image.load("image/coin.png")
img_item = pygame.image.load("image/item.png")
img_arrow = pygame.image.load("image/arrow.png")
img_unknown = pygame.image.load("image/unknown.png")
