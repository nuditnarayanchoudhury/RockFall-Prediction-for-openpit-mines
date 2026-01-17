import cv2
import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy
import random
import os

# -------------------------
# Feature extraction
# -------------------------
def extract_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 1. Crack density (Canny edges)
    edges = cv2.Canny(gray, 100, 200)
    crack_density = np.sum(edges > 0) / edges.size

    # 2. Debris texture (GLCM + entropy)
    glcm = graycomatrix(gray, [1], [0], symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    entropy_val = shannon_entropy(gray)

    # 3. Vegetation (green pixel ratio)
    green_channel = image[:, :, 1]
    green_ratio = np.sum(green_channel > 100) / green_channel.size

    return crack_density, entropy_val, contrast, homogeneity, green_ratio

# -------------------------
# Augmentations (extended)
# -------------------------
def augment_image(image, n_variations=1500):
    h, w = image.shape[:2]
    augmented = []

    for _ in range(n_variations):
        aug = image.copy()

        # Random rotation
        angle = random.choice([0, 90, 180, 270])
        if angle != 0:
            M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
            aug = cv2.warpAffine(aug, M, (w, h))

        # Random flip
        flip_code = random.choice([-1, 0, 1, None])
        if flip_code is not None:
            aug = cv2.flip(aug, flip_code)

        # Random brightness/contrast
        alpha = random.uniform(0.7, 1.3)  # contrast
        beta = random.randint(-40, 40)    # brightness
        aug = cv2.convertScaleAbs(aug, alpha=alpha, beta=beta)

        # Random Gaussian noise
        if random.random() > 0.5:
            noise = np.random.normal(0, random.randint(5, 30), aug.shape).astype(np.int16)
            noisy = np.clip(aug.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            aug = noisy

        # Random blur
        if random.random() > 0.5:
            k = random.choice([3, 5])
            aug = cv2.GaussianBlur(aug, (k, k), 0)

        augmented.append(aug)

    return augmented

# -------------------------
# Main
# -------------------------
image_path = "../dataset/syntehetic_Drone.png"  # Change path if needed
image = cv2.imread(image_path)

augmented_images = augment_image(image, n_variations=1500)

rows = []
for idx, aug_img in enumerate(augmented_images):
    features = extract_features(aug_img)
    rows.append({
        "id": idx,
        "crack_density": features[0],
        "debris_entropy": features[1],
        "debris_contrast": features[2],
        "debris_homogeneity": features[3],
        "vegetation_green_ratio": features[4]
    })

df = pd.DataFrame(rows)
df.to_csv("../dataset/synthetic_drone_dataset.csv", index=False)

print("✅ Dataset saved as synthetic_drone_dataset.csv with", len(df), "rows")
print(df.head())
