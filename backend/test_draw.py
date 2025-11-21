import cv2, mediapipe as mp, os
mp_drawing = mp.solutions.drawing_utils
mp_pose    = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)

video = r'F:\视频评估\subject01\主01.mp4'   # 一定写绝对路径
cap   = cv2.VideoCapture(video)
out_file = video.replace('.webm','_draw.webm')
fourcc = cv2.VideoWriter_fourcc(*'vp90')   # webm 编码
out = cv2.VideoWriter(out_file, fourcc, 30, (400,225))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame,(400,225))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)
    if res.pose_landmarks:
        mp_drawing.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    out.write(frame)

cap.release(); out.release()
print('画线完成 →', out_file)
