import os
from datetime import datetime
import time
import asyncio

import cv2
import numpy as np
import torch
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
import modi
from PIL import Image

load_dotenv()
ip = os.environ.get("SERVER_IP") or "localhost"

app = FastAPI()
model = torch.hub.load('ultralytics/yolov5', 'custom', './best.pt')
bundle = modi.MODI()
motor1 = bundle.motors[0]
motor2 = bundle.motors[1]
ir = bundle.irs[0]

async def turn_left(x):
    if x > 20:
        motor1.speed = x,x
        motor2.speed = x,x
        await asyncio.sleep(0.5)
        motor1.speed = 0,0
        motor2.speed = 0,0
    else:
        motor1.speed = 25,25
        motor2.speed = 25,25
        await asyncio.sleep(0.1)
        motor1.speed = 0,0
        motor2.speed = 0,0

async def turn_right(x):
    if x > 20:
        motor1.speed = -x,-x
        motor2.speed = -x,-x
        await asyncio.sleep(0.5)
        motor1.speed = 0,0
        motor2.speed = 0,0
    else:
        motor1.speed = -40,-40
        motor2.speed = -40,-40
        await asyncio.sleep(0.1)
        motor1.speed = 0,0
        motor2.speed = 0,0

async def turn(xa, ya, xb, yb):
    print(xa, ya, xb, yb)
    center = (xa + xb) / 2
    diff = center - 320
    if diff > 15:
        await turn_right(abs(diff) * 0.174)
    elif diff < -15:
        await turn_left(abs(diff) * 0.174)

@app.get("/")
async def home(request: Request):

  return HTTPException(status_code=405)

def straight():
    motor1.speed = 80, -80
    motor2.speed = -80, 80
    # time.sleep(0.5)
    # motor1.speed = 0,0
    # motor2.speed = 0,0

@app.post("/")
async def detect(file: UploadFile = File(...)):

    print("Got request at: {}".format(datetime.now()))

    content = cv2.cvtColor(cv2.imdecode(np.fromstring(await file.read(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_RGB2BGR)
    #print(content)
    results = model(content)

    print("Got result at: {}".format(datetime.now()))
    max_conf = 0
    box = [320, 320, 320, 320]
    for entry in results.xyxy[0]:
        if entry[4] > max_conf:
            box = entry[:]

    xB = int(box[2])
    xA = int(box[0])
    yB = int(box[3])
    yA = int(box[1])
    if 640 - yB < 5:
        motor1.speed = 0,0
        motor2.speed = 0,0
    await turn(xA, yA, xB, yB)
    straight()
    print(f"### {ir.proximity}")
    if ir.proximity > 10:
        motor1.speed = 0,0
        motor2.speed = 0,0
        exit(0)
    cv2.rectangle(content, (xA, yA), (xB, yB), (0, 255, 0), 2)
    cv2.imshow('image', content)
    cv2.waitKey(1)

    json_results = results_to_json(results,model)
    
    return json_results


def results_to_json(results, model):
    return [
          {
          "class": int(pred[5]),
          "class_name": model.model.names[int(pred[5])],
          "bbox": [int(x) for x in pred[:4].tolist()],
          "confidence": float(pred[4]),
          }
        for pred in results.xyxy[0]
        ]


if __name__ == '__main__':
    import uvicorn
    
    app_str = 'server:app'
    uvicorn.run(app_str, host=ip, port=8000, workers=1)
