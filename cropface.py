import cv2
from PIL import Image

def cropface():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


    image_path = 'resources/character/captured_image.jpg' 
    image = cv2.imread(image_path)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print("No face detected!")
    else:
        print(f"Detected {len(faces)} face(s)")

        # Crop the first face detected (you can modify this to handle multiple faces)
        for (x, y, w, h) in faces:
            face = image[y:y+h, x:x+w]

            # Convert the face image from OpenCV (BGR) to PIL (RGB)
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(face_rgb)

            # Create a transparent background
            pil_image = pil_image.convert("RGBA")

            # Get pixel data
            datas = pil_image.getdata()

            # Set background pixels (not part of the face) as transparent
            new_data = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:  # Assuming the background is white
                    new_data.append((255, 255, 255, 0))  # Transparent
                else:
                    new_data.append(item)  # Keep face as it is

            pil_image.putdata(new_data)

            # Save the new image with transparent background
            pil_image.save('resources/character/cropped_face_with_transparent_bg.png')
            print("Face cropped and saved with transparent background!")
