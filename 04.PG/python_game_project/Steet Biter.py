# ******************** ↓タスク↓ ********************
# ・インストール方法作成
# ・設計書反映（NR）
# ・ソースコメント、変数整理
# ******************** ↑タスク↑ ********************

import sys
from python import main as M


if __name__ == '__main__':
    lg = M.get_logger(__name__, 'log.txt')

    try:
        M.main()
    except:
	    lg.exception(sys.exc_info()) #エラーをlog.txtに書き込む
