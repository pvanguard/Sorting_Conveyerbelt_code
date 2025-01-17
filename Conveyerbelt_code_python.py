import cv2
import numpy as np
import serial
import time

cap = cv2.VideoCapture(0)

lower_blue = np.array([105, 150, 50])
upper_blue = np.array([130, 255, 255])

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

def write(x):
    print(f"Sending to Arduino: {x}")  
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.5)  
fps = 720
fps_use = int(1000/fps)
while True:
    ret, frame = cap.read()

    if cv2.waitKey(fps_use) & 0xFF == ord('q'):
        break

    if ret:
        height, width, _ = frame.shape
        rect_start = (int(width * 0.10), int(height * 0.02))
        rect_end = (int(width * 0.90), int(height * 0.98))

        cv2.rectangle(frame, rect_start, rect_end, (255, 255, 255), 2)
        cv2.putText(frame, "Detection Area", rect_start, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        roi = frame[rect_start[1]:rect_end[1], rect_start[0]:rect_end[0]]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_pixels = cv2.countNonZero(mask_blue)  
        total_pixels = roi.shape[0] * roi.shape[1]  
        blue_percentage = (blue_pixels / total_pixels) * 100 

        cv2.putText(frame, f"Blue: {blue_percentage:.2f}%", (10, height - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        if blue_percentage > 2:  
            print("Blue")
            write('b\n')
        else:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)  
            print(f"Brightness: {brightness}")  

            cv2.putText(frame, f"Brightness: {brightness:.2f}", (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if brightness > 30: 
                print("White")
                write('w\n')
            elif brightness < 30:  
                print("Black")
                write('k\n')
            else:  
                print("Gray Area (Detected as Black)")
                write('k\n')

        if arduino.in_waiting > 0:
            arduino_data = arduino.readline().decode('utf-8').strip()
            print(f"Data from Arduino: {arduino_data}")

        cv2.imshow("Frame", frame)
        time.sleep(0.5) 

cap.release()
cv2.destroyAllWindows()
