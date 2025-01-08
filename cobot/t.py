from pymycobot.mycobot import MyCobot
import time
import keyboard
import cv2 
import os
import shutil
from tensorflow.keras.models import load_model
import numpy as np

# Directories setup
dir = 'images'
os.makedirs(dir, exist_ok=True)
zip_dir = 'img_zip'
os.makedirs(zip_dir, exist_ok=True)

# Initialize variables
count = 0
points = []
model_path = 'path_to_your_cnn_model.h5'  # Update with your model path

# Load CNN model
model = load_model(model_path)

# Initialize camera and robot
cap = cv2.VideoCapture(1)
mc = MyCobot('COM7', 115200)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(2)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1)

while True:
    angles = mc.get_angles()
    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
   
    key = cv2.waitKey(1) & 0xff  

    if key == ord('q'):
        break
    if key == ord('a'):
        path = os.path.join(dir, f'img_{count}.jpg') 
        cv2.imwrite(path , frame)
        print("Image captured")
        count += 1

    cv2.imshow("Detection", frame)

    # Release all servos with 'w'
    if keyboard.is_pressed('w'):
        mc.release_all_servos()
        print("모든 서보를 해제합니다.")
    # Power on servos with 's'
    if keyboard.is_pressed('s'):
        print("모든 서보를 활성화합니다.")
        mc.power_on()
    # Save angles with 'e'
    if keyboard.is_pressed('e'):
        points.append(angles)
        print("각도 저장", angles)
    # Execute with 'd'
    if keyboard.is_pressed('d'):
        print("실행")
        break

# Define positions for good and defective products
good_position = points[1] if len(points) > 1 else [0, 0, 0, 0, 0, 0]
defective_position = points[2] if len(points) > 2 else [0, 0, 0, 0, 0, 0]

# Function to classify image using CNN model
def classify_image(image_path):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (224, 224)) # Adjust size to model input size
    img_array = np.expand_dims(img_resized / 255.0, axis=0) # Normalize and expand dimensions
    prediction = model.predict(img_array)
    return np.argmax(prediction)  # Assuming binary classification

# Process captured images
for i in range(count):
    image_path = os.path.join(dir, f'img_{i}.jpg')
    result = classify_image(image_path)

    if result == 0:
        print("양품입니다")
        mc.send_angles(good_position, 20)
    else:
        print("불량입니다")
        mc.send_angles(defective_position, 20)

    time.sleep(5)
    mc.set_eletric_gripper(0)
    mc.set_gripper_value(100, 20)
    time.sleep(2)
    mc.send_angles([0, 0, 0, 0, 0, 0], 30)
    time.sleep(5)

cap.release()
cv2.destroyAllWindows()

# Zip the images directory
zip_dir_path = os.path.join(zip_dir, 'archive')
shutil.make_archive(zip_dir_path , 'zip', dir)