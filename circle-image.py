import cv2
import numpy as np

# Load the image
image = cv2.imread('captured_image.jpg', cv2.IMREAD_UNCHANGED)  # Replace with your image path

# Define the center and radius of the circle
center = (image.shape[1] // 2, image.shape[0] // 2)  # Center of the image
radius = min(center)  # Choose a radius that fits within the image dimensions

# Create a mask with the same dimensions as the image, initialized to zeros (black)
mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

# Draw a filled circle on the mask
cv2.circle(mask, center, radius, (255), thickness=-1)

# Create an output image with an alpha channel (transparency)
output = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Set the alpha channel to 0 (transparent) where the mask is 0 (outside the circle)
output[:, :, 3] = mask

# Crop the image to the bounding box of the circle
x, y, w, h = cv2.boundingRect(mask)
cropped_image = output[y:y+h, x:x+w]

# Save the cropped image as PNG
cv2.imwrite('circle_cropped_image.png', cropped_image)

# Display the result (optional)
cv2.imshow('Cropped Circle', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
