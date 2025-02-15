import json

class RequestDispatcher:
    def __init__(self, handlers):
        """
        初始化请求分发器。
        :param handlers: dict，键是 messageType，值是 (required_params, handler) 的元组。
        """
        self.handlers = handlers

    def dispatch(self, conn, request,players_to_rooms):
        """
        分发请求到对应的处理器。
        :param conn: socket 对象，用于客户端连接。
        :param request: str，JSON 格式的请求字符串。
        :return: dict，包含 success 和 message 的响应。
        """
        try:
            # 将请求字符串解析为 JSON 对象
            request_data = json.loads(request)

            # 获取消息类型
            message_type = request_data.get("messageType")
            if message_type is None:  # 明确检查 None
                #淘汰的写法因为 if not message_type:的值为0时 if条件会触发
                return {"success": False, "message": "Missing messageType in request"}

            # 根据消息类型找到处理器
            handler_entry = self.handlers.get(message_type)
            if not handler_entry:
                return {"success": False, "message": f"Unknown messageType: {message_type}"}

            required_params, handler = handler_entry

            # 构造调用参数
            args = []
            if "conn" in required_params:
                args.append(conn)
            if "request" in required_params:
                args.append(request_data)
            if "players_to_rooms" in required_params:
                args.append(players_to_rooms)
            print(f"[INFO] 找到 messageType: {message_type} with handler: {handler.__name__}")

            # 调用处理器并返回结果
            return handler(*args)

        except json.JSONDecodeError:
            # JSON 解析错误
            return {"success": False, "message": "Invalid JSON format"}
        except Exception as e:
            # 捕获其他异常并返回错误信息，同时记录日志
            print(f"[ERROR] Exception while dispatching: {str(e)}")
            return {"success": False, "message": f"Server error: {str(e)}"}
