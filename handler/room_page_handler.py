from request_type import RequestType
from property import Room
class RoomPageHandler:
    def __init__(self,rooms,send_message_method):
        self.rooms = rooms
        # self.players_to_rooms = players_to_rooms
        self.send_message_method = send_message_method

    def handle_room_create(self, conn, request ,players_to_rooms):
        print("执行handle_room_create")
        room_id = request["roomId"]
        playerName = request["playerName"]
        senceName = request["senceName"]
        mapRank = request["mapRank"]
        roomOwner = request["playerName"]
        avaterIndex = request.get("avaterIndex",0)

        if room_id in self.rooms:
            return {"success": False, "message": "房间号已存在请重新创建"}

        # 创建房间并添加第一个玩家
        room = Room(room_id,senceName,mapRank,roomOwner)
        self.rooms[room_id] = room
        seat = room.add_player(playerName, conn, avaterIndex)

        #新增玩家和房间号映射
        if players_to_rooms[playerName] != "":
            players_to_rooms[playerName] = ""
            print(f"键 '{playerName}' 已被删除.")
        players_to_rooms[playerName] = room_id 
        print(f"映射玩家处理players_to_rooms完成{len(players_to_rooms)}")

        room = self.rooms[room_id]
        print(f"创建房间时测试玩家数量为{len(room.players)}")#测试玩家数量
        print("执行handle_room_create完毕")
        return {
                "messageType": RequestType.ROOM_CREATE.value,
                "success":True,
                "roomId":room_id,
                "playerName":playerName,
                "avaterIndex":avaterIndex,
                "seat":seat,
                "senceName":senceName,
                "mapRank":mapRank,
                "roomOwner":roomOwner
                }

    def handle_room_join(self, conn, request,players_to_rooms):
        room_id = request["roomId"]
        playerName = request["playerName"]
        avaterIndex = request.get("avaterIndex",0)

        if room_id not in self.rooms:
            return {"success": False, "message": "该房间不存在"}

        room = self.rooms[room_id]
        try:
            seat = room.add_player(playerName, conn, avaterIndex)

            #新增玩家和房间号映射
            if players_to_rooms[playerName] != "":
                players_to_rooms[playerName] = ""
                print(f"键 '{playerName}' 已被删除.")
            players_to_rooms[playerName] = room_id 

        except ValueError as e:
            return {"success": False, "message": str(e)}
        senceName = room.senceName
        mapRank = room.mapRank
        roomOwner = room.roomOwner
        print(f"加入房间时测试玩家数量{len(room.players)}")#测试玩家数量
        # 通知其他玩家
        new_player_info = {
            "messageType": RequestType.ROOM_JOIN_OTHER.value,
            "playerName":playerName,
            "roomOwner":roomOwner,
            "avaterIndex":avaterIndex,
            "seat":seat,
            }
        

        self.broadcast_to_room(room_id, playerName, new_player_info)   
        # 同步已有玩家信息
        existing_players = {
            "messageType": RequestType.ROOM_JOIN_SELF.value,
            "success":True,
            "roomId":room_id,
            "senceName":senceName,
            "mapRank":mapRank,
            "playerName":playerName,
            "roomOwner":roomOwner,
            "avaterIndex":avaterIndex,
            "seat":seat,
            "roomAllPlayerInfos" : room.get_players_info(exclude=playerName)
        }
        return (existing_players)
    
    def handle_room_leave_self(self,request,players_to_rooms):
        print("执行handle_room_leave")
        room_id = request["roomId"]
        playerName = request["playerName"]

        if room_id not in self.rooms:
            return {"success": False, "message": "找不到该房间"}

        room = self.rooms[room_id]
        try:
            print(f"删除玩家开始时测试玩家数量为{len(room.players)}")#测试玩家数量
            seat = room.remove_player(playerName)
            print(f"删除玩家结束时测试玩家数量为{len(room.players)}")#测试玩家数量

            #新增玩家和房间号映射
            if players_to_rooms[playerName]!="":
                players_to_rooms[playerName] = ""
                print(f"players_to_rooms键 '{playerName}' 已被删除.")

        except ValueError as e:
            return {"success": False, "message": str(e)}
        
        # 如果房间为空，则删除房间
        if  room.is_empty():
            del self.rooms[room_id]
            print("删除房间完成")
            return {
            "messageType": RequestType.ROOM_LEAVE_SELF.value,
            "success": True,
            "message": f"你离开房间 {room_id}"}
        
        #新房主
        roomOwner = room.roomOwner
        # 通知其他玩家
        message = {
            "messageType": RequestType.ROOM_LEAVE_OTHER.value,
            "playerName": playerName,
            "seat": seat,
            "newRoomOwner":roomOwner,
            "message": f"玩家 {playerName} 离开房间 {room_id}"
        }
        self.broadcast_to_room(room_id, playerName, message)
        print("执行handle_room_leave完毕")
        return {
            "messageType": RequestType.ROOM_LEAVE_SELF.value,
            "success": True,
            "message": f"你离开房间 {room_id}"}

    def handle_room_leave_other(self,request):
        print("执行handle_room_leave")
        room_id = request["roomId"]
        playerName = request["playerName"]

        if room_id not in self.rooms:
            return {"success": False, "message": "找不到该房间"}

        room = self.rooms[room_id]

        send_to_leave_player_message = {
            "messageType": RequestType.ROOM_LEAVE_SELF.value,
            "success": True,
            "message": f"你被踢出房间，房间号为 {room_id}"}
        
        #先通知被踢出的玩家关闭房间页面
        print(f"Current players Key: {room.players.keys()}")
        print(f"Searching for playerName: {playerName}")
        player_conn = room.players[playerName].conn
        if player_conn:
            print("找到对应的player_conn")
        self.send_message_method(player_conn, send_to_leave_player_message)

        try:
            print(f"删除玩家开始时测试玩家数量为{len(room.players)}")#测试玩家数量
            seat = room.remove_player(playerName)
            print(f"删除玩家结束时测试玩家数量为{len(room.players)}")#测试玩家数量

        except ValueError as e:
            return {"success": False, "message": str(e)}
        
        # 如果房间为空，则删除房间
        if  room.is_empty():
            del self.rooms[room_id]
            print("删除房间完成")
            return {
            "messageType": RequestType.ROOM_LEAVE_SELF.value,
            "success": True,
            "message": f"你被踢出房间，房间号为 {room_id}"}
        
        #新房主
        roomOwner = room.roomOwner

        # 通知其他玩家，同步被踢出的玩家信息
        message = {
            "messageType": RequestType.ROOM_LEAVE_OTHER.value,
            "playerName": playerName,
            "seat": seat,
            "newRoomOwner":roomOwner,
            "message": f"玩家 {playerName} 被踢出房间 {room_id}"  
        }
        self.broadcast_to_room(room_id, playerName, message)
        print("执行handle_room_leave完毕")

    def handle_room_chat_sync(self,request):
        print("执行handle_room_chat_sync")
        room_id = request["roomId"]
        playerName = request["playerName"]
        message = request["message"]

        if room_id not in self.rooms:
            return {"success": False, "message": "找不到该房间"}

        if not message:
            return {"success": False, "message": "发送的消息为null"}
        
        # 通知其他玩家，同步被踢出的玩家信息
        message = {
            "messageType": RequestType.ROOM_CHAT_CONTENT_SYNC.value,
            "playerName": playerName,
            "message": message
        }
        self.broadcast_to_room(room_id, playerName, message)
        print("执行handle_room_leave完毕")

    def broadcast_to_room(self, room_id, sender, message):
        if room_id not in self.rooms:
            print(f"房间号 {room_id} 不存在")
            return

        room = self.rooms[room_id]
        for player_name, player in room.players.items():
            if player_name != sender:
                try:
                    self.send_message_method(player.conn, message)
                except Exception as e:
                    print(f"Failed to send message to {player_name}: {e}")

