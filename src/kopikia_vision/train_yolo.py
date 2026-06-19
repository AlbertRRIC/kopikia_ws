#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / 'assets'
MODEL_DIR = PROJECT_ROOT / 'model'


def setup_classification_dataset():
    dataset_dir = PROJECT_ROOT / 'dataset'
    train_dir = dataset_dir / 'train'
    val_dir = dataset_dir / 'val'

    for d in [train_dir, val_dir]:
        for class_name in ['cup1', 'cup2']:
            (d / class_name).mkdir(parents=True, exist_ok=True)

    for class_name in ['cup1', 'cup2']:
        src_dir = ASSETS_DIR / class_name
        if not src_dir.exists():
            continue

        images = sorted([f for f in src_dir.iterdir() if f.is_file()])
        split = max(1, int(len(images) * 0.8))
        train_images = images[:split]
        val_images = images[split:]

        for img in train_images:
            shutil.copy2(img, train_dir / class_name / img.name)
        for img in val_images:
            shutil.copy2(img, val_dir / class_name / img.name)

    yaml_content = f"""path: {dataset_dir}
train: train
val: val
names:
  0: cup1
  1: cup2
nc: 2
"""
    yaml_path = dataset_dir / 'dataset.yaml'
    yaml_path.write_text(yaml_content)
    print(f"Dataset created at {dataset_dir}")
    sys.stdout.flush()


def train_model():
    setup_classification_dataset()

    dataset_yaml = PROJECT_ROOT / 'dataset' / 'dataset.yaml'
    model = YOLO(str(PROJECT_ROOT / 'model' / 'yolo11n-cls.pt'))
    model.train(
        data=str(dataset_yaml.parent),
        epochs=50,
        imgsz=224,
        batch=8,
        device='0',
        project=str(MODEL_DIR),
        name='cup_classifier',
        verbose=True
    )

    weights_dir = MODEL_DIR / 'cup_classifier' / 'weights'
    if weights_dir.exists():
        for pt_file in weights_dir.glob('*.pt'):
            shutil.copy2(pt_file, MODEL_DIR / pt_file.name)
            print(f"Model saved to {MODEL_DIR / pt_file.name}")
            sys.stdout.flush()
    else:
        print("Training completed but weights directory not found")


if __name__ == '__main__':
    train_model()
