from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import cv2

# Brightness Enhancer (Pillow)
def enhance_brightness(img, factor=1.5):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# Contrast Enhancer (Pillow)
def enhance_contrast(img, factor=1.3):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)

# Sharpness Enhancer (Pillow)
def enhance_sharpness(img, factor=2.0):
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)

# OpenCV – Sharpen Filter (returns PIL Image)
def sharpen_opencv(pil_img):
    img = np.array(pil_img.convert("RGB"))
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(img, -1, kernel)
    return Image.fromarray(sharp)

# Mood-based filter
def apply_filter(img, filter_name):
    filter_name = filter_name.lower()

    if filter_name == "grayscale":
        return img.convert("L")

    elif filter_name == "sepia":
        sepia_img = ImageOps.colorize(img.convert("L"), '#704214', '#C0A080')
        return sepia_img

    elif filter_name == "warm":
        r, g, b = img.split()
        r = r.point(lambda i: min(255, i + 30))
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "cool":
        r, g, b = img.split()
        b = b.point(lambda i: min(255, i + 30))
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "rose":
        r, g, b = img.split()
        r = r.point(lambda i: min(255, i + 20))
        g = g.point(lambda i: int(i * 0.9))
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "dim":
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(0.7)

    elif filter_name == "sharp":
        return sharpen_opencv(img)

    # Default filter – no change
    return img

# General enhancement (example: brightness)
def enhance_image(img):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1.2)
