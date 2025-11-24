from ultralytics import YOLO
import cv2
import warnings
import time
import os
import pygame

roi = [0, 0, 0, 0]
drawing = False 
roi_set = False

def draw_roi(event, x, y, flags, param):
    global roi, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi = [x, y, x, y]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            roi[2] = x
            roi[3] = y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi[2] = x
        roi[3] = y
        if roi[0] > roi[2]:
            roi[0], roi[2] = roi[2], roi[0]
        if roi[1] > roi[3]:
            roi[1], roi[3] = roi[3], roi[1]

warnings.filterwarnings("ignore", category=UserWarning, module="torch.cuda")
model = YOLO('yolov8m.pt') #if yolov8 midium is so heavy, you can use yolov8n, yolov8s
TARGET_CLASS_NAME = 'cell phone'

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("ERROR : CAN'T OPEN") #if you got this error, check "cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)" This part
    exit()

pygame.mixer.init()
alarm_sound = None
sound_file = "beep.wav" #If you wanna change alarm sound, Edit this

if os.path.exists(sound_file):
    alarm_sound = pygame.mixer.Sound(sound_file)
    print(f"Alarm sound '{sound_file}' loaded.")
else:
    print(f"Sound file '{sound_file}' not found. Its work without alarm.")

ALARM_DURATION = 3.0
alarm_trigger_time = 0.0
WINDOW_NAME = 'REAL TIME LOGIC TEST (s: Set, r: Reset, q: Quit)'

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(WINDOW_NAME, draw_roi)

print("--- Step 1. Set ROI ---")
print("1. DRAG MOUSE TO SET ROI")
print("2. 'S' Select, 'R' Reset, 'Q' Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if not roi_set:
        (x1, y1, x2, y2) = roi
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "Drag ROI. Press 'S' to set.", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow(WINDOW_NAME, frame) 
    
    else:
        results = model(frame, device=0, verbose=False, imgsz=640, classes=[0, 67]) 
        annotated_frame = results[0].plot()

        object_in_roi = False
        person_detected = False
        target_object_count = 0

        ROI_X_START, ROI_Y_START, ROI_X_END, ROI_Y_END = roi

        for r in results:
            for box in r.boxes:
                class_id = int(box.cls)
                class_name = model.names[class_id]
                
                if class_name == 'person':
                    person_detected = True

                if class_name == TARGET_CLASS_NAME:
                    target_object_count += 1
                    
                    x1, y1, x2, y2 = box.xyxy[0] 
                    
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    if (ROI_X_START < cx < ROI_X_END) and (ROI_Y_START < cy < ROI_Y_END):
                        object_in_roi = True

        if person_detected and object_in_roi:
            alarm_trigger_time = time.time()
        
        is_alarm_on = (time.time() - alarm_trigger_time) < ALARM_DURATION

        if is_alarm_on:
            print(f"'Person' And '{TARGET_CLASS_NAME}' DTC")

            cv2.rectangle(annotated_frame, (ROI_X_START, ROI_Y_START), (ROI_X_END, ROI_Y_END), (0, 0, 255), 2)
            cv2.putText(annotated_frame, "!!! WARNING !!", (ROI_X_START, ROI_Y_START - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if alarm_sound and not pygame.mixer.get_busy():
                alarm_sound.play()
        else:
            cv2.rectangle(annotated_frame, (ROI_X_START, ROI_Y_START), (ROI_X_END, ROI_Y_END), (0, 255, 0), 2)
        
        cv2.putText(annotated_frame, f"Detected: {target_object_count}", (50, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)

        cv2.imshow(WINDOW_NAME, annotated_frame) 

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        print("Quit.")
        break
    elif key == ord('s'):
        if not roi_set:
            roi_set = True
            print("--- Step 2: Start DTC---")
            print(f"ROI got selected {roi}, press 'R' to reset.")
            cv2.setMouseCallback(WINDOW_NAME, lambda *args: None)
    elif key == ord('r'):
        if roi_set:
            roi_set = False
            print("--- Step 1: Reset ROI ---")
            cv2.setMouseCallback(WINDOW_NAME, draw_roi)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
print("Quit")