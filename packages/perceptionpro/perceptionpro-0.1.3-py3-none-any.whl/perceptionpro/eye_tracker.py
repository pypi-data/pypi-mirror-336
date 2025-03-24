import mediapipe as mp

class EyeTracker:
    def __init__(self):
        self.frame_counter = 0
        self.CEF_COUNTER = 0
        self.TOTAL_BLINKS = 0
        self.eye_points = []

        # Initialize the MediaPipe face mesh solution
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)


    def landmarks_detection(self, img, results):
        """
        Detect face landmarks and return coordinates of the landmarks.

        Args:
            img (numpy.array): The image to process.
            results (object): The results from the face mesh processing.
            draw (bool): Whether to draw landmarks on the image.
        
        Returns:
            mesh_coord (list): List of tuples containing coordinates of landmarks.
        """
        img_height, img_width = img.shape[:2]
        mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]

        return mesh_coord

    def track_eye(self, ret, frame, rgb_frame, results):
        """
        Track the eye movement and return direction.

        Args:
            ret (bool): Boolean indicating whether to process the frame.
            frame (numpy.array): The current frame to process.
            rgb_frame (numpy.array): The RGB frame for MediaPipe processing.
            results (object): The results from the face mesh processing.
        
        Returns:
            direction (str): The gaze direction (Left, Right, or Center).
        """
        self.frame_counter += 1  # frame counter

        mesh_coords = self.landmarks_detection(frame, results)

        # Left and Right eye indices from the face mesh
        LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

        # Extract points for both eyes
        l_eye_pts = [mesh_coords[i] for i in LEFT_EYE]
        r_eye_pts = [mesh_coords[i] for i in RIGHT_EYE]
        print(f"extreme left of left: {l_eye_pts[8]}")
        print(f"extreme right of left: {l_eye_pts[0]}")

        # Get the frame height and width
        frame_h, frame_w, _ = frame.shape
        output = self.face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks

        center = (abs(l_eye_pts[8][0] - l_eye_pts[0][0]), abs(l_eye_pts[8][1] - l_eye_pts[0][1]))

        if landmark_points:
            landmarks = landmark_points[0].landmark
            # Get coordinates of the four points around the eye
            self.eye_points = [(int(landmarks[i].x * frame_w), int(landmarks[i].y * frame_h)) for i in range(474, 478)]
            # Unpack the four points

            if len(self.eye_points) == 4:
                x1, y1 = self.eye_points[0]
                x2, y2 = self.eye_points[1]
                x3, y3 = self.eye_points[2]
                x4, y4 = self.eye_points[3]

                # Calculate the center of the eye (average of the four points)
                center_x = (x1 + x2 + x3 + x4) // 4
                center_y = (y1 + y2 + y3 + y4) // 4

                center = (center_x, center_y)
                print(f"gaze points: {self.eye_points}")
                print(f"center: {center}")

        # Estimate the direction based on the eye positions
        direction = self.direction_estimator(l_eye_pts[0], l_eye_pts[8], center, 0.4, 0.25) # 0.4, 0.3
        return direction

    def direction_estimator(self, extreme_right_circle_left_eye, extreme_left_circle_left_eye, left_gaze_center, l_eye_threshold, r_eye_threshold):
        """
        Estimate the gaze direction based on eye position and gaze center.

        Args:
            extreme_right_circle_right_eye (tuple): The extreme right point of the right eye.
            extreme_left_circle_right_eye (tuple): The extreme left point of the right eye.
            left_gaze_center (tuple): The center point of the eye region.
            l_eye_threshold (float): Left eye threshold for detecting left gaze.
            r_eye_threshold (float): Right eye threshold for detecting right gaze.

        Returns:
            direction (str): The gaze direction ("Left", "Right", or "Center").
        """

        dist_gaze_and_leftOfLeft = extreme_left_circle_left_eye[0] - left_gaze_center[0]
        dist_gaze_and_rightOfLeft = left_gaze_center[0] - extreme_right_circle_left_eye[0]
        eye_width = extreme_left_circle_left_eye[0] - extreme_right_circle_left_eye[0]


        if dist_gaze_and_leftOfLeft < (eye_width * r_eye_threshold):
            direction = "Right"
        elif dist_gaze_and_rightOfLeft < (eye_width * l_eye_threshold):
            direction = "Left"
        else:
            direction = "Center"


        return direction

# example usage

# ret, frame = camera.read()
# # Check if the frame is valid
# if not ret or frame is None:
#     return None, None, None, None, None, "End of video or error reading frame."
# # Flip and resize the frame for uniform input
# frame = cv2.flip(frame, 1)  # Flip the frame horizontally
# frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)  # Resize for uniform input

# rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
# results = face_mesh.process(rgb_frame)

# eye_tracker = EyeTracker()
# direction = eye_tracker.track_eye(ret, frame, rgb_frame, results)
