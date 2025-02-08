import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 爆弾の数をカウント
def count_bom(bom, x, y, width, height):
    count = 0
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if i >= 0 and j >= 0 and i < height and j < width:
                count += bom[i, j]        
    return count

# マインスイーパーの盤面（爆弾を管理）
def generate_minesweeper_bom(width, height, mines):
    bom = np.zeros((height, width), dtype=int)
    for _ in range(mines):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        bom[y, x] = 1  # 地雷を 1 として配置
    return bom

# マインスイーパーの盤面（数字を管理）
def generate_minesweeper_board(width, height, bom):
    board = np.zeros((height, width), dtype=int)
    for y in range(height):
        for x in range(width):
            if bom[y, x] == 0:
                board[y, x] = count_bom(bom, x, y, width, height)
            else :
                board[y, x] = -1
    return board

# マインスイパーの盤面（空きマスを管理）
def generate_minesweeper_open(width, height):
    open = np.zeros((height, width), dtype=int)
    return open

# マインスイパーの盤面（フラグを管理）
def generate_minesweeper_flag(width, height):
    flag = np.zeros((height, width), dtype=int)
    return flag


# 描画する関数
def plot_board(board, bom, open, flag):
    height, width = bom.shape
    fig, ax = plt.subplots(figsize=(width * 0.5, height * 0.5))
    
    display_board = np.where(open == 0, np.nan, bom) 
    ax.matshow(display_board, cmap="cool", alpha=0.5, vmin=-1, vmax=8)

    for y in range(height):
        for x in range(width):
            if open[y, x] == 0 and flag[y, x] == 0:  # 未開けのセル
                ax.text(x, y, "", ha="center", va="center", color="black", bbox=dict(boxstyle="square", facecolor="gray"))
            elif flag[y, x] == 1: # フラグ
                ax.text(x, y, "?", ha="center", va="center", color="blue")
            elif bom[y, x] == 1:  # 地雷
                ax.text(x, y, "*", ha="center", va="center", color="red")
            else:  # 数字表示
                ax.text(x, y, str(board[y, x]), ha="center", va="center", color="black")

    # 軸ラベルを表示
    ax.set_xticks(np.arange(0, width)) 
    ax.set_yticks(np.arange(0, height))  
    ax.set_xticklabels(np.arange(1, width+1), fontsize=8) 
    ax.set_yticklabels(np.arange(1, height+1), fontsize=8)  

    # 軸の位置とスタイルを調整
    ax.xaxis.set_ticks_position('top')  
    ax.tick_params(axis="x", rotation=0)  

    # マス目のグリッドを追加
    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)

    ax.tick_params(left=False, right=False, top=False, bottom=False)

    st.pyplot(fig)


# インターフェース
st.title("マインスイーパー")
st.write("X, Y 座標を入力して盤面を操作してください！")

# ゲームの状態
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "game_clear" not in st.session_state:
    st.session_state.game_clear = False

# ユーザー入力
width = st.sidebar.slider("横幅", min_value=5, max_value=20, value=10)
height = st.sidebar.slider("縦幅", min_value=5, max_value=20, value=10)
mines = st.sidebar.slider("地雷の数", min_value=1, max_value=50, value=10)

# ボード生成
if "bom" not in st.session_state:
    st.session_state.bom = generate_minesweeper_bom(width, height, mines)
if "board" not in st.session_state:
    st.session_state.board = generate_minesweeper_board(width, height, st.session_state.bom)
if "open" not in st.session_state:
    st.session_state.open = generate_minesweeper_open(width, height)
if "flag" not in st.session_state:
    st.session_state.flag = generate_minesweeper_flag(width, height)

# 時間経過の表示
elapsed_time = time.time() - st.session_state.start_time
st.sidebar.write(f"経過時間: {int(elapsed_time)} 秒")

# フラグの合計
total_flags = np.sum(st.session_state.flag)
st.sidebar.write(f"現在のフラグ数: {total_flags}")

# リセットボタン
if st.button("リセット"):
    st.session_state.bom = generate_minesweeper_bom(width, height, mines)
    st.session_state.board = generate_minesweeper_board(width, height, st.session_state.bom)
    st.session_state.open = generate_minesweeper_open(width, height)
    st.session_state.flag = generate_minesweeper_flag(width, height)
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.game_clear = False
    st.write("盤面をリセットしました！")

# 入力フォーム
x_input = st.number_input("X 座標を入力", min_value=1, max_value=width, value=1)
y_input = st.number_input("Y 座標を入力", min_value=1, max_value=height, value=1)
x = x_input - 1
y = y_input - 1

# 表示ボタン
if st.button("セルを開く"):
    if st.session_state.flag[y, x] == 0 and st.session_state.open[y, x] == 0:
        if st.session_state.bom[y, x] == 0:
            st.write(f"座標 ({x_input}, {y_input}) を開きました！")
            st.session_state.open[y, x] = 1  # セルを開く

        else :
            st.write("ゲームオーバー！") 
            st.session_state.open[y, x] = 1
            st.session_state.game_over = True
    else :
        st.write(f"座標 ({x_input}, {y_input}) は開けません")

# フラグボタン
if st.button("フラグを立てる"):
    if st.session_state.flag[y, x] == 0 and st.session_state.open[y,x] == 0:
        st.write(f"座標 ({x_input}, {y_input}) にフラグを立てました！")
        st.session_state.flag[y, x] = 1  # フラグを立てる
    elif st.session_state.flag[y, x] == 1:
        st.session_state.flag[y, x] = 0  # フラグを折る
        st.write(f"座標 ({x_input}, {y_input}) を折りました！")
    else :
        st.write(f"座標 ({x_input}, {y_input}) にフラグを立てられません")


# 初期盤面を表示
plot_board(st.session_state.board, st.session_state.bom, st.session_state.open, st.session_state.flag)

# ゲームクリア判定
if np.sum(st.session_state.open) == width * height - mines and not st.session_state.game_over:
    st.write("ゲームクリア！")  
    st.session_state.game_clear = True
    st.session_state.clear_time = elapsed_time

# ゲームクリア/オーバー時に全画面に表示
if st.session_state.game_clear or st.session_state.game_over:
    message = "ゲームオーバー！" if st.session_state.game_over else f"ゲームクリア！ タイム: {int(st.session_state.clear_time)} 秒"
    if st.button("メッセージを消す"):
        st.session_state.game_over = False
        st.session_state.game_clear = False
    else:
        st.markdown(
            f"""
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                        background-color: rgba(0, 0, 0, 0.8); color: white; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 3em; z-index: 9999;">
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )
