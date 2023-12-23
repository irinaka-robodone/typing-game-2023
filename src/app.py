import pyxel
from text import BDFRenderer
import random

class TypingGame:
    def __init__(self):
        # ウィンドウのサイズとタイトルを設定
        pyxel.init(500,300 )
        self.odai_list = ["typing","game","minecraft","python"]  # ここでcurrent_wordを定義
        self.typed_word = ""
        self.is_correct = True
        # 他の初期化処理
        
        self.font = BDFRenderer("assets/font/umplus_j12r.bdf")
        # ゲームの状態を管理する変数
        self.game_state = "title"
        
        self.characters = ["炎", "水", "雷", "闇", "光"]
        self.selected_character = None
        self.current_selection = 0
        self.character_details = {
        "炎": "熱い",
        "水": "涼しい",
        "雷":"速い",
        "闇":"暗い",
        "光":"眩しい",
        }
        self.reset_game()
        # Pyxelアプリを開始
        pyxel.run(self.update, self.draw)


    def reset_game(self):
        self.current_word = random.choice(self.odai_list)  # ランダムな単語を選択
        self.typed_word = ""

    def update(self):
        # タイトル画面でEnterキーが押されたらゲーム状態を変更
        if self.game_state == "title" and pyxel.btnp(pyxel.KEY_RETURN):
                if pyxel.btnp(pyxel.KEY_RETURN):
                    self.game_state = "select_character"
                    
        elif self.game_state == "select_character":
            self.handle_character_selection()
            # self.game_state = "game"
        
        if self.game_state == "game":
            self.handle_input()
        
        
        

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
        
            self.font.draw_text(220,40,self.current_word, 7)
            self.font.draw_text(220,60,self.typed_word,6 if self.is_correct else 8)
            # pyxel.text(220, 60, self.typed_word, 11 if self.is_correct else 8)
            
        if self.game_state == "title":
            # タイトル画面の描画
            pyxel.text(50, 40, "タイトル画面", 7)
        elif self.game_state == "select_character":
            # キャラクター選択画面の描画
            for i, character in enumerate(self.characters):
                color = 7 if i == self.current_selection else 6
                self.font.draw_text(10 + i * 100 ,10 , character, color )
                # pyxel.text(120, 10 + i * 10, character, color)
                
            selected_character = self.characters[self.current_selection]
            self.draw_character_detail(selected_character)


        elif self.game_state == "game":
            # タイピング画面の描画
            self.font.draw_text(0, 80, f"選択されたキャラクター: {self.selected_character}", 7)
        # if self.game_state == "select_character":
        # # キャラクターのリストを描画
        #     for i, character in enumerate(self.characters):
        #         color = 7 if i == self.current_selection else 6
        #         pyxel.text(10, 10 + i * 10, character, color)
                
        #     self.draw_character_detail(self.characters[self.current_selection])

    def handle_input(self):
        # if not self.is_correct:
        #     return
        
        # A-Z でどのキーが押されたかを調べるループ
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
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

    def handle_character_selection(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.current_selection = max(0, self.current_selection - 1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_selection = min(len(self.characters) - 1, self.current_selection + 1)
        elif pyxel.btnp(pyxel.KEY_RETURN):
            self.selected_character = self.characters[self.current_selection]
            self.game_state = "game"
    
    def draw_character_detail(self, character):
        detail = self.character_details[character]
        x, y = 190, 220  # 吹き出しの位置
        width, height = 140, 50  # 吹き出しのサイズ

        # 吹き出しの描画（四角形とテキスト）
        pyxel.rect(x, y, width, height, 7)  # 白い背景
        self.font.draw_text(x + 5, y + 5, detail, 0)  # 黒いテキスト
# ゲームを開始
TypingGame()
