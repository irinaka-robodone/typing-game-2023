import pyxel
from text import BDFRenderer
import random
import time

# ↓ステージ構想↓
# キャラクター選択画面とゲーム画面の間にステージ選択画面ありけり
# ステージは４個＋１個あります、４個は四天王となっています彼らは一人一人が固有の能力を持っています、四天王は誰からでも倒すことができます
# １個はラスボスとなっており四天王をすべて倒すとラスボスに挑むことができます
# 四天王１→！間違えたら即死ステージ！間違えたら８０ダメージくらうぞ！！！さらに敵の体力は多いぞ（２５０ぐらい）、間違えずにできるのか！
# 四天王２→！スピード勝負！時間経過で食らうダメージが８ダメージだ！その代わりに体力が少なめだ（１８０ぐらい）、速く打てるのか！
# 四天王３→！無限に続く戦い！相手は一定時間で体力を回復するぞ！体力は（２００ぐらい）
# 四天王４→！自分との闘い！相手は自分！？ステータスがミラーされているぞ
# ボス→全体的なステータス全て高い
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
        self.SCREEN_SIZE = (500, 300)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])
        self.odai_list = ["typing","game","minecraft","python","thelegendofzelda","splatoon","grandtheftauto","google","logicool","steam","steelseries","apexlegends","fortnite","subnautica","citysskyline"]  # ここでcurrent_wordを定義
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
        "炎":{"特徴":"熱い",  "HP":350,"Max_hp":350,"attack":2}, 
        "水":{"特徴":"涼しい","HP":4,"Max_hp":400,"attack":1},
        "雷":{"特徴":"速い",  "HP":4,"Max_hp":450,"attack":5},
        "闇":{"特徴":"暗い",  "HP":5,"Max_hp":550,"attack":4},
        "光":{"特徴":"眩しい","HP":600,"Max_hp":600,"attack":100},
        }
        self.stages=["1","2","3","4","5"]
        self.selected_stage = None
        self.current_stage_selection = 0
        self.stages_details ={
        "1":{"ギミック":"間違えたら即死", "enemy_name": "四天王１","enemy_hp":400,"enemy_max_hp":400,"enemy_attack":10,"damage":5,"heal":0},
        "2":{"ギミック":"スピード勝負","enemy_name":"四天王２","enemy_hp":400,"enemy_max_hp":400,"enemy_attack":10,"damage":1,"heal":0},
        "3":{"ギミック":"無限に続く戦い","enemy_name":"四天王３","enemy_hp":400,"enemy_max_hp":400,"enemy_attack":10,"damage":5,"heal":10},
        "4":{"ギミック":"自分との戦い","enemy_name":"四天王４","enemy_hp":400,"enemy_max_hp":400,"enemy_attack":10,"damage":5,"heal":0},
        "5":{"ギミック":"最後の戦い","enemy_name":"ラスボス","enemy_hp":1500,"enemy_max_hp":1500,"enemy_attack":20,"damage":20,"heal":10},
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
            
        if self.game_state == "select_stage":
            self.handle_stage_selection()
        
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
            
        elif self.game_state == "select_stage":
            for i,stages in enumerate(self.stages):
                color = 7 if i ==self.current_stage_selection else 6
                self.font.draw_text(20+ i * 100,10,stages,color)
            selected_stage = self.stages[self.current_stage_selection]
            self.draw_stage_detail(selected_stage)
            
        elif self.game_state == "game":
            # タイピング画面の描画
            self.font.draw_text(0, 80, f"選択されたキャラクター: {self.player.name}", 7)
            self.font.draw_text(0, self.SCREEN_SIZE[1] - 20, str(self.stages_details[self.selected_stage]), 7)
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
            self.font.draw_text(190, 120, "Enterキーを押してね", pyxel.frame_count % 16)
            if pyxel.btnp(pyxel.KEY_RETURN) :
                self.game_state = "select_stage"
            else:
                pass
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
            # print("enemy_name: ", enemny_name)
            # print("candidates:", self.character_details)
            hp = self.character_details[name]["HP"]
            max_hp = self.character_details[name]["Max_hp"]
            attack = self.character_details[name]["attack"]
            self.player = Player(name, hp,max_hp,attack )
            self.game_state = "select_stage"
            self.last_decrease_time = time.time()
    
    def handle_stage_selection(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.current_stage_selection = max(0,self.current_stage_selection - 1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_stage_selection = min(len(self.stages) - 1,self.current_stage_selection + 1)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_stage = self.stages[self.current_stage_selection]
            stage_info = self.stages_details[self.selected_stage]
            enemy_hp = stage_info["enemy_hp"]
            enemy_name = stage_info["enemy_name"]
            enemy_attack = stage_info["enemy_attack"]
            enemy_max_hp = stage_info["enemy_max_hp"]
            self.enemy = Enemy(enemy_name,enemy_hp,enemy_max_hp,enemy_attack)
            self.stages.pop(self.current_stage_selection)
            print("kita?")
            self.game_state= "game"
            
    
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
    
    def draw_stage_detail(self,stages):
        stages_dict =self.stages_details[stages]
        stages_detail =stages_dict["ギミック"]
        x,y =190,220
        width, height =140,50
        pyxel.rect(x, y, width, height, 7)  # 白い背景
        self.font.draw_text(x + 35, y + 5, stages_detail, 0)  # 黒いテキスト
        self.font.draw_text(x + 5,y + 5,"内容:",0)
        
    

# ゲームを開始
TypingGame()
