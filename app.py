import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# マインスイーパーの盤面を作成する関数
def generate_minesweeper_board(width, height, mines):
    board = np.zeros((height, width), dtype=int)
    for _ in range(mines):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        board[y, x] = -1  # 地雷を -1 として配置
    return board

# マインスイパーの盤面（空いているかどうかを管理）
def generate_minesweeper_open(width, height):
    open = np.full((height, width), -2, dtype=int)
    return open

# 描画する関数
def plot_board(board, open):
    height, width = board.shape
    fig, ax = plt.subplots(figsize=(width * 0.5, height * 0.5))
    
    # 背景色（未開け: 0 を灰色に設定）
    display_board = np.where(open == 0, np.nan, board)  # 未開け部分を NaN に
    ax.matshow(display_board, cmap="cool", alpha=0.5, vmin=-1, vmax=8)  # 値域を調整

    for y in range(height):
        for x in range(width):
            if open[y, x] == 0:  # 未開けのセル
                ax.text(x, y, "", ha="center", va="center", color="black", bbox=dict(boxstyle="square", facecolor="gray"))
            elif board[y, x] == -1:  # 地雷
                ax.text(x, y, "💣", ha="center", va="center", color="red")
            else:  # その他のセル
                ax.text(x, y, str(board[y, x]), ha="center", va="center", color="black")
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

# Streamlit アプリのインターフェース
st.title("マインスイーパー")
st.write("X, Y 座標を入力して盤面を操作してください！")

# ユーザー入力
width = st.sidebar.slider("横幅", min_value=5, max_value=20, value=10)
height = st.sidebar.slider("縦幅", min_value=5, max_value=20, value=10)
mines = st.sidebar.slider("地雷の数", min_value=1, max_value=50, value=10)

# ボード生成
if "board" not in st.session_state:
    st.session_state.board = generate_minesweeper_board(width, height, mines)
    st.session_state.open = generate_minesweeper_open(width, height)

# 入力フォーム
x = st.number_input("X 座標を入力 (0 から始まるインデックス)", min_value=0, max_value=width-1, value=0)
y = st.number_input("Y 座標を入力 (0 から始まるインデックス)", min_value=0, max_value=height-1, value=0)

# 表示用ボタン
if st.button("セルを開く"):
    st.write(f"座標 ({x}, {y}) を選択しました！")
    if st.session_state.open[y, x] == 0:  # 未開けの場合のみ更新
        st.session_state.open[y, x] = 1  # セルを開く（デモ用に 0 を設定）
    plot_board(st.session_state.board, st.session_state.ope)

# 初期盤面を表示
plot_board(st.session_state.board, st.session_state.open)
