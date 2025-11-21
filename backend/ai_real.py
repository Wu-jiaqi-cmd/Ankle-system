import cv2, mediapipe as mp, numpy as np, os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

def calc_score(video_path: str):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step  = max(total // 60, 1)
    ang_list = []

    # 画线视频路径：原目录 + 原文件名 + _draw.mp4
    draw_path = video_path.replace('.mp4', '_draw.mp4').replace('.webm', '_draw.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'avc1')   # H.264
    out = cv2.VideoWriter(draw_path, fourcc, fps, (400, 225))

    for idx in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret: continue
        frame = cv2.resize(frame, (400, 225))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            heel  = np.array([lm[mp_pose.PoseLandmark.RIGHT_HEEL].x * 400,
                              lm[mp_pose.PoseLandmark.RIGHT_HEEL].y * 225])
            ankle = np.array([lm[mp_pose.PoseLandmark.RIGHT_ANKLE].x * 400,
                              lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y * 225])
            toe   = np.array([lm[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * 400,
                              lm[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * 225])
            ang = abs(np.degrees(np.arctan2(toe[1] - ankle[1], toe[0] - ankle[0]) -
                                  np.arctan2(heel[1] - ankle[1], heel[0] - ankle[0])))
            ang_list.append(ang)
            # 画骨架
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        out.write(frame)
    cap.release(); out.release()

    score = int(np.clip((40 - np.mean(ang_list)) / 40 * 100, 0, 100)) if ang_list else 70
    return score, draw_path

