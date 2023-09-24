import pygame
import datetime
from collections import deque


# ******************** 定数／変数 ********************
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
COLOR_ORANGE = 5     # 橙色
# # =============== GAME MANAGE ===============
idx = 0                     # ゲーム画面インデックス
tmr = 0                     # ゲームのタイマー
tmr_all = 0                 # ゲームの総プレイ時間
tmr_pause = 0               # ポーズ画面(idx=2)のタイマー
course = 0                  # コースの回数
course_max = 30             # コースの最大値
point_all = 0               # 総獲得ポイント数
# # =============== BLOCK ===============
EDGE = 1                    # フィールド端の壁
WALL = 0                    # フィールド端以外の壁
ROAD = -1                   # 通路
GOAL = -2                   # ゴール
ITEM = -3                   # アイテム
POINT = -4                  # ポイント
# # =============== TITLE IMG ===============
plt_col = []     # ゲームタイトル画面のプレイヤー画像のカラーインデックス
# # =============== MANUAL IMG ===============
mnl_itm_num = 0     # マニュアル画面のアイテム画像のカラーインデックス
mnl_itm_col = []    # マニュアル画面のアイテム画像のカラーインデックスリスト
# # =============== SCREEN ===============
sc_min = -10
sc_max = 11
sc_x = 10
sc_y = 6
# # =============== FIELD ===============
block_size = 60  # フィールドの１ブロックのサイズ
block_num = 17   # フィールドの１辺のブロック数
field = []       # フィールド管理用配列
# # =============== GOAL ===============
goal_f = False          # ゴールがフィールド上にあるかの判定フラグ
goal_generate_time = 0  # ゴールを生成するまでの時間
# # =============== PLAYER ===============
pl_col = 0             # プレイヤーの色(使用するアイテムで変化)
pl_x = 0               # X座標
pl_y = 0               # Y座標
pl_d = 0               # 移動方向
pl_point = 0           # 獲得ポイント数（コース）
pl_life = 0            # ライフ
pl_item = [0]*6        # 各アイテムの所有数
pl_fov = 0             # 視界制限
pl_muteki = 0          # 無敵時間（秒）
pl_wallbreak = 0       # 壁破壊カウント
pll_inc_point_1 = 50   # ライフを増やすためのポイント数（コース１～５）
pll_inc_point_2 = 60   # ライフを増やすためのポイント数（コース６～１０）
pll_inc_point_3 = 80   # ライフを増やすためのポイント数（コース１０～１５）
pll_inc_point_4 = 100  # ライフを増やすためのポイント数（コース１６～２０）
plm_tmr = 0
# # =============== ITEM ===============
item_use = False        # アイテム使用の判定
item_time = 0           # アイテム使用時間
item_max = 0            # アイテムの最大数
item_generate_time = 0  # アイテムを生成するまでの時間
# # =============== TIME LIMIT (minutes)===============
time_limit_1_10 = datetime.timedelta(minutes = 1)
time_limit_11_20 = datetime.timedelta(minutes = 3)
time_limit_21_25 = datetime.timedelta(minutes = 3)
time_limit_26_29 = datetime.timedelta(minutes = 3)
time_limit_30 = datetime.timedelta(minutes = 1.5)
# # =============== ENEMY ===============
emy_max = 0             # エネミーの最大数
emy_no = 0              # エネミーの配列の添字
emy_num_max = False     # エネミーが最大数いるか
emy_time = 0            # エネミーを生成するまでの時間
emy_f = [False]*emy_max # エネミーが存在するか
emy_col = [0]*emy_max   # エネミーの色(タイプ)
emy_x = [0]*emy_max     # X座標
emy_y = [0]*emy_max     # Y座標
emy_d = [0]*emy_max     # 移動方向
emy_s = [0]*emy_max     # 移動スピード
ENEMY_HIGH_SPEED = 3    # 移動スピードレベル
ENEMY_NORMAL_SPEED = 4  # 移動スピードレベル
ENEMY_LOW_SPEED = 6     # 移動スピードレベル
# # =============== BFS ===============
que = deque()
dist = []

# ******************** ブロック／オブジェクト画像 ********************
img_road = pygame.image.load("image/road.png")
img_wall = pygame.image.load("image/wall.png")
img_fov = [
    pygame.image.load("image/fov_0.png"),
    pygame.image.load("image/fov_1.png")
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
    pygame.image.load("image/enemy_1.png"),
    pygame.image.load("image/enemy_2.png"),
    pygame.image.load("image/enemy_3.png"),
    pygame.image.load("image/enemy_4.png"),
    pygame.image.load("image/enemy_5.png"),
    pygame.image.load("image/enemy_6.png")
]
img_goal = pygame.image.load("image/goal.png")
img_point = pygame.image.load("image/point.png")
img_item = [
    pygame.image.load("image/item_0.png"),
    pygame.image.load("image/item_1.png"),
    pygame.image.load("image/item_2.png"),
    pygame.image.load("image/item_3.png"),
    pygame.image.load("image/item_4.png")
]
img_unknown = pygame.image.load("image/unknown.png")

# ******************** マニュアル ********************
img_manual = pygame.image.load("image/manual.png")
mnl_point = pygame.image.load("image/mnl_point.png")
mnl_goal = pygame.image.load("image/mnl_goal.png")
mnl_item = pygame.image.load("image/mnl_item.png")
mnl_item_annotation = pygame.image.load("image/mnl_item_annotation.png")
mnl_enemy = pygame.image.load("image/mnl_enemy.png")
mnl_enemy_list = [
    pygame.image.load("image/mnl_enemy_01.png"),
    pygame.image.load("image/mnl_enemy_02.png"),
    pygame.image.load("image/mnl_enemy_03.png"),
    pygame.image.load("image/mnl_enemy_04.png"),
    pygame.image.load("image/mnl_enemy_05.png"),
    pygame.image.load("image/mnl_enemy_06.png")
]
mnl_player = pygame.image.load("image/mnl_player.png")
mnl_player_list = [
    pygame.image.load("image/mnl_player_01.png"),
    pygame.image.load("image/mnl_player_02.png"),
    pygame.image.load("image/mnl_player_03.png"),
    pygame.image.load("image/mnl_player_04.png"),
    pygame.image.load("image/mnl_player_05.png")
]
mnl_unknown = pygame.image.load("image/mnl_unknown.png")
img_operation = pygame.image.load("image/operation.png")
mnl_operation = pygame.image.load("image/mnl_operation.png")

# =============== COLOR ===============
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (254, 226, 237)
BLUE = (0, 103, 192)
GREEN = (77, 181, 106)

# # =============== SOUND ===============
se_point = None
se_item = None
se_goal = None
se_attack = None
se_damage = None
se_pl_red = None
se_pl_blue = None
se_pl_green = None
se_pl_yellow = None
se_pl_orange = None
se_break_wall = None
se_enemy = None
se_delete_item = None
se_break_goal = None
se_manual = None
