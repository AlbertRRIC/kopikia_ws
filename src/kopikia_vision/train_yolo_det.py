#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).parent
MODEL_DIR = PROJECT_ROOT / 'model'
DATASET_DIR = PROJECT_ROOT / 'dataset'


def check_annotations_exist():
    train_labels = DATASET_DIR / 'train' / 'labels'
    val_labels = DATASET_DIR / 'val' / 'labels'

    if not train_labels.exists() or not val_labels.exists():
        return False

    train_files = list(train_labels.glob('*.txt'))
    val_files = list(val_labels.glob('*.txt'))

    if not train_files:
        return False

    has_content = False
    for f in train_files + val_files:
        content = f.read_text().strip()
        if content and len(content.splitlines()) > 0:
            has_content = True
            break

    return has_content


def convert_json_to_yolo_txt(json_path, img_path, class_id):
    """Parses LabelEditor JSON and returns YOLO formatted string."""
    try:
        
        data = json.loads(json_path.read_text())
        
        width = data.get('imageWidth')
        height = data.get('imageHeight')

        # Absolute safety fallback just in case a JSON is missing them
        if not width or not height:
            from PIL import Image
            with Image.open(img_path) as img:
                width, height = img.size

        yolo_lines = []
        
        # Check if the JSON structure contains shapes/rectangles
        # LabelEditor typically saves shapes in a list
        shapes = data.get('shapes', data.get('annotations', []))
        
        for shape in shapes:
            # Extract coordinates based on LabelEditor format [[x1, y1], [x2, y2]] 
            # or box dictionaries
            points = shape.get('points', [])
            if len(points) >= 2:
                x1, y1 = points[0]
                x2, y2 = points[1]
                
                xmin, xmax = min(x1, x2), max(x1, x2)
                ymin, ymax = min(y1, y2), max(y1, y2)
                
                # Normalize values between 0 and 1
                x_center = (xmin + xmax) / 2.0 / width
                y_center = (ymin + ymax) / 2.0 / height
                bbox_width = (xmax - xmin) / width
                bbox_height = (ymax - ymin) / height
                
                yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}")
                
        return "\n".join(yolo_lines)
    except Exception as e:
        print(f"Warning: Failed to parse JSON {json_path.name}: {e}")
        return ""


def setup_detection_dataset():
    train_dir = DATASET_DIR / 'train'
    val_dir = DATASET_DIR / 'val'

    for d in [train_dir, val_dir]:
        (d / 'images').mkdir(parents=True, exist_ok=True)
        (d / 'labels').mkdir(parents=True, exist_ok=True)

    # Class mappings
    class_map = {'cup1': 0, 'cup2': 1}

    for class_name, class_id in class_map.items():
        assets_dir = PROJECT_ROOT / 'assets' / class_name
        if not assets_dir.exists():
            continue

        images = sorted([f for f in assets_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        split = max(1, int(len(images) * 0.8))
        train_images = images[:split]
        val_images = images[split:]

        # Helper to process splits
        def process_split(image_list, target_dir):
            for img in image_list:
                shutil.copy2(img, target_dir / 'images' / img.name)
                label_name = img.stem + '.txt'
                json_name = img.stem + '.json'
                
                src_json = assets_dir / json_name
                label_path = target_dir / 'labels' / label_name
                
                # Check for LabelEditor JSON first
                if src_json.exists():
                    yolo_content = convert_json_to_yolo_txt(src_json, img, class_id)
                    label_path.write_text(yolo_content)
                else:
                    # Fallback to an empty file if no annotation exists
                    if not label_path.exists():
                        label_path.write_text('')

        process_split(train_images, train_dir)
        process_split(val_images, val_dir)

    yaml_content = f"""path: {DATASET_DIR}
train: train/images
val: val/images
nc: 2
names:
  0: cup1
  1: cup2
"""
    yaml_path = DATASET_DIR / 'dataset_det.yaml'
    yaml_path.write_text(yaml_content)
    print(f"Detection dataset successfully created and converted at {DATASET_DIR}")
    sys.stdout.flush()


def train_detection_model():
    setup_detection_dataset()

    if not check_annotations_exist():
        print("\nERROR: No valid bounding box annotations found in your dataset!")
        print("Please ensure you have drawn boxes using LabelEditor and the .json files are in your assets folders.")
        sys.stdout.flush()
        return

    dataset_yaml = DATASET_DIR / 'dataset_det.yaml'
    model = YOLO(str(PROJECT_ROOT / 'model' / 'yolo11n.pt'))
    model.train(
        data=str(dataset_yaml.parent),
        epochs=50,
        imgsz=224,
        amp=False,
        batch=4,
        workers=1,
        device='0',
        project=str(MODEL_DIR),
        name='cup_detector',
        cache=False,
        verbose=True
    )

    weights_dir = MODEL_DIR / 'cup_detector' / 'weights'
    if weights_dir.exists():
        for pt_file in weights_dir.glob('*.pt'):
            shutil.copy2(pt_file, MODEL_DIR / pt_file.name)
            print(f"Model saved to {MODEL_DIR / pt_file.name}")
            sys.stdout.flush()
    else:
        print("Training completed but weights directory not found")


if __name__ == '__main__':
    train_detection_model()