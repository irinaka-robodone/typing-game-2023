import pyxel
from text import BDFRenderer
import random
import time

class Character():
    def __init__(self, name: str, hp: int, max_hp: int, attack):
        self.name = name
        self.current_hp = hp
        self.max_hp = max_hp
        self.attack = attack
        
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")

    def is_defeated(self):
        return self.current_hp <= 0

class Enemy(Character):
    def __init__(self, name, hp, max_hp: int,attack):
        super().__init__(name, hp ,max_hp,attack )
        
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp=0
            print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")

        
    
class Player(Character):
    def __init__(self, name, hp, max_hp: int,attack):
        super().__init__(name, hp,max_hp,attack )
        
        

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
        "炎":{"特徴":"熱い",  "HP":100,"Max_hp":100,"attack":10}, 
        "水":{"特徴":"涼しい","HP":140,"Max_hp":140,"attack":5},
        "雷":{"特徴":"速い",  "HP":90,"Max_hp":90,"attack":15},
        "闇":{"特徴":"暗い",  "HP":110,"Max_hp":110,"attack":8},
        "光":{"特徴":"眩しい","HP":120,"Max_hp":120,"attack":7},
        }
        # pyxel.init(160, 120, caption="TypingGame")
        # self.enemy = Enemy(50, 50, 10)  # 敵キャラクターの初期化
        # pyxel.run(self.update, self.draw)
        # pyxel.init(160, 120, caption="HP Decrease Over Time")
        self.hp_decrease_interval = 1  # HPが減少する間隔（フレーム数）
        
        
        self.update_odai()
        # Pyxelアプリを開始
        pyxel.run(self.update, self.draw)


    def update_odai(self):
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
            if self.typed_word == self.current_word:
                self.update_odai()
            if self.enemy.current_hp == 0:
                self.game_state = "won"
            # self.player.take_damage(20)
            if self.player.current_hp == 0:
                self.game_state = "lose"
            # # ここにゲームプレイのロジックを実装
            # # 例: プレイヤーが攻撃を行った場合、敵のHPを減らす
            # if pyxel.btnp(pyxel.KEY_SPACE):  # スペースキーで攻撃
            #     if self.enemy.take_damage(10):  # 敵に10のダメージ
                    
            current_time = time.time()
            if current_time - self.last_decrease_time >= self.hp_decrease_interval:
                self.player.take_damage(1)  # HPを1減少させる
                self.last_decrease_time = current_time
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
            
            pyxel.rect(5, 10, 200, 20, 7)
            pyxel.rect(7, 12, int(186 *self.player.current_hp/self.player.max_hp) , 16, 6)
            pyxel.rect(280,10,200,20,7)
            pyxel.rect(280,12,int(186*self.enemy.current_hp/self.enemy.max_hp),16,6)
            
            
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
                        self.enemy.take_damage(self.player.attack)

                    else:
                        self.is_correct = False
                        
                        print("dou?")
                        self.player.take_damage(self.enemy.attack)
                        if self.player.current_hp == 0:
                            self.game_state = "lose"
                        
                    
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
            max_hp = self.character_details[name]["Max_hp"]
            attack = self.character_details[name]["attack"]
            enemy_hp = self.character_details[enemny_name]["HP"]
            enemny_max_hp = self.character_details[enemny_name]["Max_hp"]
            enemy_atttack = self.character_details[enemny_name]["attack"]
            self.player = Player(name, hp,max_hp,attack )
            self.enemy = Enemy(enemny_name,enemy_hp,enemny_max_hp,enemy_atttack)
            self.game_state = "game"
            self.last_decrease_time = time.time()
            
    
    def draw_character_detail(self, character):
        chara_dict = self.character_details[character]
        detail = chara_dict["特徴"]
        hp = chara_dict["HP"]
        attack = chara_dict["attack"]
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
        self.font.draw_text(x + 5, y + 20,"攻撃力:",0)
        self.font.draw_text(x + 50,y + 20,str(attack),0)




# ゲームを開始
TypingGame()
