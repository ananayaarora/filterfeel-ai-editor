from PIL import ImageEnhance, Image, ImageOps

def enhance_image(img):
    """
    Automatically enhances brightness, contrast, and sharpness.
    """
    # Brightness
    bright = ImageEnhance.Brightness(img)
    img = bright.enhance(1.2)

    # Contrast
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.3)

    # Sharpness
    sharp = ImageEnhance.Sharpness(img)
    img = sharp.enhance(1.1)

    return img


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
