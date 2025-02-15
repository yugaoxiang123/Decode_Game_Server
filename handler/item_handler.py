class ItemHandler:
    def __init__(self, rooms):
        """
        初始化处理器。
        :param rooms: 房间数据，格式为字典。
        """
        self.rooms = rooms

    def handle_item_interaction(self, request):
        """
        转发物品交互请求。
        :param request: 客户端发来的请求数据，包含房间 ID、玩家 ID 和交互信息。
        :return: 响应结果。
        """
        room_id = request["room_id"]
        player_id = request["player_id"]

        # 检查房间和玩家是否存在
        if room_id not in self.rooms or player_id not in self.rooms[room_id]["players"]:
            return {"success": False, "message": "Invalid room or player"}

        # 广播请求数据给同房间其他玩家
        for other_player in self.rooms[room_id]["players"]:
            if other_player != player_id:
                # 转发数据给其他玩家 (示例：打印消息，实际应发送到客户端)
                print(f"Broadcast to {other_player}: {request}")

        return {"success": True, "message": "Item interaction forwarded"}


# class ItemHandler:
#     def __init__(self, rooms, items):
#         """
#         初始化物品处理器。
#         :param rooms: dict，包含房间及其玩家信息的字典。
#         :param items: dict，包含物品及其状态信息的字典。
#         """
#         self.rooms = rooms
#         self.items = items

#     def handle_item_interaction(self, request):
#         """
#         处理物品交互。
#         :param request: dict，请求数据，包含 room_id, player_id, action, item_id, 等信息。
#         :return: dict，交互结果。
#         """
#         room_id = request.get("room_id")
#         player_id = request.get("player_id")
#         action = request.get("action")  # e.g., "pick", "drop", "use", "rotate"
#         item_id = request.get("item_id")
#         new_state = request.get("new_state")  # 用于物品的状态改变

#         # 验证房间和玩家是否有效
#         if room_id not in self.rooms or player_id not in self.rooms[room_id]["players"]:
#             return {"success": False, "message": "Invalid room or player"}

#         # 验证物品是否有效
#         if item_id not in self.items:
#             return {"success": False, "message": "Invalid item"}

#         # 根据 action 执行逻辑
#         if action == "pick":
#             print(f"Player {player_id} picked item {item_id} in room {room_id}")
#         elif action == "drop":
#             print(f"Player {player_id} dropped item {item_id} in room {room_id}")
#         elif action == "use":
#             print(f"Player {player_id} used item {item_id} in room {room_id}")
#         elif action == "rotate":
#             # 更新物品的旋转状态
#             self.items[item_id]["rotation"] = new_state
#             print(f"Player {player_id} rotated item {item_id} in room {room_id} to {new_state}")
#         elif action == "change_state":
#             # 更新物品的其他状态
#             self.items[item_id]["state"] = new_state
#             print(f"Player {player_id} changed state of item {item_id} to {new_state}")
#         else:
#             return {"success": False, "message": "Unknown action"}

#         # 广播物品状态更新给房间内其他玩家
#         for other_player in self.rooms[room_id]["players"]:
#             if other_player != player_id:
#                 print(f"Broadcast to {other_player}: {player_id} -> action: {action}, item: {item_id}, state: {new_state}")

#         return {"success": True, "message": f"Action {action} performed on item {item_id}"}
