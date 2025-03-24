import cv2
import numpy as np

class HeadPoseEstimator:
    def __init__(self):
        self.text = "Center"

    def head_pose(self, frame, results):
        """
        Estimates the head pose direction based on facial landmarks.

        Args:
        frame (np.array): The input image/frame where face landmarks are detected.
        results (mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList): Facial landmarks obtained from MediaPipe.

        Returns:
        str: The head pose direction (e.g., "Left", "Right", "Up", "Down", "Center").
        """
        img_h, img_w, Img_c = frame.shape
        face_3d = []
        face_2d = []

        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                # Define key facial landmarks (e.g., nose, eyes, etc.)
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        # Calculate 2D and 3D positions for the nose
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                    # Extract 2D coordinates for other landmarks
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

        # Convert to numpy arrays
        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        # Camera matrix for perspective projection
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                               [0, focal_length, img_w / 2],
                               [0, 0, 1]])

        # Distortion matrix (assuming no distortion)
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Solve for rotation and translation vectors using PnP
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

        # Rodrigues rotation to rotation matrix
        rmat, jac = cv2.Rodrigues(rot_vec)

        # Decompose the rotation matrix into Euler angles
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

        # Convert radians to degrees
        x = angles[0] * 360
        y = angles[1] * 360
        z = angles[2] * 360

        # Determine the head pose based on Euler angles
        if y < -10:
            self.text = "Left"
        elif y > 10:
            self.text = "Right"
        elif x < -18:
            self.text = "Down"
        elif x > 15:
            self.text = "Up"
        else:
            self.text = "Center"

        return self.text

# example usage

# ret, frame = camera.read()
# # Check if the frame is valid
# if not ret or frame is None:
#     return None, None, None, None, None, "End of video or error reading frame."
# # Flip and resize the frame for uniform input
# frame = cv2.flip(frame, 1)  # Flip the frame horizontally
# frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)  # Resize for uniform input

# rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# results = face_mesh.process(rgb_frame)

# head_pose_estimator = HeadPoseEstimator()
# head_direction = pose_estimator.head_pose(rgb_frame, results)
