import time
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path, desired_features=None):
        """
        Initializes the ObjectDetector with the YOLO model and desired features.

        Args:
        - model_path (str): Path to the YOLO model weights (default is 'yolov8s.pt').
        - desired_features (list): List of feature names to detect (default is person, book, cell phone).
        """

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(e)
        self.class_names = [
            "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
            "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
            "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
            "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
            "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
            "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
            "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
            "teddy bear", "hair drier", "toothbrush"
        ]
        self.desired_features = desired_features if desired_features else ["person", "book", "cell phone"]
        
        self.alert_timer = 0
        self.alert_triggered = False
        self.start_time = time.time()

    def detect_objects(self, ret, image):
        """
        Detects objects in the image and triggers an alert if the thresholds are exceeded.

        Args:
        - ret (bool): Whether the image is valid.
        - image (np.array): The input image/frame for object detection.

        Returns:
        - bool: Whether an alert is triggered (False) or not (True).
        """
        results = self.model.predict(image, device='cpu')
        count = [0] * len(self.desired_features)  # Initialize count for desired features

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])  # Get the class ID
                class_name = self.class_names[cls_id]

                if class_name in self.desired_features:
                    count[self.desired_features.index(class_name)] += 1  # Increment count for detected class

        # Calculate FPS based on time elapsed
        end = time.time()
        total_time = end - self.start_time
        fps = 1 / total_time if total_time > 0 else 0
        self.start_time = end

        # Trigger alert if thresholds are exceeded
        if count[0] > 1 or count[1] > 0 or count[2] > 0:
            self.alert_timer += 1
            if self.alert_timer > 15:
                self.alert_triggered = True
                self.alert_timer = 0
                return False  # Alert triggered
        return True  # No alert

# example usage

# detector = ObjectDetector(model_path='yolov8s.pt', desired_features=["person", "book", "cell phone"])

# ret, frame = camera.read()
# alert_status = detector.detect_objects(ret, frame)