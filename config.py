import pymysql
# config.py
SERVER_HOST = "192.168.3.77"
SERVER_PORT = 12345
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "ygx_decode",
    "charset": "utf8mb4",
    "cursorclass":pymysql.cursors.DictCursor
}
