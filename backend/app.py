from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, os, uuid, shutil
from ai_real import calc_score
import os, uuid, datetime
app = Flask(__name__)
CORS(app)
UPLOAD = 'upload'
os.makedirs(UPLOAD, exist_ok=True)

def get_conn():
    return sqlite3.connect('ankle.db')

def db_run(sql, args=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    return cur.lastrowid

@app.post('/register')
def register():
    data = request.json
    try:
        uid = db_run("INSERT INTO users(username,pwd,age) VALUES(?,?,?)",
                     (data['u'], data['p'], data['a']))
        return jsonify({'uid': uid})
    except sqlite3.IntegrityError:
        return jsonify({'uid': 0, 'msg': '用户名已存在'})

@app.post('/login')
def login():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND pwd=?", (data['u'], data['p']))
    row = cur.fetchone()
    return jsonify({'uid': row[0] if row else 0})

@app.post('/upload')
def upload():
    file = request.files['video']
    user_id = request.form['uid']
    # 读取用户名
    conn = get_conn()
    user_row = conn.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
    username = user_row[0] if user_row else 'unknown'

    now = datetime.datetime.now()
    # 文件夹：upload/用户名/202511/21/
    sub_dir = os.path.join(username, now.strftime("%Y%m"), now.strftime("%d"))
    upload_dir = os.path.join(UPLOAD, sub_dir)
    os.makedirs(upload_dir, exist_ok=True)

    # 文件名：用户名_时分秒.mp4
    file_name = f"{username}_{now.strftime('%H%M%S')}.mp4"
    save_path = os.path.join(upload_dir, file_name)

    file.save(save_path)
    score, draw_path = calc_score(save_path)   # 画线视频也放在同一目录
    risk = '低' if score > 80 else '中' if score > 60 else '高'
    advice = {'低': '单脚站立 3×30 秒', '中': '弹力带脚踝外翻 3×15', '高': '建议线下就医'}[risk]
    db_run("INSERT INTO videos(user_id,path,score,risk,advice) VALUES(?,?,?,?,?)",
           (user_id, draw_path, score, risk, advice))
    return jsonify({'videoPath': draw_path, 'score': score, 'risk': risk, 'advice': advice})

@app.get('/history')
def history():
    uid = request.args.get('uid', type=int)
    conn = get_conn()
    rows = conn.execute(
        'SELECT score,risk,advice,upload_time FROM videos WHERE user_id=? ORDER BY upload_time DESC', (uid,)
    ).fetchall()
    return jsonify([{'score': r[0], 'risk': r[1], 'advice': r[2], 'time': r[3]} for r in rows])

# 让前端可以访问视频
@app.route('/upload/<path:filename>')   # 支持任意深度子目录
def uploaded_file(filename):
    return send_from_directory(UPLOAD, filename)

if __name__ == '__main__':
    if not os.path.exists('ankle.db'):
        os.system('python database.py')
    app.run(debug=True, port=5000)
