from PIL import ImageEnhance

def enhance_image(img):
    # Apply brightness enhancement
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1.2)

def apply_filter(img, filter_name):
    if filter_name == "grayscale":
        return img.convert("L")  # Grayscale
    return img  # No change
