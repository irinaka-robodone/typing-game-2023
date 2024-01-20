import pyxel
from text import BDFRenderer
import random

class Character():
    def __init__(self, name: str, hp: int, max_hp: int = None):
        self.name = name
        self.current_hp = hp
        
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")

    def is_defeated(self):
        return self.current_hp <= 0

class Enemy(Character):
    def __init__(self, name, hp, max_hp: int = None):
        super().__init__(name, hp, hp)
        
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp=0
            print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")

        
    
class Player(Character):
    def __init__(self, name, hp, max_hp: int = None):
        super().__init__(name, hp, hp)
        
        
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
        "炎":{"特徴":"熱い",  "HP":100}, 
        "水":{"特徴":"涼しい","HP":140},
        "雷":{"特徴":"速い",  "HP":90},
        "闇":{"特徴":"暗い",  "HP":110},
        "光":{"特徴":"眩しい","HP":120},
        }
        # pyxel.init(160, 120, caption="TypingGame")
        # self.enemy = Enemy(50, 50, 10)  # 敵キャラクターの初期化
        # pyxel.run(self.update, self.draw)
        
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
            # # ここにゲームプレイのロジックを実装
            # # 例: プレイヤーが攻撃を行った場合、敵のHPを減らす
            # if pyxel.btnp(pyxel.KEY_SPACE):  # スペースキーで攻撃
            #     if self.enemy.take_damage(10):  # 敵に10のダメージ
                    
        if self.game_state == "won":
            """"""
        if self.game_state == "lose":
            """"""

    def draw(self):
        pyxel.cls(0) # 画面をクリア
        # self.enemy.draw()
    
        # タイトル画面の描画
        if self.game_state == "title":
            self.font.draw_text(200, 130, "タイピングゲーム", pyxel.frame_count % 16)
            self.font.draw_text(200, 160, "Enterを押して開始",pyxel.frame_count % 16)
        # ゲーム画面の描画（ここでは仮に設定）
        elif self.game_state == "game":
            # self.font.draw_text(50, 60, "ゲーム中...", 7)
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
            self.font.draw_text(0, 80, f"選択されたキャラクター: {self.player.name}", 7)
            # character = Character("炎", 100)
            # character = Character("水", 140)
            # character = Character("雷", 90)
            # character = Character("闇", 110)
            # character = Character("光", 120)
            hp = self.player.current_hp
            self.font.draw_text(90,100,str(hp),11)
            self.font.draw_text(48,100,"残りHP:",11)
            self.font.draw_text(400,100,str(self.enemy.current_hp),11)
            self.font.draw_text(390,80,self.enemy.name,11)
            self.font.draw_text(355,100,"残りHP:",11)
        elif self.game_state == "won":
            # 勝利画面の描画
            self.font.draw_text(190, 100, "W        I        N", pyxel.frame_count % 16)
        elif self.game_state == "lose":
            self.font.draw_text(170, 100, "L        O        S        E", pyxel.frame_count % 16)
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
                        self.enemy.take_damage(30)
                        if self.enemy.current_hp == 0:
                            self.game_state = "won"
                        self.player.take_damage(20)
                        if self.player.current_hp == 0:
                            self.game_state = "lose"

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
            name = self.characters[self.current_selection]
            self.characters.pop(self.current_selection)
            # print("enemy id: ", self.current_selection + 1)
            enemny_name = random.choice(self.characters)
            # print("enemy_name: ", enemny_name)
            # print("candidates:", self.character_details)
            hp = self.character_details[name]["HP"]
            enemy_hp = self.character_details[enemny_name]["HP"]
            self.player = Player(name, hp)
            self.enemy = Enemy(enemny_name,enemy_hp)
            self.game_state = "game"
            
    
    def draw_character_detail(self, character):
        detail = self.character_details[character]["特徴"]
        hp = self.character_details[character]["HP"]
        x, y = 190, 220  # 吹き出しの位置
        width, height = 140, 50  # 吹き出しのサイズ
        # detail= self.character_details[character]["HP"]
        # x,y = 190,220
        # widht,height = 140,50

        # 吹き出しの描画（四角形とテキスト）
        pyxel.rect(x, y, width, height, 7)  # 白い背景
        self.font.draw_text(x + 5, y + 5, detail, 0)  # 黒いテキスト
        self.font.draw_text(x + 50,y + 5,"HP:",0)
        self.font.draw_text(x + 70,y + 5,str(hp),0)




# ゲームを開始
TypingGame()
