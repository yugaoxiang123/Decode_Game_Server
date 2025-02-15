
class AuthHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager
            
   
    def handle_register(self,data):
        return self.db_manager.register_user(data["name"], data["password"], data["phone"])

    def handle_login(self,data,players_to_rooms):
        return self.db_manager.login_user(data["name"], data["password"],players_to_rooms)
    
    def handle_change_head_image(self ,data):
        return self.db_manager.change_head_image(data["playerName"],data["avaterIndex"])