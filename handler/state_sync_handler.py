class StateSyncHandler:
    def __init__(self, rooms):
        """
        初始化状态同步处理器。
        :param rooms: dict，包含房间及其玩家信息的字典。
        """
        self.rooms = rooms

    def handle_sync_state(self, request):
        """
        同步玩家的位置信息和旋转信息。
        :param request: dict，请求数据，包含 room_id, player_id, position, rotation。
        :return: dict，同步结果。
        """
        room_id = request.get("room_id")
        player_id = request.get("player_id")
        position = request.get("position")
        rotation = request.get("rotation")

        # 验证房间和玩家是否有效
        if room_id not in self.rooms or player_id not in self.rooms[room_id]["players"]:
            return {"success": False, "message": "Invalid room or player"}

        # 广播状态更新给房间内其他玩家
        for other_player in self.rooms[room_id]["players"]:
            if other_player != player_id:
                # 示例广播
                print(f"Broadcast to {other_player}: {player_id} -> pos: {position}, rot: {rotation}")

        return {"success": True, "message": "State synchronized"}

    def handle_sync_animation(self, request):
        """
        同步玩家的动画状态。
        :param request: dict，请求数据，包含 room_id, player_id, animation_state。
        :return: dict，同步结果。
        """
        room_id = request.get("room_id")
        player_id = request.get("player_id")
        animation_state = request.get("animation_state")

        # 验证房间和玩家是否有效
        if room_id not in self.rooms or player_id not in self.rooms[room_id]["players"]:
            return {"success": False, "message": "Invalid room or player"}

        # 广播动画状态更新给房间内其他玩家
        for other_player in self.rooms[room_id]["players"]:
            if other_player != player_id:
                # 示例广播
                print(f"Broadcast to {other_player}: {player_id} -> anim: {animation_state}")

        return {"success": True, "message": "Animation synchronized"}
