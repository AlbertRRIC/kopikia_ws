#!/usr/bin/env python3
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
MODEL_DIR = PROJECT_ROOT / 'model'
DATASET_DIR = PROJECT_ROOT / 'dataset'
#CONTINUE_SIGNAL_FILE = PROJECT_ROOT / '.continue_training'
CLASSIFICATION_SCRIPT = PROJECT_ROOT / 'train_yolo.py'
#DETECTION_SCRIPT = PROJECT_ROOT / 'train_yolo_det.py'



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



if __name__ == '__main__':
    main()
