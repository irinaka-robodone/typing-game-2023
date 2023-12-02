import pyxel
from text import BDFRenderer
import random

class TypingGame:
    def __init__(self):
        # ウィンドウのサイズとタイトルを設定
        pyxel.init(1000,600 )
        self.odai_list = ["a","q","w","e","r","t","y","u"]  # ここでcurrent_wordを定義
        self.typed_word = ""
        self.is_correct = True
        # 他の初期化処理
        
        self.font = BDFRenderer("assets/font/umplus_j12r.bdf")
        # ゲームの状態を管理する変数
        self.game_state = "title"
        self.reset_game()
        # Pyxelアプリを開始
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.current_word = random.choice(self.odai_list)  # ランダムな単語を選択

    def update(self):
        # タイトル画面でEnterキーが押されたらゲーム状態を変更
        if self.game_state == "title" and pyxel.btnp(pyxel.KEY_RETURN):
            self.game_state = "game"
        
        if self.game_state == "game":
            self.handle_input()
        

    def draw(self):
        pyxel.cls(0) # 画面をクリア
    
        # タイトル画面の描画
        if self.game_state == "title":
            self.font.draw_text(50, 60, "タイピングゲーム", pyxel.frame_count % 16)
            self.font.draw_text(43, 80, "Enterを押して開始",pyxel.frame_count % 16)
        # ゲーム画面の描画（ここでは仮に設定）
        elif self.game_state == "game":
            self.font.draw_text(50, 60, "ゲーム中...", 7)
            # pyxel.cls(0)
        
            pyxel.text(50, 40, self.current_word, 10)
            pyxel.text(50, 50, self.typed_word, 11 if self.is_correct else 8)

    def handle_input(self):
        # if not self.is_correct:
        #     return
        
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            # print(key)
            if pyxel.btnp(key):
                char = chr(int(key))
                print(key, char)
                expected_char = self.current_word[len(self.typed_word)]
                if char == expected_char:
                    self.typed_word += char
                else:
                    self.is_correct = False
                if self.typed_word == self.current_word:
                    print("dou?")
                    self.reset_game()
# ゲームを開始
TypingGame()
