import cv2
import mediapipe as mp

class PoseDetector():

    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True, enable_segmentation=False, 
                 smooth_segmentation=True, detectionCon=0.5, trackCon=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        # Initialize the MediaPipe pose solution
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.static_image_mode, 
                                     model_complexity=self.model_complexity, 
                                     smooth_landmarks=self.smooth_landmarks, 
                                     enable_segmentation=self.enable_segmentation, 
                                     smooth_segmentation=self.smooth_segmentation, 
                                     min_detection_confidence=self.detectionCon, 
                                     min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)
        
        # if results.pose_landmarks:
            # if draw:
            #     self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img, results

    def getPosition(self, img, results):
        lmList = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        img, results = detector.findPose(img)
        lmList = detector.getPosition(img, results)
        
        # Print landmark positions for testing
        if lmList:
            print(lmList)

        cv2.imshow("Image", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
