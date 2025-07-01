# 📦 Required Libraries
from PIL import Image, ImageEnhance
import cv2
import numpy as np

# 💡 Brightness Enhancer (Pillow)
def enhance_brightness(img, factor=1.5):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# 💡 Contrast Enhancer (Pillow)
def enhance_contrast(img, factor=1.3):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)

# 💡 Sharpness Enhancer (Pillow)
def enhance_sharpness(img, factor=2.0):
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)

# 🧠 Extra: OpenCV – Sharpen Filter
def sharpen_opencv(img_path):
    img = cv2.imread(img_path)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(img, -1, kernel)
    cv2.imwrite("opencv_sharp.jpg", sharp)

# 🏁 Main Execution Block
if __name__ == "__main__":
    try:
        # 📥 Ask user for image filename
        filename = input("Enter the image file name (with extension, e.g., 'photo.jpg'): ")

        # === PILLOW PART ===
        img = Image.open(filename)

        enhance_brightness(img.copy()).save("bright.jpg")
        enhance_contrast(img.copy()).save("contrast.jpg")
        enhance_sharpness(img.copy()).save("sharp.jpg")

        # === OPENCV PART ===
        sharpen_opencv(filename)

        print("✅ Pillow + OpenCV enhancements done successfully!")

    except FileNotFoundError:
        print("❌ File not found. Please make sure the image is in this folder.")



def apply_filter(img, filter_name):
    """
    Applies a color filter to the image based on the selected mood.
    """
    filter_name = filter_name.lower()

    if filter_name == "grayscale":
        return img.convert("L")

    elif filter_name == "sepia":
        sepia_img = ImageOps.colorize(img.convert("L"), '#704214', '#C0A080')
        return sepia_img

    elif filter_name == "warm":
        r, g, b = img.split()
        r = r.point(lambda i: min(255, i + 30))  # boost red
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "cool":
        r, g, b = img.split()
        b = b.point(lambda i: min(255, i + 30))  # boost blue
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "rose":
        r, g, b = img.split()
        r = r.point(lambda i: min(255, i + 20))
        g = g.point(lambda i: int(i * 0.9))
        return Image.merge("RGB", (r, g, b))

    elif filter_name == "dim":
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(0.7)

    # Default filter – no change
    return img

def enhance_image(img):
    # Apply brightness enhancement
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1.2)

def apply_filter(img, filter_name):
    if filter_name == "grayscale":
        return img.convert("L")  # Grayscale
    return img  # No change
