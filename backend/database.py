import sqlite3, os

DB_FILE = 'ankle.db'
# 如果已有就删掉重建，方便演示
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
# 用户表
conn.execute('''
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pwd TEXT NOT NULL,
    age INTEGER
);
''')
# 视频/评估表
conn.execute('''
CREATE TABLE videos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    path TEXT,
    score INTEGER,
    risk TEXT,
    advice TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
conn.close()
print('✅ 数据库 ankle.db 初始化完成')
