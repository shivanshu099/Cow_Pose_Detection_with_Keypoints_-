🐄 Cow Pose Detection with Keypoints

This project focuses on pose estimation for cows by labeling anatomical keypoints. The labeled dataset can be used to train keypoint detection models (e.g., YOLOv8 Pose, HRNet, or DeepLabCut) for applications like posture analysis, lameness detection, weight estimation, and behavior monitoring.

✨ Keypoints Definition

We define 14–16 anatomical landmarks that represent the cow’s body structure:

Head Region

Nose (snout tip)

Left ear base

Right ear base

Neck & Shoulder

Withers (shoulder top / highest spine point)

Torso

Chest point (base of neck, between front legs)

Mid-back / spine midpoint

Hip point (center of hip bone)

Forelimbs

Left front knee

Right front knee

Left front hoof

Right front hoof

Hindlimbs

Left hind knee (stifle)

Right hind knee

Left hind hoof

Right hind hoof

Back End

Tail base

Rump pin bone (rear hip pin)

📌 Annotation Guidelines

Use a consistent order of labeling (same index for same keypoint across all images).

Place keypoints on visible joints/landmarks.

If a keypoint is occluded, still annotate it approximately (if possible).

Save labels in COCO format or YOLO Pose format for training.

🛠️ Tools for Labeling

Label Studio

CVAT

Roboflow Annotate

🚀 Training Models

You can train models like:

YOLOv8 Pose (Ultralytics)

HRNet

DeepLabCut (commonly used for animal pose estimation)

Example (YOLOv8 Pose):

yolo pose train data=cow_keypoints.yaml model=yolov8n-pose.pt epochs=100 imgsz=640

Automated lameness detection

Body condition scoring

Gait & movement analysis

Livestock monitoring systems

🙌 Acknowledgments

Inspired by existing animal pose estimation research and adapted to cattle anatomy.


#screenshots



![classification_model](https://github.com/shivanshu099/Cow_Pose_Detection_with_Keypoints_-/blob/main/Screenshot%202025-09-28%20000325.png)
