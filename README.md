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


#screenshots



![classification_model](https://github.com/shivanshu099/Cow_Pose_Detection_with_Keypoints_-/blob/main/Screenshot%202025-09-28%20000325.png)
