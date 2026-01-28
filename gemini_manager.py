"""
Gemini API を管理するモジュール
"""
import google.generativeai as genai

class GeminiManager:
    """Gemini APIとの通信を管理するクラス"""

    def __init__(self, api_key=None):
        """
        初期化
        """
        # APIキーが指定されていない場合、ターミナルから入力を求める
        if api_key is None:
            print("Google AI Studioで取得したAPIキーを入力してください。")
            api_key = input("API Key > ").strip()

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def get_move(self, board_text_state, valid_moves_list):
        """
        盤面と有効な手を受け取り、Geminiに手を選んでもらう
        """
        moves_str = "\n".join(valid_moves_list)
        prompt = (
            "You are an expert AI player of Dobutsu Shogi (Animal Shogi).\n"
            "You are playing as the 'Enemy' (Player 1).\n"
            "Your objective is to win the game.\n\n"
            "--- Game State ---\n"
            f"{board_text_state}\n\n"
            "--- Valid Moves List ---\n"
            f"{moves_str}\n\n"
            "Instructions:\n"
            "1. Choose the absolute best move from the 'Valid Moves List' "
            "to defeat the opponent.\n"
            "2. Your response must be ONLY the exact string from the list "
            "corresponding to your choice.\n"
            "3. Do not add any explanation, punctuation, or extra text.\n"
        )

        response = self.model.generate_content(prompt)
        return response.text.strip()
