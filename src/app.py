import pyxel
from text import BDFRenderer
import random
import time
from copy import deepcopy

class TypingGame:
    def __init__(self):
        # ウィンドウのサイズとタイトルを設定
        pyxel.init(500,300)
        pyxel.mouse(True)
        
        # お題の文章リストを初期化する
        self.odai_list = ["typing","game","minecraft","python", "help", "key config", "key mapping", "test", "ammo", "hello", "programming", "shot", "fire"]
        self.odai_list_playing = deepcopy(self.odai_list)
        self.typed_word = ""
        self.is_correct = True
        # ビットマップフォントをロードする
        self.font = BDFRenderer("assets/font/umplus_j12r.bdf")
        # ゲームの状態を管理する変数
        self.game_state = "title"
        # お題の文、キー入力状況の初期化
        self.reset_game()
        # Pyxelアプリを開始
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        
        if self.game_state == "result":
            self.odai_list_playing = deepcopy(self.odai_list)
            print(self.odai_list_playing)
            self.game_state = "title"
        
        if len(self.odai_list_playing) < 1:
            self.game_state = "result"
            self.typed_word = ""
            self.current_word = ""
            self.elapsed_time = time.time() - self.start_time
            return
        
        odai_id = random.choice(range(len(self.odai_list_playing)))  # ランダムな単語を選択
        print(self.odai_list_playing[odai_id])
        self.current_word = self.odai_list_playing[odai_id]
        self.odai_list_playing.pop(odai_id)
        self.typed_word = ""
        
    def update(self):
        # タイトル画面でEnterキーが押されたらゲーム状態を変更
        if self.game_state == "title" and pyxel.btnp(pyxel.KEY_RETURN):
            self.game_state = "game"
            self.start_time = time.time()
        
        if self.game_state == "game":
            self.handle_input()
            
        elif self.game_state == "result":
            self.update_result()
        

    def draw(self):
        pyxel.cls(0) # 画面をクリア
    
        # タイトル画面の描画
        if self.game_state == "title":
            self.font.draw_text(200, 130, "タイピングゲーム", pyxel.frame_count % 16)
            self.font.draw_text(200, 160, "Enterを押して開始",pyxel.frame_count % 16)
        # ゲーム画面の描画（ここでは仮に設定）
        elif self.game_state == "game":
            self.font.draw_text(50, 60, "ゲーム中...", 7)
            # pyxel.cls(0)
        
            self.font.draw_text(220,40,self.current_word, 1)
            self.font.draw_text(220,60,self.typed_word,11 if self.is_correct else 8)
            # pyxel.text(220, 60, self.typed_word, 11 if self.is_correct else 8)
            
        elif self.game_state == "result":
            self.font.draw_text(100, 40, f"クリア時間: {round(self.elapsed_time, 1)}秒", 1)
            self.font.draw_text(220, 100, "Play Again?", (pyxel.frame_count // 2) % 16)
            self.font.draw_text(220, 130, "Press Enter", (pyxel.frame_count // 2) % 16)

    def handle_input(self):
        # if not self.is_correct:
        #     return
        
        # A-Z でどのキーが押されたかを調べるループ
        for key in range(pyxel.KEY_SPACE, pyxel.KEY_Z + 1):
            # print(key)
            # もし、そのキーが押されていたら
            if pyxel.btnp(key):
                # 数字をアルファべっとに　変換する
                char = chr(int(key))
                print(key, char)
                # お題の単語: current_word
                # 正確にタイプされた単語: typed_word
                if len(self.typed_word) < len(self.current_word):
                    # 正解のキーを定義する
                    expected_char = self.current_word[len(self.typed_word)]
                    if char == expected_char:
                        self.typed_word += char
                        self.is_correct = True
                    else:
                        self.is_correct = False
                if self.typed_word == self.current_word:
                    print("dou?")
                    self.reset_game()
                    
    def update_result(self):
        """ゲームが終了したときにする処理
        """
        if pyxel.btnp(pyxel.KEY_RETURN):    
            self.reset_game()

# ゲームを開始
TypingGame()
