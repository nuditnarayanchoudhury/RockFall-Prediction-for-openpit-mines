import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. Generate synthetic drone-like image
# -------------------------
def generate_synthetic_image(size=256):
    img = np.zeros((size, size, 3), dtype=np.uint8)

    # Vegetation patch (green)
    cv2.rectangle(img, (50, 50), (200, 120), (0, 255, 0), -1)

    # Crack (white line)
    cv2.line(img, (30, 200), (220, 50), (255, 255, 255), 2)

    # Loose debris (random gray dots)
    for _ in range(300):
        x, y = np.random.randint(0, size, 2)
        img[y, x] = (100, 100, 100)

    return img

synthetic_img = generate_synthetic_image()

# -------------------------
# 2. Crack detection (edges)
# -------------------------
gray = cv2.cvtColor(synthetic_img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

# -------------------------
# 3. Vegetation detection (green ratio)
# -------------------------
green_channel = synthetic_img[:,:,1]
veg_mask = cv2.inRange(synthetic_img, (0,100,0), (100,255,100))

# -------------------------
# 4. Show results
# -------------------------
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
axs[0].imshow(cv2.cvtColor(synthetic_img, cv2.COLOR_BGR2RGB))
axs[0].set_title("Synthetic Drone Image")
axs[1].imshow(edges, cmap="gray")
axs[1].set_title("Crack Detection")
axs[2].imshow(veg_mask, cmap="Greens")
axs[2].set_title("Vegetation Detection")
plt.show()
