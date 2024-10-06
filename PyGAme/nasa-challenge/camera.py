import cv2

def capture_new_face_image():

    # Initialize the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot access the camera")
        exit()

    # Discard the first 15 frames
    for i in range(15):
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame {i}")
            exit()

    print("First 15 frames discarded")

    # Show live camera feed until a key is pressed
    while True:
        # Capture frame-by-frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Display the live feed in a window
        cv2.imshow('Live Camera - Press any key to take picture', frame)

        # Wait for a key press (1 ms delay between frames)
        if cv2.waitKey(1) & 0xFF != 255:  # Press any key to break the loop
            break

    # Save the captured frame as a picture after key press
    cv2.imwrite('resources/character/captured_image.jpg', frame)
    print("Picture taken and saved as 'captured_image.jpg'")

    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
