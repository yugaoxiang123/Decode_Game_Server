# 多人在线游戏服务器

这是一个基于Python Socket实现的多人在线游戏服务器，支持房间系统、状态同步、物品交互等功能。
本项目配合[Decode_Game_Client](https://github.com/yugaoxiang123/Decode_Game_Client)服务端使用。

## 功能特性

- 用户认证系统
  - 用户注册
  - 用户登录
  - 修改头像
  
- 房间系统
  - 创建房间
  - 加入房间
  - 离开房间（自己/他人）
  - 房间聊天
  - 房间列表查看
  - 指定房间查询
  
- 游戏功能
  - 状态同步
  - 动画同步
  - 物品交互
  
## 技术实现

- 使用TCP Socket实现网络通信
- 采用多线程处理多客户端连接
- 使用JSON格式进行数据传输
- 实现了消息长度前缀机制，确保消息完整性
- 采用请求分发器模式处理不同类型的请求
- 支持断线检测和自动清理

## 项目结构

```
├── main.py # 主程序入口
├── database.py # 数据库管理
├── handler/
│ ├── auth.py # 认证处理
│ ├── room.py # 房间处理
│ ├── state.py # 状态同步处理
│ ├── item.py # 物品交互处理
│ └── dispatcher.py # 请求分发器
├── config.py # 配置文件
└── request_type.py # 请求类型定义

## 核心组件

### Server类
- 负责管理TCP连接和客户端会话
- 实现消息的长度前缀机制
- 处理客户端断开连接的清理工作
- 管理房间和已登录玩家列表

### RequestDispatcher
处理以下类型的请求：
1. 状态同步相关
   - 游戏状态同步
   - 动画状态同步
   - 物品交互同步

2. 房间管理相关
   - 房间创建/加入/退出
   - 房间聊天
   - 房间列表查询

3. 用户认证相关
   - 注册/登录
   - 头像修改

## 消息格式

### 消息结构
1. 长度前缀：4字节（小端序）
2. 消息内容：JSON格式
## 数据库结构

### players 表

CREATE TABLE players (
id INT AUTO_INCREMENT PRIMARY KEY, -- 用户ID，自增主键
name VARCHAR(10) NOT NULL UNIQUE, -- 用户名，唯一
password VARCHAR(20) NOT NULL, -- 密码
phone VARCHAR(11), -- 电话号码
levels INT DEFAULT 0, -- 用户等级
avaterIndex INT DEFAULT 0 -- 头像索引
);

字段说明：
- `id`: 用户唯一标识符
- `name`: 用户名（最大10个字符）
- `password`: 用户密码（最大20个字符）
- `phone`: 手机号码
- `levels`: 用户等级，默认为0
- `avaterIndex`: 头像索引，默认为0
## 安装和配置

### 环境要求
- Python 3.x
- MySQL数据库

### 依赖安装
pip install -r requirements.txt

### 服务器配置
SERVER_HOST = "localhost"
SERVER_PORT = 8888
### 数据库配置
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database"

## 特殊功能实现

### 消息类型
- 1: 用户注册
- 2: 用户登录
- 3: 创建房间
- 4: 加入房间
- 5: 离开房间
- 6: 状态同步
- 7: 动画同步
- 8: 物品交互
- 9: 房间聊天

### 断线处理机制
1. 检测客户端断开连接
2. 自动清理断线玩家的房间状态
3. 通知房间内其他玩家
4. 从已登录玩家集合中移除

### 房间管理系统
1. 动态房间创建和销毁
2. 房间状态实时同步
3. 支持多人同时在线
4. 房间聊天功能
5. 支持查看所有房间和指定房间

### 安全机制
1. 防止重复登录
2. 消息长度验证（限制1MB）
3. 基本的异常处理
4. 用户名和密码长度限制
