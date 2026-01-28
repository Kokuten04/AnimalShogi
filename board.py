"""
どうぶつしょうぎの盤面
ゲームの状態、ロジック、描画を管理する
"""
import random
import pygame as pg
import config

class Board:
    """ゲームの盤面とロジックを表すクラス"""
    def __init__(self):
        """初期化"""
        # grid[col][row] の形になるように修正 (外側がcol、内側がrow)
        self.grid = [[None] * config.BOARD_ROWS for _ in range(config.BOARD_COLS)]
        self.hands = [[], []] #持ち駒を表す。インデックスが0なら自身、1なら相手。
        self.turn = random.randint(0, 1) #ターンを扱う変数。0なら自身が先行、1なら相手が先行。ランダムで決定する。
        self.selected = None #駒選択時に用いる
        self.possible_moves = [] #移動可能な位置を判定
        self.game_over = False
        self.winner = None
        self.message_text = "" # メッセージ表示用
        self.turn_n = 1

        #初期配置
        self.reset_board()

    def reset_board(self):
        """盤面を初期状態にリセットする"""
        # grid[col][row] の形になるように修正
        self.grid = [[None] * config.BOARD_ROWS for _ in range(config.BOARD_COLS)]
        self.hands = [[], []] #持ち駒を表す。インデックスが0なら自身、1なら相手。
        self.turn = random.randint(0, 1) #ターンを扱う変数。0なら自身が先行、1なら相手が先行。ランダムで決定する。
        self.selected = None #駒選択時に用いる
        self.possible_moves = [] #移動可能な位置を判定
        self.game_over = False
        self.winner = None
        self.message_text = ""

        self.grid[0][0] = ("G", 1)
        self.grid[1][0] = ("L", 1)
        self.grid[2][0] = ("E", 1)
        self.grid[1][1] = ("C", 1)


        self.grid[0][3] = ("E", 0)
        self.grid[1][3] = ("L", 0)
        self.grid[2][3] = ("G", 0)
        self.grid[1][2] = ("C", 0)

    def draw(self, screen):
        """ゲーム要素を描画する"""
        self.draw_board(screen)
        self.draw_highlights(screen)
        self.draw_pieces(screen)
        self.draw_message(screen)
        self.draw_turn(screen)
        self.draw_game_over(screen)

    def set_message(self, text):
        """メッセージを設定する"""
        self.message_text = text

    def draw_message(self, screen):
        """メッセージを描画する"""
        if not self.message_text:
            return

        font = pg.font.SysFont("arial", 20)
        # テキストを描画
        text_surf = font.render(self.message_text, True, (0, 0, 0))
        # 画面下部に配置
        rect = text_surf.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT + 50))
        screen.blit(text_surf, rect)

    def get_legal_moves(self, player):
        """指定プレイヤーの手の全候補を返す（Gemini用文字列リスト）"""
        moves = []

        # 盤上の駒の移動
        for col in range(config.BOARD_COLS):
            for row in range(config.BOARD_ROWS):
                piece = self.grid[col][row]
                if piece and piece[1] == player:
                    valid_targets = self.get_valid_moves(col, row)
                    for t_col, t_row in valid_targets:
                        # フォーマット: MOVE: from_col,from_row -> to_col,to_row
                        moves.append(f"MOVE: {col},{row} -> {t_col},{t_row}")

        # 持ち駒を打つ
        current_hand = self.hands[player]

        checked_types = set()

        empty_cells = []
        for c in range(config.BOARD_COLS):
            for r in range(config.BOARD_ROWS):
                if self.grid[c][r] is None:
                    empty_cells.append((c, r))

        for p_type in current_hand:
            if p_type in checked_types:
                continue
            checked_types.add(p_type)

            for t_col, t_row in empty_cells:
                moves.append(f"DROP: {p_type} -> {t_col},{t_row}")

        return moves

    def execute_ai_move(self, move_str):
        """Geminiから受け取った文字列の手を実行する"""
        if move_str.startswith("MOVE:"):
            # MOVE: 1,2 -> 1,1
            parts = move_str.replace("MOVE:", "").strip().split("->")
            from_coords = parts[0].strip().split(",")
            to_coords = parts[1].strip().split(",")

            f_col, f_row = int(from_coords[0]), int(from_coords[1])
            t_col, t_row = int(to_coords[0]), int(to_coords[1])

            # 選択状態にして移動実行
            self.selected = (f_col, f_row)
            self.execute_move(t_col, t_row)

        elif move_str.startswith("DROP:"):
            # DROP: C -> 1,2
            parts = move_str.replace("DROP:", "").strip().split("->")
            p_type = parts[0].strip()
            to_coords = parts[1].strip().split(",")
            t_col, t_row = int(to_coords[0]), int(to_coords[1])

            # 持ち駒の中から対象のインデックスを探す
            hand_index = -1
            for i, hand_p in enumerate(self.hands[self.turn]):
                if hand_p == p_type:
                    hand_index = i
                    break

            if hand_index != -1:
                self.selected = ("hand", hand_index)
                self.execute_move(t_col, t_row)
            else:
                print(f"Error: {p_type} was not found in hands")


    def draw_game_over(self, screen):
        """ゲーム終了メッセージを描画する"""
        if self.winner is None:
            return

        font = pg.font.SysFont("Arial", 50, bold=True)
        msg = ""     # 初期化を追加
        color = (0, 0, 0) # 初期化を追加

        if self.winner == 0:
            msg = "YOU WIN!"
            color = (255, 0, 0)
        elif self.winner == 1:
            msg = "YOU LOSE!"
            color = (0, 0, 255)

        if msg: # msgが空でない場合のみ描画
            text = font.render(msg, True, color)
            # 画面中央に表示
            text_rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

    def draw_board(self, screen):
        """盤面の背景とグリッド線を描画する"""
        board_rect = (
            0,
            config.OFFSET_Y,
            config.BOARD_COLS * config.TILE_SIZE,
            config.BOARD_ROWS * config.TILE_SIZE
        )
        pg.draw.rect(screen, config.COLOR_BOARD, board_rect)

        for col in range(config.BOARD_COLS):
            for row in range(config.BOARD_ROWS):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE + config.OFFSET_Y
                rect = pg.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)

                #グリッドを描画
                pg.draw.rect(screen, config.COLOR_LINE, rect, 1)

    def draw_highlights(self, screen):
        """選択と移動可能場所のハイライトを描画する"""
        for col in range(config.BOARD_COLS):
            for row in range(config.BOARD_ROWS):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE + config.OFFSET_Y
                rect = pg.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)

                #ハイライトを描画
                if self.selected == (col, row):
                    pg.draw.rect(screen, config.COLOR_SELECT, rect.inflate(-4, -4), 4)

                if (col, row) in self.possible_moves:
                    pg.draw.rect(screen, config.COLOR_POSSIBLE, rect.inflate(-10, -10), 4)

        # 持ち駒のハイライト
        if self.selected and self.selected[0] == "hand" and self.turn == 0:
            i = self.selected[1]
            if 0 <= i < len(self.hands[0]):
                y_start_player = config.OFFSET_Y + config.BOARD_ROWS * config.TILE_SIZE + 20
                x = i * 60 + 20
                rect = pg.Rect(x, y_start_player, 50, 50)
                pg.draw.rect(screen, config.COLOR_SELECT, rect.inflate(4, 4), 4)

    def draw_pieces(self, screen):
        """盤上の駒を描画する"""
        # 日本語フォント指定
        font = pg.font.SysFont("applemyungjo", 40)

        for col in range(config.BOARD_COLS):
            for row in range(config.BOARD_ROWS):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE + config.OFFSET_Y
                rect = pg.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)

                piece = self.grid[col][row]
                if piece:
                    p_type = piece[0]
                    owner = piece[1]
                    if owner == 0:
                        bg_color = config.COLOR_PLAYER
                    else:
                        bg_color = config.COLOR_ENEMY

                    pg.draw.rect(screen, bg_color, rect.inflate(-20, -20), border_radius=8)
                    pg.draw.rect(
                        screen,
                        config.COLOR_LINE,
                        rect.inflate(-20, -20),
                        2,
                        border_radius=8
                    )

                    text_content = config.PIECE_DISPLAY_NAMES.get(p_type, p_type)
                    text_surf = font.render(text_content, True, config.COLOR_TEXT)

                    text_rect = text_surf.get_rect(center=rect.inflate(-20, -20).center)
                    screen.blit(text_surf, text_rect)


        # 持ち駒描画
        self.draw_hands(screen, font)

    def draw_hands(self, screen, font):
        """持ち駒を描画する"""
        y_start_enemy = 20
        for i, p_type in enumerate(self.hands[1]):
            x = i * 60 + 20
            rect = pg.Rect(x, y_start_enemy, 50, 50)

            # 手駒選択時のハイライト
            if self.selected == ("hand", i) and self.turn == 1:
                pg.draw.rect(screen, config.COLOR_SELECT, rect.inflate(4, 4), 4)

            pg.draw.rect(screen, config.COLOR_ENEMY, rect, border_radius=5)
            pg.draw.rect(screen, config.COLOR_LINE, rect, 2, border_radius=5)

            p_name = config.PIECE_DISPLAY_NAMES.get(p_type, p_type)
            text = font.render(p_name, True, config.COLOR_TEXT)
            screen.blit(text, text.get_rect(center=rect.center))

        y_start_player = config.OFFSET_Y + config.BOARD_ROWS * config.TILE_SIZE + 20
        for i, p_type in enumerate(self.hands[0]):
            x = i * 60 + 20
            rect = pg.Rect(x, y_start_player, 50, 50)

            # 手駒選択時のハイライト (Player)
            if self.selected == ("hand", i) and self.turn == 0:
                pg.draw.rect(screen, config.COLOR_SELECT, rect.inflate(4, 4), 4)

            pg.draw.rect(screen, config.COLOR_PLAYER, rect, border_radius=5)
            pg.draw.rect(screen, config.COLOR_LINE, rect, 2, border_radius=5)
            p_name = config.PIECE_DISPLAY_NAMES.get(p_type, p_type)
            text = font.render(p_name, True, config.COLOR_TEXT)
            screen.blit(text, text.get_rect(center=rect.center))

    def handle_click(self, mx, my):
        """マウスクリックイベントを処理する"""
        # 盤面
        board_area_y = config.OFFSET_Y
        board_area_height = config.BOARD_ROWS * config.TILE_SIZE

        if board_area_y <= my < board_area_y + board_area_height:
            col = mx // config.TILE_SIZE
            row = (my - board_area_y) // config.TILE_SIZE
            self.select(col, row)

        else:
            # 持ち駒(相手側)
            if 20 <= my <= 70:
                if self.turn == 1:
                    hand_index = (mx - 20) // 60
                    if 0 <= hand_index < len(self.hands[1]):
                        self.select(0, 0, is_hand_click=True, hand_index=hand_index)

            # 持ち駒(自身側)
            hand_y_start = config.OFFSET_Y + config.BOARD_ROWS * config.TILE_SIZE + 20
            if hand_y_start <= my <= hand_y_start + 50:
                if self.turn == 0:
                    hand_index = (mx - 20) // 60
                    if 0 <= hand_index < len(self.hands[0]):
                        self.select(0, 0, is_hand_click=True, hand_index=hand_index)

    def _handle_hand_click(self, hand_index):
        """持ち駒選択処理の関数"""
        # 現在のターンプレイヤーの持ち駒を参照
        target_hand = self.hands[self.turn]
        if not 0 <= hand_index < len(target_hand):
            return

        # 既に同じ持ち駒を選択中なら解除
        if self.selected == ("hand", hand_index):
            self.selected = None
            self.possible_moves = []
        else:
            self.selected = ("hand", hand_index)
            self.possible_moves = []
            for c in range(config.BOARD_COLS):
                for r in range(config.BOARD_ROWS):
                    if self.grid[c][r] is None:
                        self.possible_moves.append((c, r))

    def select(self, col, row, is_hand_click=False, hand_index=-1):
        """駒を選択、または移動を実行する"""
        if self.game_over:
            return

        # 持ち駒クリック処理
        if is_hand_click:
            self._handle_hand_click(hand_index)
            return

        if self.selected and (col, row) in self.possible_moves and not is_hand_click:
            self.execute_move(col, row)
            return

        if not is_hand_click:
            if 0 <= col < config.BOARD_COLS and 0 <= row < config.BOARD_ROWS:
                piece = self.grid[col][row]
                if piece and piece[1] == self.turn:
                    self.selected = (col, row)
                    self.possible_moves = self.get_valid_moves(col, row)
                    return

        self.selected = None
        self.possible_moves = []

    def get_valid_moves(self, col, row):
        """指定位置の駒の有効な移動先リストを返す"""
        moves = []
        piece = self.grid[col][row]
        if not piece:
            return []

        p_type, owner = piece

        # "H"はひよこが成った状態
        directions = config.PIECE_MOVES.get(p_type, [])

        # 相手の駒(owner=1)は動きを反転させる
        current_directions = []
        if owner == 1:
            for dx, dy in directions:
                current_directions.append((-dx, -dy))
        else:
            current_directions = directions

        for dx, dy in current_directions:
            nx, ny = col + dx, row + dy

            if 0 <= nx < config.BOARD_COLS and 0 <= ny < config.BOARD_ROWS:
                target = self.grid[nx][ny]
                if target is None:
                    moves.append((nx, ny))
                elif target[1] != owner: # 相手の駒なら取れる!
                    moves.append((nx, ny))

        return moves

    def execute_move(self, target_col, target_row):
        """移動を実行する"""
        if not self.selected:
            return

        # 持ち駒の場合
        if isinstance(self.selected, tuple) and self.selected[0] == "hand":
            self._execute_drop(target_col, target_row)
        # 移動
        elif isinstance(self.selected, tuple) and len(self.selected) == 2:
            self._execute_board_move(target_col, target_row)

        # ターン交代
        self._end_turn()

    def draw_turn(self,screen):
        """ターン数を描画する"""
        if self.turn == 0:
            player_msg = f"Turn {self.turn_n}: Your Turn"
        else:
            player_msg = f"Turn {self.turn_n}: Enemy Turn"

        font = pg.font.SysFont("arial", 20)
        # テキストを描画
        text_surf = font.render(player_msg, True, (0, 0, 0))
        # 画面下部に配置
        rect = text_surf.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT + 80))
        screen.blit(text_surf, rect)


    def _execute_drop(self, target_col, target_row):
        """持ち駒からの打つ動作を実行する"""
        hand_index = self.selected[1]
        p_type = self.hands[self.turn][hand_index]
        self.hands[self.turn].pop(hand_index)
        self.grid[target_col][target_row] = (p_type, self.turn)

    def _execute_board_move(self, target_col, target_row):
        """盤上の駒移動を実行する"""
        from_col, from_row = self.selected
        moving_piece = self.grid[from_col][from_row]
        target_piece = self.grid[target_col][target_row]

        if target_piece:
            self._process_capture(target_piece)

        self.grid[target_col][target_row] = moving_piece
        self.grid[from_col][from_row] = None

        self._process_promotion(moving_piece, target_col, target_row)

        self._check_try_win(target_col, target_row)

    def _process_capture(self, target_piece):
        """駒を取る処理を行う"""
        captured_type = target_piece[0]
        # 成っている駒を取ったら元に戻る
        if captured_type == "H":
            captured_type = "C"
        self.hands[self.turn].append(captured_type)

        # ライオンを取ったら勝ち
        if captured_type == "L":
            self.winner = self.turn
            self.game_over = True

    def _process_promotion(self, moving_piece, target_col, target_row):
        """成りの処理を行う"""
        p_type = moving_piece[0]
        owner = moving_piece[1]

        # ヒヨコの場合のみ判定
        if p_type == "C":
            must_promote = False

            # 自分が一番上へ移動
            if owner == 0 and target_row == 0:
                must_promote = True
            # 相手が一番下へ移動
            elif owner == 1 and target_row == config.BOARD_ROWS - 1:
                must_promote = True

            if must_promote:
                self.grid[target_col][target_row] = ("H", owner)

    def _check_try_win(self, col, row):
        """トライによる勝利判定を行う"""
        piece = self.grid[col][row]
        if not piece:
            return

        p_type, owner = piece
        if p_type == "L":
            if (owner == 0 and row == 0) or \
               (owner == 1 and row == config.BOARD_ROWS - 1):
                self.winner = owner
                self.game_over = True

    def _end_turn(self):
        """ターンを終了し、プレイヤーを交代する"""
        self.selected = None
        self.possible_moves = []
        if not self.game_over:
            self.turn = 1 - self.turn
            self.turn_n +=1

    def get_board_state_as_text(self):
        """現在の盤面をGemini API用のテキスト形式で返す"""
        lines = []
        if self.turn == 0:
            turn_str = "Player (0)"
        else:
            turn_str = "Enemy (1)"
        lines.append(f"Current Turn: {turn_str}")

        lines.append("--- Board Layout (col, row) ---")
        # 盤面をテキスト化
        for row in range(config.BOARD_ROWS):
            row_items = []
            for col in range(config.BOARD_COLS):
                piece = self.grid[col][row]
                if piece:
                    p_type, owner = piece
                    if owner == 0:
                        owner_mark = "Player"
                    else:
                        owner_mark = "Enemy"
                    item = f"[{col},{row}:{p_type}({owner_mark})]"
                else:
                    item = f"[{col},{row}: . ]"
                row_items.append(item)
            lines.append(" ".join(row_items))

        lines.append("--- Hands ---")
        lines.append(f"Player Hand: {self.hands[0]}")
        lines.append(f"Enemy Hand : {self.hands[1]}")

        return "\n".join(lines)
