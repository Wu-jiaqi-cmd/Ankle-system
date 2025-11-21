import cv2, mediapipe as mp
print('OpenCV 版本:', cv2.__version__)
print('Mediapipe 版本:', mp.__version__)

mp_drawing = mp.solutions.drawing_utils
mp_pose    = mp.solutions.pose

cap = cv2.VideoCapture(0)   # 用摄像头
pose = mp_pose.Pose()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)
    if res.pose_landmarks:
        mp_drawing.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('test', frame)
    if cv2.waitKey(1) & 0xFF == 27: break   # ESC 退出

cap.release(); cv2.destroyAllWindows()
