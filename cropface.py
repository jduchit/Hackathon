import cv2
from PIL import Image
import os
import sys

def cropface():
    # Detect if running inside a PyInstaller package
    if hasattr(sys, '_MEIPASS'):
        haarcascade_path = os.path.join(sys._MEIPASS, 'cv2/data/haarcascade_frontalface_default.xml')
    else:
        haarcascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    face_cascade = cv2.CascadeClassifier(haarcascade_path)

    image_path = 'resources/character/captured_image.jpg' 
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print("No face detected!")
    else:
        print(f"Detected {len(faces)} face(s)")

        # Crop the first face detected
        for (x, y, w, h) in faces:
            face = image[y:y+h, x:x+w]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(face_rgb)
            pil_image = pil_image.convert("RGBA")

            # Create transparency for background
            datas = pil_image.getdata()
            new_data = []
            for item in datas:
                if item[:3] == (255, 255, 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            pil_image.putdata(new_data)
            pil_image.save('resources/character/cropped_face_with_transparent_bg.png')
            print("Face cropped and saved with transparent background!")
