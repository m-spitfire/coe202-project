from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from PIL import Image
from io import BytesIO
import os

import torch

load_dotenv()
ip = os.environ.get("SERVER_IP") or "localhost"

app = FastAPI()

@app.get("/")
async def home(request: Request):

  return HTTPException(status_code=405)


@app.post("/")
async def detect(file: UploadFile = File(...)):

    model = torch.hub.load('ultralytics/yolov5', 'custom', './best.pt')

    results = model(Image.open(BytesIO(await file.read())))

    json_results = results_to_json(results,model)
    return json_results


def results_to_json(results, model):
    return [
        [
          {
          "class": int(pred[5]),
          "class_name": model.model.names[int(pred[5])],
          "bbox": [int(x) for x in pred[:4].tolist()],
          "confidence": float(pred[4]),
          }
        for pred in result
        ]
      for result in results.xyxy
      ]


if __name__ == '__main__':
    import uvicorn
    
    app_str = 'server:app'
    uvicorn.run(app_str, host=ip, port=8000, reload=True, workers=1)
