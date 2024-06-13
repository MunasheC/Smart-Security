import cv2
import os
import time
from datetime import datetime
from PoseModule import PoseDetector
import requests

def isHandRaised(lmList):
    # Check if a hand is raised by comparing y-coordinates of wrist and shoulder
    if lmList:
        left_wrist_y = lmList[15][2]  # Left wrist landmark index
        left_shoulder_y = lmList[11][2]  # Left shoulder landmark index
        right_wrist_y = lmList[16][2]  # Right wrist landmark index
        right_shoulder_y = lmList[12][2]  # Right shoulder landmark index
        
        if left_wrist_y < left_shoulder_y or right_wrist_y < right_shoulder_y:
            return True
    return False

ESP32_IP = "http://192.168.137.208"  # Replace with the IP address of your ESP32

def send_command_to_esp32(command):
    url = f"{ESP32_IP}/{command}"
    try:
        response = requests.get(url)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending command to ESP32: {e}")

def save_image_with_timestamp(img):
    # Create the folder if it doesn't exist
    folder_path = "potential_security_threats"
    os.makedirs(folder_path, exist_ok=True)
    
    # Get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the file path
    file_path = os.path.join(folder_path, f"{timestamp}.jpg")
    
    # Save the image
    cv2.imwrite(file_path, img)
    print(f"Image saved: {file_path}")
    time.sleep(3)

def main():
    cap = cv2.VideoCapture(1)
    detector = PoseDetector()

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        
        img, results = detector.findPose(img)
        lmList = detector.getPosition(img, results)

        # Get the frame dimensions
        height, width, _ = img.shape
        middle_line_x = width // 2

        # Draw the middle line
        cv2.line(img, (middle_line_x, 0), (middle_line_x, height), (255, 0, 0), 2)

        if lmList:
            # Head landmark indices
            head_landmarks_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            
            for index in head_landmarks_indices:
                x, y = lmList[index][1], lmList[index][2]
                if x > middle_line_x:  # Check if landmark's x-coordinate crosses the middle line
                    print("Alert: Head landmark crossed the line!")
                    cv2.putText(img, "Alert: Trespass detected!", (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    save_image_with_timestamp(img)
                    
                    # send_command_to_esp32("alert_on")
                    break  # Alert only once per frame if any head landmark crosses the line

        if isHandRaised(lmList):
            cv2.putText(img, "Hand Raised", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # send_command_to_esp32("alert_on")
        # else:
        #     send_command_to_esp32("alert_off")
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
