import time
import cv2
import mediapipe as mp

class PerceptionInit:
    def __init__(self, camera, model_path="https://github.com/UmarBalak/ProctorVision/raw/refs/heads/main/yolov8s.pt"):
        """
        Initialize the PerceptionInit with camera and speech settings.

        Args:
        - camera: The camera object used for capturing frames.
        - use_speech (bool): Whether to speak the alerts (default is True).
        """
        from .head_pose_estimator import HeadPoseEstimator
        from .eye_tracker import EyeTracker
        from .object_detector import ObjectDetector

        self.camera = camera

        self.alerts = {
            "visibility": ["Attention: Your face is not visible to the camera."],
            "direction": ["Alert: It seems you are not facing the camera."],
            "object": ["Warning: An important object has been detected."]
        }

        # Variables for alert tracking
        self.start_time = time.time()
        self.change_dir_counter = 0
        self.dir_warning_counter = 0
        self.vis_warning_counter = 0
        self.warning_count = 0
        self.visibility_counter = 0

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

        self.head_pose_estimator = HeadPoseEstimator()
        self.eye_tracker = EyeTracker()
        self.object_detector = ObjectDetector(model_path=model_path)

    def track(self):
        """
        Process the captured frame from the camera and detect alerts based on visibility, direction, and objects.
        
        Returns:
        - tuple: Direction, head direction, FPS, object detection status, and alert message (if any).
        """
        ret, frame = self.camera.read()

        # Validate frame capture
        if not ret or frame is None:
            return None, None, None, None, "End of video or error reading frame."

        # Preprocessing the frame
        frame = cv2.flip(frame, 1)  # Flip horizontally
        frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)  # Resize
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to RGB for processing

        # Process for face landmarks
        results = self.face_mesh.process(rgb_frame)

        direction, head_direction = '', ''
        obj_d = True
        fps = 0

        # If face landmarks are detected
        if results.multi_face_landmarks:
            head_direction = self.head_pose_estimator.head_pose(rgb_frame, results)

            if head_direction in ["Center", "Up"]:
                eye_direction = self.eye_tracker.track_eye(ret, frame, rgb_frame, results)
                direction = eye_direction
            else:
                direction = head_direction

            # FPS calculation
            end = time.time()
            total_time = end - self.start_time
            fps = 1 / total_time if total_time > 0 else 0
            self.start_time = end

            # Monitor direction changes
            if direction in ["Right", "Left", "Up"]:
                self.change_dir_counter += 1
                if self.change_dir_counter > 20:
                    self.change_dir_counter = 0
                    self.dir_warning_counter += 1
                    self.warning_count += 1
                    return False, direction, head_direction, fps, obj_d, self.alerts["direction"][0]
                return True, direction, head_direction, fps, obj_d, None
            else:
                # Object detection
                obj_d = self.object_detector.detect_objects(ret, frame)
                if not obj_d:
                    return False, direction, head_direction, fps, obj_d, self.alerts["object"][0]
                return True, direction, head_direction, fps, obj_d, None
        else:
            # Handle no face detection case
            self.visibility_counter += 1
            if self.visibility_counter > 20:
                self.visibility_counter = 0
                self.change_dir_counter = 0
                self.vis_warning_counter += 1
                self.warning_count += 1
                return False, direction, head_direction, fps, obj_d, self.alerts["visibility"][0]
            return True, direction, head_direction, fps, obj_d, None
