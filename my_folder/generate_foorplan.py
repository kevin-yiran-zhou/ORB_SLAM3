import cv2
import numpy as np

# Real-world dimensions in meters
outer_width_m = 30
outer_height_m = 40
hallway_width_m = 2
padding_m = 10  # extra white space around

# Pixels per meter
scale = 20

# Convert to pixels
outer_w = int(outer_width_m * scale)
outer_h = int(outer_height_m * scale)
hallway_w = int(hallway_width_m * scale)
padding = int(padding_m * scale)

# Canvas size
img_w = outer_w + padding * 2
img_h = outer_h + padding * 2

# Create white canvas
img = np.ones((img_h, img_w), dtype=np.uint8) * 255

# Outer rectangle border
pt1_outer = (padding, padding)
pt2_outer = (padding + outer_w, padding + outer_h)
cv2.rectangle(img, pt1_outer, pt2_outer, color=0, thickness=2)

# Inner rectangle border
pt1_inner = (padding + hallway_w, padding + hallway_w)
pt2_inner = (padding + outer_w - hallway_w, padding + outer_h - hallway_w)
cv2.rectangle(img, pt1_inner, pt2_inner, color=0, thickness=2)

# Save image
cv2.imwrite("toy_floorplan.png", img)
print("✅ Saved: toy_floorplan.png")
