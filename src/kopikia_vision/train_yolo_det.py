#!/usr/bin/env python3
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


def setup_detection_dataset():
    train_dir = DATASET_DIR / 'train'
    val_dir = DATASET_DIR / 'val'

    for d in [train_dir, val_dir]:
        (d / 'images').mkdir(parents=True, exist_ok=True)
        (d / 'labels').mkdir(parents=True, exist_ok=True)

    assets_dirs = [PROJECT_ROOT / 'assets' / class_name for class_name in ['cup1', 'cup2']]

    for class_name in ['cup1', 'cup2']:
        assets_dir = PROJECT_ROOT / 'assets' / class_name
        if not assets_dir.exists():
            continue

        images = sorted([f for f in assets_dir.iterdir() if f.is_file()])
        split = max(1, int(len(images) * 0.8))
        train_images = images[:split]
        val_images = images[split:]

        for img in train_images:
            shutil.copy2(img, train_dir / 'images' / img.name)
            label_name = img.stem + '.txt'
            label_path = train_dir / 'labels' / label_name
            if not label_path.exists():
                label_path.write_text('')
        for img in val_images:
            shutil.copy2(img, val_dir / 'images' / img.name)
            label_name = img.stem + '.txt'
            label_path = val_dir / 'labels' / label_name
            if not label_path.exists():
                label_path.write_text('')

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
    print(f"Detection dataset created at {DATASET_DIR}")
    sys.stdout.flush()


def train_detection_model():
    setup_detection_dataset()

    dataset_yaml = DATASET_DIR / 'dataset_det.yaml'
    model = YOLO(str(PROJECT_ROOT / 'model' / 'yolo11n.pt'))
    model.train(
        data=str(dataset_yaml),
        epochs=50,
        imgsz=640,
        batch=4,
        device='0',
        project=str(MODEL_DIR),
        name='cup_detector',
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
