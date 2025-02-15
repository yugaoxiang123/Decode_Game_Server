class Player:
    def __init__(self, name, conn,  avaterIndex, seat):
        self.name = name
        self.conn = conn
        self.avaterIndex = avaterIndex
        self.seat = seat

    def get_players_info(self):
        return [
            {"name": self.name, "seat": self.seat, "avaterIndex": self.avaterIndex}
        ]

class Room:
    def __init__(self, room_id, senceName, mapRank, roomOwner, max_players=4):
        self.room_id = room_id
        self.senceName = senceName
        self.mapRank = mapRank
        self.roomOwner=roomOwner
        self.max_players = max_players
        self.players = {}  # 存储玩家信息，键为玩家名称，值为 Player 对象
        self.available_seats = list(range(0, max_players))  # 初始化可用座位号

    def add_player(self, name, conn, avaterIndex):
        if name in self.players:
            raise ValueError(f"Player {name} is already in the room.")
        if len(self.players) >= self.max_players:
            raise ValueError("Room is full.")
        if not self.available_seats:
            raise ValueError("No seats available.")

        # 分配座位并添加玩家
        seat = self.available_seats.pop(0)
        self.players[name] = Player(name, conn, avaterIndex, seat)
        return seat

    def remove_player(self, player_name):
        if player_name not in self.players:
            raise ValueError(f"Player {player_name} is not in the room.")

        # 释放座位并移除玩家
        print("Removing player...")
        seat = self.players[player_name].seat
        self.available_seats.append(seat)
        self.available_seats.sort()  # 保持座位的有序性
        del self.players[player_name]
        print("Player removed.")
        
        # 如果被移除的玩家是房主，更新房主
        if player_name == self.roomOwner:
            if self.players:  # 如果还有其他玩家
                self.roomOwner = next(iter(self.players.values())).name  # 设置为第一个玩家
            else:
                print("Room is now empty, no owner.")
                self.roomOwner = None  # 可以选择将房主设置为 None 或其他处理逻辑
        return seat

    def is_empty(self):
        print(f"删除房间前测试玩家数量为{len(self.players)}")#测试玩家数量
        return len(self.players) <= 0

    def get_players_info(self, exclude=None):
        return [
            {"playerName": player.name, "seat": player.seat, "avaterIndex": player.avaterIndex}
            for player in self.players.values()
            if player.name != exclude
        ]
