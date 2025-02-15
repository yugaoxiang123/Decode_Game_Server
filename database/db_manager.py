import pymysql
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self,already_logged_in_players):
        self.connection = pymysql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        self.already_logged_in_players = already_logged_in_players
        print(f"DatabaseManager is running on {self.connection}")

    def register_user(self, name, password, phone):
        try:
            sql = "INSERT INTO players (name, password, phone) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (name, password, phone))
            self.connection.commit()
            return {"success": True, "message": "注册成功!"}
        except pymysql.MySQLError as e:
            return {"success": False, "message": str(e)}

    def login_user(self, name, password,players_to_rooms):
        try:
            if name in self.already_logged_in_players:
                return {"success": False, "message": "账号已经在别处登录!"}
            sql = "SELECT * FROM players WHERE name = %s AND password = %s"
            self.cursor.execute(sql, (name, password))
            user = self.cursor.fetchone()
            if user:
                self.already_logged_in_players.add(name)#记录玩家已经登录
                players_to_rooms[name]=""
                return {"success": True, "message": "登录成功!","name":user.get("name"), 
                        "levels": user.get("levels", 0),"avaterIndex": user.get("avaterIndex", 0)}
            else:
                return {"success": False, "message": "名字或者密码错误,未注册,请先注册账户!"}
        except pymysql.MySQLError as e:
            return {"success": False, "message": str(e)}
        
    def change_head_image(self, name, avaterIndex):
        try:
            # 查询用户是否存在
            sql_select = "SELECT * FROM players WHERE name = %s"
            self.cursor.execute(sql_select, (name,))
            user = self.cursor.fetchone()
            
            if user:
                # 更新头像索引
                sql_update = "UPDATE players SET avaterIndex = %s WHERE name = %s"
                self.cursor.execute(sql_update, (avaterIndex, name))
                self.connection.commit()
                print(f"更换头像成功{name}")
                return {"success": True, "message": "头像索引更新成功!", }
            else:
                return {"success": False, "message": "用户不存在，无法更新头像索引!"}
        except pymysql.MySQLError as e:
            return {"success": False, "message": str(e)}


    def close(self):
        self.cursor.close()
        self.connection.close()
