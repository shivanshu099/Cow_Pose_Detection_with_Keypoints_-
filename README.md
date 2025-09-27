# 🐄 Cow Pose Detection with Keypoints

This repository contains a pipeline for **cow pose/keypoint detection**: dataset labeling, model training, and a simple app (FastAPI backend + frontend) to run and visualize predictions.

**Highlights**
- Dataset labeled with **Roboflow Annotate**.  
- Model trained with **YOLOv8 Pose (Ultralytics)**.  
- Backend: **FastAPI** (serves model inference API).  
- Frontend: simple web UI (run with `npm run dev`).

---

## ✨ Keypoints (14–16 landmarks)

**Head**
- Nose (snout tip)  
- Left ear base  
- Right ear base

**Neck & Shoulder**
- Withers (highest spine point / shoulder top)

**Torso**
- Chest point (base of neck, between front legs)  
- Mid-back / spine midpoint  
- Hip point (center of hip bone)

**Forelimbs**
- Left front knee  
- Right front knee  
- Left front hoof  
- Right front hoof

**Hindlimbs**
- Left hind knee (stifle)  
- Right hind knee  
- Left hind hoof  
- Right hind hoof

**Back End**
- Tail base  
- Rump pin bone (rear hip pin)

---

## 📌 Annotation Guidelines

- Use a **consistent keypoint index/order** across all images.  
- Place keypoints on **visible joints/landmarks**.  
- If occluded, **approximate** the location as best as possible and mark visibility appropriately.  
- Export labels in **COCO** or **YOLO Pose** format for training.

---

## 🛠️ Tools

- **Roboflow Annotate** — labeling (used for this project)  
- **Ultralytics / YOLOv8** — training and inference  
- **Label Studio**, **CVAT** — alternatives

---

## 🚀 Training (example)

Train using Ultralytics YOLOv8 Pose after preparing `cow_keypoints.yaml` (dataset config):

## screenshots

![classification_model](https://github.com/shivanshu099/Cow_Pose_Detection_with_Keypoints_-/blob/main/Screenshot%202025-09-28%20000325.png)


## ⚡ Project Setup & Run Instructions

The project is split into `backend/` (FastAPI) and `frontend/` (web UI). The backend includes the inference code that loads your trained YOLOv8 pose model.

### Backend (FastAPI)

1.  Open a terminal and go to the backend folder:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    -   **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    -   **Windows (cmd):**
        ```bash
        .\venv\Scripts\activate
        ```
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the FastAPI service:
    ```bash
    # If main.py starts FastAPI on its own:
    python main.py

    # Or use uvicorn (recommended for development):
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

**Backend endpoints (examples)**
-   `POST /predict` — run pose inference on uploaded image
-   `GET /health` — health check
(Check backend code for exact route names.)

### Frontend

1.  Open a new terminal and go to the frontend folder:
    ```bash
    cd myapp
    ```
2.  Install node dependencies (if not already installed):
    ```bash
    npm install
    ```
3.  Start development server:
    ```bash
    npm run dev
    ```
4.  Open the UI in your browser (usually at `http://localhost:3000` or as printed by the dev server) and use it to upload images and view pose predictions from the backend.

---


---

## 🛠️ Tips & Troubleshooting

-   Ensure the backend and frontend URLs/ports match (CORS may need enabling in FastAPI).
-   Put your trained YOLOv8 weights in `backend/models/` and update the inference path in `main.py`.
-   If GPU inference is required, install PyTorch with CUDA matching your GPU and check Ultralytics docs.
-   For production, serve the model with a proper ASGI server (uvicorn/gunicorn) and consider batching requests.

---

## 🌟 Applications

-   Automated lameness detection
-   Body condition scoring
-   Gait & movement analysis
-   Integrated livestock monitoring systems

---

## 🙌 Acknowledgments

-   Dataset labeled with Roboflow
-   Model training with Ultralytics YOLOv8 Pose
-   Inspired by animal pose-estimation research and adapted for cattle anatomy

