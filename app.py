import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# マインスイーパーの盤面を作成する関数
def generate_minesweeper_board(width, height, mines):
    board = np.zeros((height, width), dtype=int)
    for _ in range(mines):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        board[y, x] = 1  # 地雷を 1 として配置
    return board

# マインスイパーの盤面（空いているかどうかを管理）
def generate_minesweeper_open(width, height):
    open = np.zeros((height, width), dtype=int)
    return open

# マインスイパーの盤面（フラグが立っているかどうかを管理）
def generate_minesweeper_flag(width, height):
    flag = np.zeros((height, width), dtype=int)
    return flag

def count_bom(board, x, y, width, height):
    count = 0
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if i >= 0 and j >= 0 and i < height and j < width:
                count += board[i, j]
                
    return count


# 描画する関数
def plot_board(board, open, flag):
    height, width = board.shape
    fig, ax = plt.subplots(figsize=(width * 0.5, height * 0.5))
    
    # 背景色（未開け: 0 を灰色に設定）
    display_board = np.where(open == 0, np.nan, board)  # 未開け部分を NaN に
    ax.matshow(display_board, cmap="cool", alpha=0.5, vmin=-1, vmax=8)  # 値域を調整

    for y in range(height):
        for x in range(width):
            if open[y, x] == 0 and flag[y, x] == 0:  # 未開けのセル
                ax.text(x, y, "", ha="center", va="center", color="black", bbox=dict(boxstyle="square", facecolor="gray"))
            elif flag[y, x] == 1:
                ax.text(x, y, "?", ha="center", va="center", color="blue")
            elif board[y, x] == 1:  # 地雷
                ax.text(x, y, "*", ha="center", va="center", color="red")
            else:  # その他のセル
                count = count_bom(board, x, y, width, height)
                ax.text(x, y, str(count), ha="center", va="center", color="black")
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

# Streamlit アプリのインターフェース
st.title("マインスイーパー")
st.write("X, Y 座標を入力して盤面を操作してください！")

# ゲームの状態
game_over = False
game_clear = False

# ユーザー入力
width = st.sidebar.slider("横幅", min_value=5, max_value=20, value=10)
height = st.sidebar.slider("縦幅", min_value=5, max_value=20, value=10)
mines = st.sidebar.slider("地雷の数", min_value=1, max_value=50, value=10)

# ボード生成
if "board" not in st.session_state:
    st.session_state.board = generate_minesweeper_board(width, height, mines)
if "open" not in st.session_state:
    st.session_state.open = generate_minesweeper_open(width, height)
if "flag" not in st.session_state:
    st.session_state.flag = generate_minesweeper_flag(width, height)

total_flags = np.sum(st.session_state.flag)
st.sidebar.write(f"現在のフラグ数: {total_flags}")

# 入力フォーム
x = st.number_input("X 座標を入力 (0 から始まるインデックス)", min_value=0, max_value=width-1, value=0)
y = st.number_input("Y 座標を入力 (0 から始まるインデックス)", min_value=0, max_value=height-1, value=0)

# 表示用ボタン
if st.button("セルを開く"):
    if st.session_state.flag[y, x] == 0 and st.session_state.open[y, x] == 0:
        if st.session_state.board[y, x] == 0:
            st.write(f"座標 ({x}, {y}) を開きました！")
            st.session_state.open[y, x] = 1  # セルを開く
        else :
            st.session_state.open[y, x] = 1
            st.write("ゲームオーバー！")
            game_over = True
    else :
        st.write(f"座標 ({x}, {y}) は開けません")

if st.button("フラグを立てる"):
    if st.session_state.flag[y, x] == 0 and st.session_state.open[y,x] == 0:
        st.write(f"座標 ({x}, {y}) にフラグを立てました！")
        st.session_state.flag[y, x] = 1  # フラグを立てる
    elif st.session_state.flag[y, x] == 1:
        st.session_state.flag[y, x] = 0  # フラグを折る
        st.write(f"座標 ({x}, {y}) を折りました！")
    else :
        st.write(f"座標 ({x}, {y}) にフラグを立てられません")

# リセットボタン
if st.button("リセット"):
    st.session_state.board = generate_minesweeper_board(width, height, mines)
    st.session_state.open = generate_minesweeper_open(width, height)
    st.session_state.flag = generate_minesweeper_flag(width, height)
    st.write("盤面をリセットしました！")

# 初期盤面を表示
plot_board(st.session_state.board, st.session_state.open, st.session_state.flag)

if np.sum(st.session_state.open) == width * height - mines and st.session_state.board[y, x] == 0:
    st.write("ゲームクリア！")  
    game_clear = True


# ゲームクリア/オーバー時に全画面に表示
if "show_message" not in st.session_state:
    st.session_state.show_message = True

if game_clear or game_over:
    if st.session_state.show_message:
        message = "ゲームオーバー！" if game_over else "ゲームクリア！"
        st.markdown(
            f"""
            <div id="overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                        background-color: rgba(0, 0, 0, 0.8); color: white; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 3em; z-index: 9999;">
                {message}
            </div>
            <script>
                setTimeout(function() {{
                    var overlay = document.getElementById('overlay');
                    if (overlay) {{
                        overlay.remove();
                    }}
                }}, 3000);
            </script>
            """,
            unsafe_allow_html=True
        )
        st.session_state.show_message = False  # メッセージを一度だけ表示
