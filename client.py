import cv2
import requests
from dotenv import load_dotenv

import time
import os

load_dotenv()
ip = os.environ.get("SERVER_IP")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
cap.set(cv2.CAP_PROP_FPS, 36)


def infer(i):
    ret, img = cap.read()
    if not ret:
        return
    
    img = cv2.rotate(img, cv2.ROTATE_180)
    retv, buf = cv2.imencode(".jpg", img)

    result = requests.post(f"http://{ip}:8000", files={'file': buf}).json()

    try:
        if result[0][0]['confidence'] > 0.7:
            cv2.imwrite(f"save{i}.jpg", img)
            print(i, result)
    except:
        pass


i = 0
while True:
    infer(i)
    time.sleep(1)
    i += 1