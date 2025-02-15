from enum import Enum

class RequestType(Enum):
    REGISTER = 0
    LOGIN = 1
    SYNC_STATE = 2  # 玩家状态同步
    SYNC_ANIMATION = 3  # 动画状态同步
    ITEM_INTERACTION = 4  # 物品交互
    ROOM_CREATE = 5  # 创建房间
    ROOM_JOIN_OTHER = 6  # 加入房间
    ROOM_JOIN_SELF = 7  # 加入房间
    ROOM_LEAVE_OTHER = 8  # 离开房间
    ROOM_LEAVE_SELF = 9  # 离开房间
    ROOM_REQUEST_ALL_ROOM = 10 #加载所有房间
    ROOM_REQUEST_ASSIGN_ROOM = 11 #加载指定房间
    CHANGE_PLAYER_HEAD_IMAGE = 12 #更换头像
    ROOM_CHAT_CONTENT_SYNC = 13 #同步房间内玩家聊天内容