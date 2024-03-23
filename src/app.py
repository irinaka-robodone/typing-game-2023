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
    def __init__(self, name: str, hp: int, max_hp: int, attack,stage_damage:int,heal :int):
        self.name = name
        self.current_hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.stage_damage = stage_damage
        self.heal = heal
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")

    def is_defeated(self):
        return self.current_hp <= 0

class Enemy(Character):
    def __init__(self, name, hp, max_hp,attack,stage_damage:int,heal ):
        super().__init__(name, hp ,max_hp,attack,stage_damage,heal )
        
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp=0
            print(f"{self.name} took {damage} damage! Current HP: {self.current_hp}")
        

class Player(Character):
    def __init__(self, name, hp, max_hp,attack,stage_damage:int,heal):
        super().__init__(name, hp,max_hp,attack,stage_damage,heal )
        
        

class TypingGame:
    def __init__(self):
        # ウィンドウのサイズとタイトルを設定
        self.SCREEN_SIZE = (500, 300)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])
        self.odai_list = ["typing","game","minecraft","python","the legend of zelda","splatoon","grand theft auto","google","logicool","steam","steelseries","apex legends","fortnite","subnautica","citys skyline","windows","wakka kimoti yosugi daro","nihon no tyuugakkou","robodann",""] 
        self.typed_word = ""
        self.is_correct = True
        # 他の初期化処理
        
        self.font_m = BDFRenderer("assets/font/b16.bdf")
        self.font_s = BDFRenderer("assets/font/b14.bdf")
        self.font_l = BDFRenderer("assets/font/b24.bdf")
        # ゲームの状態を管理する変数

        self.game_state = "title"
        
        self.characters = ["炎", "水", "雷", "闇", "光"]
        self.selected_character = None
        self.current_selection = 0
        self.character_details = {
        "炎":{"特徴":"熱い",  "HP":350,"Max_hp":350,"attack":10,"stage_damage":0 ,"heal":0}, 
        "水":{"特徴":"涼しい","HP":400,"Max_hp":400,"attack":8,"stage_damage":0 ,"heal":0},
        "雷":{"特徴":"速い",  "HP":310,"Max_hp":310,"attack":15,"stage_damage":0 ,"heal":0},
        "闇":{"特徴":"暗い",  "HP":360,"Max_hp":360,"attack":11,"stage_damage":0 ,"heal":0},
        "光":{"特徴":"眩しい","HP":370,"Max_hp":370,"attack":12,"stage_damage":0 ,"heal":0},
        }
        self.stages=["1","2","3","4","5"]
        self.selected_stage = None
        self.current_stage_selection = 0
        self.stages_details ={
        "1":{"ギミック":"スタンダード", "enemy_name": "カモノハシ","enemy_hp":540,"enemy_max_hp":540,"enemy_attack":10,"stage_damage":5,"heal":0},
        "2":{"ギミック":"スピード勝負","enemy_name":"トラ","enemy_hp":400,"enemy_max_hp":400,"enemy_attack":10,"stage_damage":15,"heal":0},
        "3":{"ギミック":"持久戦","enemy_name":"カメ","enemy_hp":800,"enemy_max_hp":750,"enemy_attack":10,"stage_damage":5,"heal":10},
        "4":{"ギミック":"自分との戦い","enemy_name":"人","enemy_hp":None,"enemy_max_hp":None,"enemy_attack":10,"stage_damage":5,"heal":0},
        "5":{"ギミック":"最後の戦い","enemy_name":"機械","enemy_hp":3000,"enemy_max_hp":3000,"enemy_attack":20,"stage_damage":10,"heal":11},
        }
        
        pyxel.load("assets/resource.pyxres")
        self.hp_decrease_interval = 1  # HPが減少する間隔（秒数）
        self.clear_stages = set()
        
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
            # self.game_state = "play"
        
        elif self.game_state == "select_stage":
            self.handle_stage_selection()
        
        elif self.game_state == "play":
            self.handle_input()
            if self.typed_word == self.current_word:
                self.update_odai()
            if self.enemy.current_hp == 0:
                self.game_state = "won"
            if self.player.current_hp == 0:
                self.game_state = "lose"
            print("stage damage:", self.enemy.stage_damage)
            current_time = time.time()
            if current_time - self.last_decrease_time >= self.hp_decrease_interval:
                self.player.take_damage(self.enemy.stage_damage)  # HPを1減少させる
                self.last_decrease_time = current_time
                
        if self.game_state == "won":
            clear_stages = list(self.clear_stages)
            clear_stages.append(self.selected_stage)
            self.clear_stages = set(clear_stages)
            
            if pyxel.btnp(pyxel.KEY_RETURN) :
                self.player.current_hp = self.player.max_hp
                self.player.current_hp =(self.player.current_hp + 35 )
                self.player.max_hp= (self.player.max_hp+ 35)
                self.player.attack = (self.player.attack + 15)
                self.game_state = "select_stage"
                print(self.clear_stages)
            else:
                pass
        if self.game_state == "lose":
            """"""

    def draw(self):
        pyxel.cls(0) # 画面をクリア
        # self.enemy.draw()
    
        # タイトル画面の描画
        if self.game_state == "title":
            pyxel.text(50, 40, "タイトル画面", 7)
            self.font_l.draw_text(200, 130, "タイピングゲーム", pyxel.frame_count % 16)
            self.font_m.draw_text(200, 160, "Enterを押して開始", pyxel.frame_count % 16)
        # ゲーム画面の描画（ここでは仮に設定）
        
        elif self.game_state == "select_character":
            # キャラクター選択画面の描画
            title = "1. プレイヤーを選べ"
            self.font_m.draw_text(20, 20, title, 7)
            pyxel.line(20, 40, 500, 40, 7)
            
            pos_x = 40
            pos_y = 80
            
            for i, character in enumerate(self.characters):
                color = 7 if i == self.current_selection else 6
                self.font_m.draw_text(pos_x + i * 100 ,pos_y , character, color )
                # pyxel.text(120, 10 + i * 10, character, color)
                
            selected_character = self.characters[self.current_selection]
            self.draw_character_detail(selected_character)
            
        elif self.game_state == "select_stage":
            title = "2. ステージを選べ"
            self.font_m.draw_text(20, 20, title, 7)
            pyxel.line(20, 40, 500, 40, 7)
            
            pos_x = 40
            pos_y = 80
            
            for i,stages in enumerate(self.stages):
                color = 7 if i ==self.current_stage_selection else 6
                self.font_m.draw_text(pos_x + i * 100, pos_y, stages,color)
            selected_stage = self.stages[self.current_stage_selection]
            self.draw_stage_detail(selected_stage)
            
        elif self.game_state == "play":
            # self.font_m.draw_text(50, 60, "ゲーム中...", 7)
            # pyxel.cls(0)
            pos_x = 20
            pos_y = 40
            
            word_length = len(self.current_word)
            
            self.font_m.draw_text(self.SCREEN_SIZE[0]//2 - word_length*12//4, 40, 
                                self.current_word, 7)
            
            word_bar_x = self.SCREEN_SIZE[0]//2 - word_length*12//4 - 10
            pyxel.line(word_bar_x, 60, word_bar_x + word_length*12//2 + 20, 60, 6)
            
            typed_word_length = len(self.typed_word)
            self.font_m.draw_text(self.SCREEN_SIZE[0]//2 - typed_word_length*12//4, 70, 
                                self.typed_word, 6 if self.is_correct else 8)
            
            pyxel.rect(5, 10, 200, 20, 7)
            pyxel.rect(7, 12, int(186 *self.player.current_hp/self.player.max_hp) , 16, 3)
            pyxel.rect(280,10,200,20,7)
            pyxel.rect(280,12,int(186*self.enemy.current_hp/self.enemy.max_hp),16,3)
            
            # self.font_m.draw_text(pos_x, pos_y, "プレイヤー", 7)
            self.font_m.draw_text(pos_x, pos_y + 30, f"{self.player.name}", 7)
            # self.font_m.draw_text(pos_x, self.SCREEN_SIZE[1] - 40, str(self.stages_details[self.selected_stage]), 7)
            hp = self.player.current_hp
            self.font_m.draw_text(90,100,str(hp),7)
            self.font_m.draw_text(48,100,"残りHP:",7)
            self.font_m.draw_text(400,100,str(self.enemy.current_hp),7)
            self.font_m.draw_text(400,70,self.enemy.name,7)
            self.font_m.draw_text(355,100,"残りHP:",7)
        elif self.game_state == "won":
            # 勝利画面の描画
            self.font_m.draw_text(190, 100, "W        I        N", pyxel.frame_count % 16)
            self.font_m.draw_text(190, 120, "Enterキーを押してね", pyxel.frame_count % 16)
            self.font_m.draw_text(45, 125, "レベルアップ!", pyxel.frame_count % 16)
            self.font_m.draw_text(50, 140, "attack 10↑", 7)
            self.font_m.draw_text(50, 155, "HP     35↑", 7)
            
        elif self.game_state == "lose":
            self.font_m.draw_text(170, 100, "L        O        S        E", pyxel.frame_count % 16)
        # if self.game_state == "select_character":
        # # キャラクターのリストを描画
        #     for i, character in enumerate(self.characters):
        #         color = 7 if i == self.current_selection else 6
        #         pyxel.text(10, 10 + i * 10, character, color)
                
        #     self.draw_character_detail(self.characters[self.current_selection])
        
        if self.clear_stages == {"1","2","3","4","5"} :
            self.game_state = "game_clear"
        if self.game_state =="game_clear":
            self.font_m.draw_text(120, 100, "G    A    M    E        C    L    E    A    R", pyxel.frame_count % 16)
    def handle_input(self):
        # if not self.is_correct:
        #     return
        
        # A-Z でどのキーが押されたかを調べるループ
        key_map = list(range(pyxel.KEY_A, pyxel.KEY_Z + 1))
        key_map.append(pyxel.KEY_SPACE)
        for key in key_map:
            # print(key)
            # もし、そのキーが押されていたら
            if pyxel.btnp(key):
                pyxel.play(0, 0, loop= False)
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
                        # self.enemy.take_damage(self.enemy.heal-10)

                    else:
                        pyxel.play(0, 1, loop= False)
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
            stage_damage = self.character_details[name]["stage_damage"]
            heal = self.character_details[name]["heal"]
            self.player = Player(name, hp,max_hp,attack,stage_damage,heal )
            self.game_state = "select_stage"
            self.last_decrease_time = time.time()
    
    def handle_stage_selection(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.current_stage_selection = max(0,self.current_stage_selection - 1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_stage_selection = min(len(self.stages) - 1,self.current_stage_selection + 1)
        elif pyxel.btnp(pyxel.KEY_RETURN):
            self.selected_stage = self.stages[self.current_stage_selection]
            stage_info = self.stages_details[self.selected_stage]
            if self.clear_stages != {"1","2","3","4"} and self.selected_stage == "5":
                return
            
            if self.selected_stage == "4":
                enemy_hp = self.player.current_hp
                enemy_max_hp = self.player.max_hp
            else:
                enemy_hp = stage_info["enemy_hp"]
                enemy_max_hp = stage_info["enemy_max_hp"]
            enemy_name = stage_info["enemy_name"]
            enemy_attack = stage_info["enemy_attack"]
            
            enemy_stage_damage = stage_info["stage_damage"]
            enemy_heal = stage_info["heal"]
            self.enemy = Enemy(enemy_name,enemy_hp,enemy_max_hp,enemy_attack,enemy_stage_damage,enemy_heal)
            self.stages.pop(self.current_stage_selection)
            print("kita?")
            self.update_odai()
            self.game_state= "play"
            
    
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
        self.font_m.draw_text(x + 5, y + 5, detail, 0)  # 黒いテキスト
        self.font_m.draw_text(x + 50,y + 5,"HP:",0)
        self.font_m.draw_text(x + 75,y + 5,str(hp),0)
        self.font_m.draw_text(x + 5, y + 20,"攻撃力:",0)
        self.font_m.draw_text(x + 60,y + 20,str(attack),0)
    
    def draw_stage_detail(self,stages):
        stages_dict =self.stages_details[stages]
        stages_detail =stages_dict["ギミック"]
        x,y =190,220
        width, height =140,50
        pyxel.rect(x, y, width, height, 7)  # 白い背景
        self.font_m.draw_text(x + 45, y + 5, stages_detail, 0)  # 黒いテキスト
        self.font_m.draw_text(x + 5,y + 5,"内容:",0)
        
    

# ゲームを開始
TypingGame()
