import numpy as np
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt


data_path = 'TI=50;Vb=1000;Vx=1;vy=0.4;gain=20.stm'
with open(data_path, 'rb') as f:
# Read the first 256 bytes to get the header information
    f.seek(-256 * 256, 2)
# Read the grayscale image data
    image_data = f.read(256 * 256)
# Convert the data to a NumPy array and reshape it into a 256x256 image
    grayscale_image = np.frombuffer(image_data, dtype=np.uint8).reshape((256, 256))
# Display the image using matplotlib
# Create a figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)

# Display the image
img_display = ax.imshow(grayscale_image, cmap='gray', origin='lower')

# Add sliders for contrast adjustment
ax_contrast = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_black = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_white = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_gamma = plt.axes([0.25, 0.1, 0.65, 0.03])

slider_contrast = Slider(ax_contrast, 'Contrast', 0.1, 3.0, valinit=1.0)
slider_black = Slider(ax_black, 'Black Point', 0, 255, valinit=0)
slider_white = Slider(ax_white, 'White Point', 0, 255, valinit=255)
slider_gamma = Slider(ax_gamma, 'Gamma', 0.1, 3.0, valinit=1.0)

# Update function for sliders
def update(val):
    contrast = slider_contrast.val
    black_point = slider_black.val
    white_point = slider_white.val
    gamma = slider_gamma.val

    # Adjust the image
    adjusted_image = np.clip((grayscale_image - black_point) / (white_point - black_point), 0, 1)
    adjusted_image = np.power(adjusted_image, gamma) * contrast
    img_display.set_data(adjusted_image)
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_contrast.on_changed(update)
slider_black.on_changed(update)
slider_white.on_changed(update)
slider_gamma.on_changed(update)

plt.show()