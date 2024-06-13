# Import the required packages
import numpy as np
import imutils
import sys
import cv2

# Define parameters
MODEL_PATH = r"C:\Users\USER\Desktop\Netro Projects\Uganda Expo\Virtual Security\resnet-34_kinetics.onnx"  # Specify path to your pre-trained model
CLASSES_PATH = r"C:\Users\USER\Desktop\Netro Projects\Uganda Expo\Virtual Security\Actions.txt"  # Specify path to your class labels file
DISPLAY = 1  # Set to 1 to display output frames
USE_GPU = 0  # Set to 1 to use GPU, otherwise 0 for CPU

# Load class labels
ACT = open(CLASSES_PATH).read().strip().split("\n")
SAMPLE_DURATION = 16
SAMPLE_SIZE = 112

# Load the Deep Learning model
print("Loading The Deep Learning Model For Human Activity Recognition")
gp = cv2.dnn.readNet(MODEL_PATH)

# Check if GPU will be used
if USE_GPU > 0:
    print("Setting preferable backend and target to CUDA...")
    gp.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    gp.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Access the webcam video stream
print("Accessing the video stream...")
vs = cv2.VideoCapture(0)  # 0 to use the default webcam
fps = vs.get(cv2.CAP_PROP_FPS)
print("Original FPS:", fps)

# Process frames
while True:
    frames = []
    originals = []

    for i in range(0, SAMPLE_DURATION):
        (grabbed, frame) = vs.read()
        if not grabbed:
            print("[INFO] No frame read from the stream - Exiting...")
            sys.exit(0)
        originals.append(frame)
        frame = imutils.resize(frame, width=400)
        frames.append(frame)

    blob = cv2.dnn.blobFromImages(frames, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE),
                                  (114.7748, 107.7354, 99.4750),
                                  swapRB=True, crop=True)
    blob = np.transpose(blob, (1, 0, 2, 3))
    blob = np.expand_dims(blob, axis=0)

    gp.setInput(blob)
    outputs = gp.forward()
    label = ACT[np.argmax(outputs)]

    for frame in originals:
        cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
        cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

        if DISPLAY > 0:
            cv2.imshow("Activity Recognition", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                vs.release()
                cv2.destroyAllWindows()
                sys.exit(0)
