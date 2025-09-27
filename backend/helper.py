from ultralytics import YOLO
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image



# ✅ Keypoints mapping from your cow_keypoints.yaml
KEYPOINTS = {
    0: "head",
    1: "withers",
    2: "hip_point",
    3: "tail_base",
    4: "rump_pin",
    5: "chest",
    6: "neck",
    7: "middle_hip"
}




#__________________________________________________score_calculator_______________________


def score_trait(value, trait):
    """
    Assigns classification score (1-9) based on value ranges.
    You should refine thresholds based on dataset or domain expert rules.
    """
    if trait == "body_length":
        if value < 80: return 3
        elif value < 100: return 5
        elif value < 120: return 7
        else: return 9

    elif trait == "chest_depth":
        if value < 50: return 3
        elif value < 70: return 5
        elif value < 90: return 7
        else: return 9

    elif trait == "neck_length":
        if value < 40: return 3
        elif value < 60: return 5
        elif value < 80: return 7
        else: return 9

    elif trait == "rump_angle":
        # Ideal rump angle ~ 110–130° (example range)
        if value < 100: return 3
        elif value < 110: return 5
        elif value < 130: return 7
        else: return 9

    return 0  # fallback





#___________________________________________________________Measurement & Visualization Function_________________________________






def analyze_cow(kpts,ref_length_cm=100, ref_kpts=(4,0)):
    """
    Analyze cow body structure using YOLO pose keypoints.
    Args:
        ref_length_cm (float): Real-world reference length in cm (default: rump_pin → head ≈ 100 cm)
        ref_kpts (tuple): Tuple of two keypoint indices used for scale calibration (default: rump_pin=4, head=0)
    Returns:
        dict with body_length, chest_depth, neck_length, rump_angle (in cm/deg)
    """


    # --- Calibration: px → cm ---
    ref_length_px = np.linalg.norm(kpts[ref_kpts[0]] - kpts[ref_kpts[1]])
    scale = ref_length_cm / ref_length_px   # cm per pixel

    # --- Compute measurements ---
    body_length_px = np.linalg.norm(kpts[4] - kpts[0])  # rump_pin → head
    chest_depth_px = np.linalg.norm(kpts[1] - kpts[5])  # withers → chest
    neck_length_px = np.linalg.norm(kpts[1] - kpts[6])  # withers → neck

    # Rump angle (at tail_base between rump_pin and hip_point)
    v1 = kpts[4] - kpts[3]   # rump_pin → tail_base
    v2 = kpts[2] - kpts[3]   # hip_point → tail_base
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    rump_angle_deg = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    # --- Convert to cm ---
    metrics = {
        "body_length (cm)": body_length_px * scale,
        "chest_depth (cm)": chest_depth_px * scale,
        "neck_length (cm)": neck_length_px * scale,
        "rump_angle (deg)": rump_angle_deg
    }
    # --- classification scores ---
    scores = {
        "body_length_score": score_trait(body_length_px*scale, "body_length"),
        "chest_depth_score": score_trait(chest_depth_px*scale, "chest_depth"),
        "neck_length_score": score_trait(neck_length_px*scale, "neck_length"),
        "rump_angle_score": score_trait(rump_angle_deg, "rump_angle")
    }


    return metrics,scores



#_____________________________________________________visualizer________________________________________________




def visualizer(img_path,kpts,metrics):
    # --- Visualization ---
    img = cv2.imread(img_path)

    # Draw keypoints
    for i, (x, y) in enumerate(kpts):
        cv2.circle(img, (int(x), int(y)), 5, (0,255,0), -1)
        cv2.putText(img, KEYPOINTS[i], (int(x)+5, int(y)-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    # Draw measurement lines + labels
    def draw_measure(p1, p2, label, value, unit, color=(255,0,0)):
        x1,y1 = int(p1[0]), int(p1[1])
        x2,y2 = int(p2[0]), int(p2[1])
        cv2.line(img, (x1,y1), (x2,y2), color, 2)
        midx, midy = (x1+x2)//2, (y1+y2)//2
        cv2.putText(img, f"{label}: {value:.1f}{unit}", (midx+10, midy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Draw lines for each metric
    draw_measure(kpts[4], kpts[0], "Body", metrics["body_length (cm)"], "cm", (255,0,0))
    draw_measure(kpts[1], kpts[5], "Chest", metrics["chest_depth (cm)"], "cm", (0,255,0))
    draw_measure(kpts[1], kpts[6], "Neck", metrics["neck_length (cm)"], "cm", (0,165,255))

    # Show rump angle at tail_base
    tb = kpts[3].astype(int)
    cv2.putText(img, f"Rump angle: {metrics['rump_angle (deg)']:.1f}°",
                (tb[0]+20, tb[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    # Convert BGR→RGB for plotting
    #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #plt.figure(figsize=(10,8))
    #plt.imshow(img_rgb)
    #plt.axis("off")
    #plt.show()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img =  Image.fromarray(img_rgb)
    return pil_img


# --- Example Usage ---

def to_python_type(obj):
    """Convert numpy types to pure Python types (recursively)."""
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: to_python_type(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_python_type(v) for v in obj]
    return obj



# Load model and run prediction
model_path="best.pt"
#img_path = "cow_1.jpg"   # change to your cow image
model = YOLO(model_path)

def body_clasification(img_path):
    results = model(img_path)[0]
    kpts = results.keypoints.xy.cpu().numpy()[0]  # (8, 2)
    metrics,score_trait_classification= analyze_cow(kpts)
    metrics=to_python_type(metrics)
    score_trait_classification=to_python_type(score_trait_classification)
    predict_img=visualizer(img_path,kpts,metrics)
    #print(metrics)
    #print(score_trait_classification)
    return metrics,score_trait_classification,predict_img




















