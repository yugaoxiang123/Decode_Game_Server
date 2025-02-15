import random
from request_type import RequestType
class RoomHallHandler:
    def __init__(self,rooms):
        self.rooms = rooms

    def request_all_room(self,count=10):
        # 获取所有房间的列表
        all_rooms = list(self.rooms.values())
        
        if not all_rooms:
            return {"success" : False,"message":"no room"}
        # 随机选择指定数量的房间
        random_rooms = random.sample(all_rooms, min(count, len(all_rooms)))
        
        room_list = []
        for room in random_rooms:
            room_info = {
                "roomId": room.room_id,
                "senceName": room.senceName,
                "mapRank": room.mapRank,
                "roomOwner": room.roomOwner,
                "currentRoomPlayers": len(room.players)
            }
            room_list.append(room_info)   
        return {"messageType":RequestType.ROOM_REQUEST_ALL_ROOM.value,
                "rooms": room_list}

    def request_assgin_room(self,request):
        room_id = request.get("roomId")

        # 检查 room_id 是否存在
        if room_id not in self.rooms:
            return {"success": False, "message": f"Room ID {room_id} does not exist."}

        # 获取房间信息
        room = self.rooms[room_id]
        return {
            "messageType": RequestType.ROOM_REQUEST_ASSIGN_ROOM.value,
            "roomId": room.room_id,
            "senceName": room.senceName,
            "mapRank": room.mapRank,
            "roomOwner": room.roomOwner,
            "currentRoomPlayers": len(room.players)
        }