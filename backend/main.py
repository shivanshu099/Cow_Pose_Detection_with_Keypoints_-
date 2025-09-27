from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import io
import cv2
import base64
from PIL import Image
from helper import body_clasification
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# 🔥 Enable CORS so frontend (5173) can talk to backend (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read and save uploaded file
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img_path = "temp.jpg"
    img.save(img_path)

    # Run classification (already returns JSON-safe types)
    metrics, scores, predict_img = body_clasification(img_path)

    # Convert predict_img to bytes
    if isinstance(predict_img, Image.Image):
        img_bytes = io.BytesIO()
        predict_img.save(img_bytes, format="JPEG")
        img_bytes = img_bytes.getvalue()
    elif isinstance(predict_img, (bytes, bytearray)):
        img_bytes = predict_img
    else:  # assume OpenCV (numpy array)
        _, buffer = cv2.imencode(".jpg", predict_img)
        img_bytes = buffer.tobytes()

    # Encode image as base64 for JSON
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Build response
    content = {
        "metrics": metrics,   # pure dict with float/int
        "scores": scores,     # pure dict with int
        "predict_img": img_base64
    }

    return JSONResponse(content=content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)





"""
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img_path = "temp.jpg"
    img.save(img_path)

    metrics, scores, predict_img = body_clasification(img_path)

    return {
        "metrics": metrics,
        "scores": scores
    }

"""



























