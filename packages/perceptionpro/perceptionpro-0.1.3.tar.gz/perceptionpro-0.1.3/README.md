# PerceptionPro

**PerceptionPro** is a Python package designed for real-time monitoring and alert systems. It provides modular components for head pose estimation, eye tracking, and object detection, all integrated into a cohesive alert system.

## Features
* **Head Pose Estimation:** Tracks the orientation of the user's head in real-time, providing insights into the direction of attention.

* **Eye Tracking:** Detects and analyzes eye movements and gaze direction, ensuring effective focus monitoring.

* **Object Detection:** Identifies objects in the environment, supporting compliance and situational awareness.

* **Alert System:** Integrated mechanism to trigger alerts based on configurable thresholds for head pose, eye tracking, and object detection.


## Installation

```bash
pip install perceptionpro
```

## Components

**1. Head Pose Estimation:**

* Module: `HeadPoseEstimator`

* Uses facial landmarks to determine the orientation of the user's head (e.g., Left, Right, Up, Down, Center).

**2. Eye Tracking:**

* Module: `EyeTracker`

* Tracks eye movements and gaze direction for applications like focus monitoring and attention analysis.

**3. Object Detection:**

* Module: `ObjectDetector`

* Leverages the YOLO model to identify and count objects such as person, book, and cell phone in real-time.

**4. Alert System:**

* Threshold-based system to monitor head pose, eye tracking, and detected objects, triggering alerts when defined criteria are met.

## Usage
```python
import cv2
import time
import keyboard 
from perceptionpro.core import PerceptionInit

def main():
    """
    Main function to initialize the camera, process video frames,
    and handle user input to quit.
    """
    try:
        # Initialize the camera
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Error: Camera could not be opened.")
            return
        else:
            print("Camera opened successfully.")

        # Initialize the PerceptionInit with speech enabled
        vision = PerceptionInit(camera, model_path="https://github.com/UmarBalak/ProctorVision/raw/refs/heads/main/yolov8s.pt")

        # Initialize variables
        violation_count = 0
        prev_time = time.time()

        while True:
            # Capture frame-by-frame
            ret, frame = camera.read()

            if not ret:
                print("Failed to capture video. Check your camera connection.")
                break

            # Calculate frame rate
            current_time = time.time()
            elapsed_time = current_time - prev_time
            fps = 1 / elapsed_time if elapsed_time > 0 else 0
            prev_time = current_time

            # Process frame metrics
            result, eye_d, head_d, fps, obj_d, alert_msg = vision.track()
            print("Procesed")

            if not result:
                violation_count += 1
                print(f"Warning: {violation_count} - {alert_msg}")

                if violation_count == 4:
                    print("The exam has been terminated.")
                    break
            else:
                pass
                # Print real-time metrics to console
                print(f"FPS: {fps:.2f}")
                print(f"Eye Direction: {eye_d}")
                print(f"Head Direction: {head_d}")
                print(f"Background: {'Ok' if obj_d else 'Object detected'}")

            # Check if 'q' is pressed to exit the loop
            if keyboard.is_pressed('q'):
                print("User requested to stop the process.")
                break

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Always release the camera and close windows
        if 'camera' in locals() and camera.isOpened():
            camera.release()
        print("Camera released. Process complete.")

if __name__ == "__main__":
    main()

```