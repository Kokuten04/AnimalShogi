"""
タイトル画面を表示し、モード選択を行うモジュール
"""
import sys
import pygame as pg 
import config

class TitleScreen:
    """タイトル画面を管理するクラス"""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self._init_fonts()
        self._init_buttons()

    def _init_fonts(self):
        """フォントの初期化"""
        font_name = "applemyungjo"
        self.title_font = pg.font.SysFont(font_name, 36, bold=True)
        self.button_font = pg.font.SysFont(font_name, 32)

    def _init_buttons(self):
        """ボタンの位置とサイズの初期化"""
        cx = config.WINDOW_WIDTH // 2
        cy = config.WINDOW_HEIGHT // 2
        btn_width, btn_height = 240, 60

        self.btn_ai = pg.Rect(0, 0, btn_width, btn_height)
        self.btn_ai.center = (cx, cy - 20)

        self.btn_pvp = pg.Rect(0, 0, btn_width, btn_height)
        self.btn_pvp.center = (cx, cy + 60)

    def _draw_button(self, rect, text, hover=False):
        """ボタンを描画する"""
        bg_color = (255, 255, 255)
        text_color = config.COLOR_TEXT

        if hover:
            # ホバー時は少し暗くする
            bg_color = (max(0, bg_color[0]-30), max(0, bg_color[1]-30), max(0, bg_color[2]-30))

        pg.draw.rect(self.screen, bg_color, rect, border_radius=10)
        pg.draw.rect(self.screen, config.COLOR_LINE, rect, 2, border_radius=10)

        text_surf = self.button_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def show(self):
        """タイトル画面ループを実行し、選択されたモードを返す"""
        cx = config.WINDOW_WIDTH // 2
        cy = config.WINDOW_HEIGHT // 2

        while True:
            # 背景描画
            self.screen.fill(config.COLOR_BOARD)

            mx, my = pg.mouse.get_pos()

            # タイトル描画
            title_text = "どうぶつしょうぎ"
            title_surf = self.title_font.render(title_text, True, config.COLOR_TEXT)
            title_rect = title_surf.get_rect(center=(cx, cy - 120))
            self.screen.blit(title_surf, title_rect)

            # ボタンホバー判定
            is_hover_ai = self.btn_ai.collidepoint((mx, my))
            is_hover_pvp = self.btn_pvp.collidepoint((mx, my))

            # ボタン描画
            self._draw_button(self.btn_ai, "VS AI", is_hover_ai)
            self._draw_button(self.btn_pvp, "VS Player", is_hover_pvp)

            # イベント処理
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: # 左クリック
                        if is_hover_ai:
                            return "ai"
                        if is_hover_pvp:
                            return "pvp"

            pg.display.update()
            self.clock.tick(30)
