#!/usr/bin/env python3
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
MODEL_DIR = PROJECT_ROOT / 'model'
DATASET_DIR = PROJECT_ROOT / 'dataset'
CONTINUE_SIGNAL_FILE = PROJECT_ROOT / '.continue_training'
CLASSIFICATION_SCRIPT = PROJECT_ROOT / 'train_yolo.py'
DETECTION_SCRIPT = PROJECT_ROOT / 'train_yolo_det.py'


def check_annotations_exist():
    train_labels = DATASET_DIR / 'train' / 'labels'
    val_labels = DATASET_DIR / 'val' / 'labels'

    if not train_labels.exists() or not val_labels.exists():
        return False

    train_files = list(train_labels.glob('*.txt'))
    val_files = list(val_labels.glob('*.txt'))

    if not train_files:
        return False

    for f in train_files + val_files:
        content = f.read_text().strip()
        if content and len(content.splitlines()) > 0:
            return True

    return False


def run_stage(stage_name, script_path):
    print(f"\n{'='*50}")
    print(f"Stage: {stage_name}")
    print(f"{'='*50}\n")
    sys.stdout.flush()

    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(line, end='')
        sys.stdout.flush()

    process.wait()

    if process.returncode != 0:
        print(f"ERROR: {stage_name} failed with exit code {process.returncode}")
        sys.exit(process.returncode)

    print(f"{stage_name} completed successfully.\n")
    sys.stdout.flush()


def main():
    print("Starting streamlined training pipeline...")
    sys.stdout.flush()

    run_stage("Classification Training", CLASSIFICATION_SCRIPT)

    if check_annotations_exist():
        print("Annotations already found in dataset/. Continuing to detection training...\n")
        sys.stdout.flush()
    else:
        print("\n" + "="*50)
        print("ACTION REQUIRED: Annotate images before detection training")
        print("="*50)
        print("\nAnnotation instructions:")
        print("1. Open LabelImg: labelimg")
        print(f"2. Open Dir: {DATASET_DIR / 'train' / 'images'}")
        print(f"3. Set save dir: {DATASET_DIR / 'train' / 'labels'}")
        print("4. For each image, draw a box around cup1 or cup2")
        print("5. Repeat for val/images -> val/labels/")
        print("\nYOLO format: class_id x_center y_center width height")
        print("Example: 0 0.512 0.634 0.281 0.420")
        print("="*50)
        sys.stdout.flush()
        print("\nPress Continue button in the app after annotating images...")
        sys.stdout.flush()
        
        while not CONTINUE_SIGNAL_FILE.exists():
            time.sleep(1)
        
        CONTINUE_SIGNAL_FILE.unlink()
        
        if not check_annotations_exist():
            print("\nERROR: No annotations found. Exiting.")
            sys.exit(1)

    run_stage("Detection Training", DETECTION_SCRIPT)

    print("\n" + "="*50)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Classification model: {MODEL_DIR / 'cup_classifier' / 'weights' / 'best.pt'}")
    print(f"Detection model: {MODEL_DIR / 'cup_detector' / 'weights' / 'best.pt'}")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
