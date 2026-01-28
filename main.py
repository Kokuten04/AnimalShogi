"""
どうぶつしょうぎのメインプログラム
"""
#2454755 矢島隆史

import sys
import pygame as pg
import config
from board import Board
from title_screen import TitleScreen

# GeminiManagerをインポート
try:
    from gemini_manager import GeminiManager
    HAS_GEMINI = True
except ImportError:
    print("gemini_manager.py not found or google-generativeai not installed.")
    HAS_GEMINI = False


def main():
    """メイン関数"""
    pg.init()
    pg.display.set_caption("どうぶつしょうぎ")
    display_height = config.WINDOW_HEIGHT + 100
    screen = pg.display.set_mode((config.WINDOW_WIDTH, display_height))
    clock = pg.time.Clock()

    # --- タイトル画面 ---
    title = TitleScreen(screen)
    mode = title.show()
    print(f"Game Mode Selected: {mode}")

    # 盤面の初期化
    board = Board()

    # GeminiManagerの初期化
    gemini = None
    if HAS_GEMINI and mode == "ai":
        gemini = GeminiManager()
        print("Gemini AI initialized.")

    # メインループ
    while True:
        # 画面を初期化する。
        screen.fill(pg.Color("WHITE"))

        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # マウスクリック処理
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # 左クリック
                    # AIモード時、AI思考中はクリックをブロック
                    if mode == "ai" and gemini and board.turn == 1 and not board.game_over:
                        pass
                    else:
                        mx, my = pg.mouse.get_pos()
                        board.handle_click(mx, my)

        # AIの処理 (AIモード かつ Enemyターン かつ Gemini有効時)
        if mode == "ai" and board.turn == 1 and not board.game_over and gemini:
            # メッセージ更新と描画
            board.set_message("Gemini is thinking...")
            board.draw(screen)
            pg.display.update()

            # AIの手を計算
            state_text = board.get_board_state_as_text()
            legal_moves = board.get_legal_moves(1)

            if legal_moves:
                move_str = gemini.get_move(state_text, legal_moves)
                if move_str:
                    print(f"Gemini: {move_str}")
                    board.execute_ai_move(move_str)
                    board.set_message(f"Gemini: {move_str}")
                else:
                    print("Gemini failed to move.")
            else:
                print("Gemini has no moves.")

        # 描画
        board.draw(screen)

        # 画面を表示する。
        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
