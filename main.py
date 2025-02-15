import socket
import struct
import threading
import json
from database import DatabaseManager
from handler import AuthHandler
from handler import RequestDispatcher
from handler import StateSyncHandler
from handler import RoomPageHandler
from handler import ItemHandler
from handler import RoomHallHandler
from config import SERVER_HOST, SERVER_PORT
from request_type import RequestType

class Server:
    def __init__(self, host, port, request_dispatcher,rooms,already_logged_in_players):
        self.host = host
        self.port = port
        self.request_dispatcher = request_dispatcher
        self.rooms = rooms
        self.already_logged_in_players = already_logged_in_players

    # 添加发送消息的方法
    def send_message_with_length_prefix(self,conn, message):
        try:
            message = json.dumps(message)
            # 将消息编码为字节
            message_bytes = message.encode('utf-8')
            
            # 计算消息长度并转换为4字节长度前缀
            length_prefix = len(message_bytes).to_bytes(4, byteorder='little')
            
            # 将长度前缀和消息内容拼接
            full_message = length_prefix + message_bytes
            
            # 发送完整的消息
            conn.sendall(full_message)
        except Exception as e:
            print(f"发送消息失败: {e}")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server is running on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Connected by {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                client_thread.start()

    def handle_client(self, conn):
        try:
            players_to_rooms = {}  # 创建字典=>记录玩家名和房间号的映射
            with conn:
                while True:
                    try:
                        # Step 1: 接收长度前缀（4字节）
                        length_prefix = b""
                        while len(length_prefix) < 4:
                            chunk = conn.recv(4 - len(length_prefix))
                            if not chunk:
                                print("客户端已关闭连接")
                                break
                            length_prefix += chunk
                        
                        # 解析长度前缀为整数（小端序）
                        message_length = struct.unpack('<I', length_prefix)[0]
                        if message_length <= 0 or message_length > 1024 * 1024:  # 防止异常长度
                            raise ValueError(f"无效的消息长度: {message_length}")
                        
                        print (f"收到的消息长度:{message_length}")
                        # Step 2: 接收完整消息内容
                        buffer = b''
                        while len(buffer) < message_length:
                            chunk = conn.recv(message_length - len(buffer))
                            if not chunk:
                                raise ConnectionError("连接中断")
                            buffer += chunk
                        
                        # Step 3: 解析客户端的请求
                        request = buffer.decode('utf-8')
                        print(f"收到请求: {request}")

                        # 处理请求
                        response = self.request_dispatcher.dispatch(conn,request,players_to_rooms)

                        if response:
                        # 发送带长度前缀的响应
                            self.send_message_with_length_prefix(conn, response)
                    
                    except Exception as e:
                        print(f"Error: {e}") 
                        break
        finally:
            if players_to_rooms:
                # 获取第一个 key
                first_key_playerName = next(iter(players_to_rooms))
                # 获取第一个 value
                first_value_roomid = players_to_rooms[first_key_playerName]
                if first_value_roomid:#如果是空字符串""仍然会被判定为false
                    if first_key_playerName in self.rooms[first_value_roomid].players:
                        print(f"玩家 {first_key_playerName} 存在于房间 {first_value_roomid} 中")
                        request = {"messageType":9,"roomId":first_value_roomid,"playerName":first_key_playerName}
                        request = json.dumps(request)
                        print(f"玩家离线请求: {request}")
                        self.request_dispatcher.dispatch(conn,request,players_to_rooms)
                        print(f"清除离线玩家处理players_to_rooms完成{len(players_to_rooms)}")
                    else:
                        print(f"玩家 {first_key_playerName} 已经不在房间 {first_value_roomid} 中，可能被强制踢出")
                else:
                    print(f"玩家 {first_key_playerName} 没有在任何房间中，可能未进入任何房间或者自己退出房间")
                self.already_logged_in_players.remove(first_key_playerName)
                print(f"玩家 {first_key_playerName} 已经从登录玩家的集合中already_logged_in_players删除")
            else:
                print(f"用户 {conn} 没有登录")
            
            print(f"玩家 {conn} 连接断开")

# 程序入口
if __name__ == "__main__":

    already_logged_in_players = set()
    rooms = {}

    db_manager = DatabaseManager(already_logged_in_players)
    room_handler = RoomPageHandler(rooms,send_message_method=None)
    room_hall_handler = RoomHallHandler(rooms)
    state_sync_handler = StateSyncHandler(rooms)
    auth_handler = AuthHandler(db_manager)
    item_handler = ItemHandler(rooms)

    handlers = {
        
            RequestType.SYNC_STATE.value: (["conn", "request"],state_sync_handler.handle_sync_state),
            RequestType.SYNC_ANIMATION.value: (["conn", "request"],state_sync_handler.handle_sync_animation),
            RequestType.ITEM_INTERACTION.value: (["conn", "request"],item_handler.handle_item_interaction),

            RequestType.ROOM_CREATE.value: (["conn", "request","players_to_rooms"],room_handler.handle_room_create),
            RequestType.ROOM_JOIN_SELF.value: (["conn", "request","players_to_rooms"],room_handler.handle_room_join),
            RequestType.ROOM_LEAVE_SELF.value: (["request","players_to_rooms"],room_handler.handle_room_leave_self),
            RequestType.ROOM_LEAVE_OTHER.value: (["request"],room_handler.handle_room_leave_other),
            RequestType.ROOM_CHAT_CONTENT_SYNC.value:(["request"],room_handler.handle_room_chat_sync),
            RequestType.ROOM_REQUEST_ALL_ROOM.value : ([],room_hall_handler.request_all_room),
            RequestType.ROOM_REQUEST_ASSIGN_ROOM.value:(["request"],room_hall_handler.request_assgin_room),
  
            RequestType.REGISTER.value: (["request"],auth_handler.handle_register),
            RequestType.LOGIN.value: (["request","players_to_rooms"],auth_handler.handle_login),
            RequestType.CHANGE_PLAYER_HEAD_IMAGE.value:(["request"],auth_handler.handle_change_head_image)

    }

    request_dispatcher = RequestDispatcher(handlers)
    server = Server(SERVER_HOST, SERVER_PORT, request_dispatcher,rooms,already_logged_in_players)
    room_handler.send_message_method=server.send_message_with_length_prefix

    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        db_manager.close()