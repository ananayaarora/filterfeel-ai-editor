import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

class ImageEditor:
    """Handles image processing and filter applications"""
    
    def __init__(self):
        self.filters = {
            'warm': self._apply_warm_filter,
            'cool': self._apply_cool_filter,
            'vintage': self._apply_vintage_filter,
            'dramatic': self._apply_dramatic_filter,
            'soft': self._apply_soft_filter,
            'vibrant': self._apply_vibrant_filter,
            'monochrome': self._apply_monochrome_filter,
            'dreamy': self._apply_dreamy_filter,
            'golden': self._apply_golden_filter,
            'ethereal': self._apply_ethereal_filter,
            'moody': self._apply_moody_filter,
            'bright': self._apply_bright_filter
        }
    
    def apply_filter(self, image, filter_name):
        """Apply specified filter to image"""
        if filter_name.lower() in self.filters:
            return self.filters[filter_name.lower()](image)
        else:
            # Default to a gentle enhancement if filter not found
            return self._apply_soft_filter(image)
    
    def _pil_to_cv2(self, pil_image):
        """Convert PIL image to OpenCV format"""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def _cv2_to_pil(self, cv2_image):
        """Convert OpenCV image to PIL format"""
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    
    def _apply_warm_filter(self, image):
        """Apply warm, cozy filter for happy/romantic moods"""
        # Enhance warmth and brightness
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # Increase saturation
        
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)  # Slight brightness boost
        
        # Add warm tint
        cv2_image = self._pil_to_cv2(image)
        warm_kernel = np.array([[1.0, 1.1, 1.2]])
        cv2_image = cv2_image * warm_kernel
        cv2_image = np.clip(cv2_image, 0, 255).astype(np.uint8)
        
        return self._cv2_to_pil(cv2_image)
    
    def _apply_cool_filter(self, image):
        """Apply cool, calming filter for sad/calm moods"""
        # Reduce saturation and add blue tint
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.8)  # Reduce saturation
        
        cv2_image = self._pil_to_cv2(image)
        cool_kernel = np.array([[1.2, 1.1, 1.0]])
        cv2_image = cv2_image * cool_kernel
        cv2_image = np.clip(cv2_image, 0, 255).astype(np.uint8)
        
        return self._cv2_to_pil(cv2_image)
    
    def _apply_vintage_filter(self, image):
        """Apply vintage filter for nostalgic moods"""
        # Reduce saturation and add sepia tone
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.7)
        
        # Convert to grayscale and back for sepia effect
        gray = image.convert('L')
        sepia = Image.merge('RGB', (gray, gray, gray))
        
        # Apply sepia tint
        cv2_image = self._pil_to_cv2(sepia)
        sepia_kernel = np.array([[0.8, 0.9, 1.0]])
        cv2_image = cv2_image * sepia_kernel
        cv2_image = np.clip(cv2_image, 0, 255).astype(np.uint8)
        
        return self._cv2_to_pil(cv2_image)
    
    def _apply_dramatic_filter(self, image):
        """Apply dramatic filter for energetic/mysterious moods"""
        # Increase contrast and saturation
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)
        
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)
        
        # Apply slight vignette effect
        cv2_image = self._pil_to_cv2(image)
        h, w = cv2_image.shape[:2]
        
        # Create vignette mask
        X_resultant_kernel = cv2.getGaussianKernel(w, w/3)
        Y_resultant_kernel = cv2.getGaussianKernel(h, h/3)
        kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = kernel / kernel.max()
        
        for i in range(3):
            cv2_image[:, :, i] = cv2_image[:, :, i] * mask
        
        return self._cv2_to_pil(cv2_image)
    
    def _apply_soft_filter(self, image):
        """Apply soft filter for calm/dreamy moods"""
        # Apply slight blur and reduce contrast
        image = image.filter(ImageFilter.GaussianBlur(radius=0.8))
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.9)
        
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.05)
        
        return image
    
    def _apply_vibrant_filter(self, image):
        """Apply vibrant filter for energetic/celebratory moods"""
        # Boost saturation and contrast
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def _apply_monochrome_filter(self, image):
        """Apply monochrome filter for moody atmospheres"""
        # Convert to grayscale with slight tint
        gray = image.convert('L')
        
        # Add slight blue tint
        blue_tinted = Image.merge('RGB', (gray, gray, gray))
        enhancer = ImageEnhance.Color(blue_tinted)
        blue_tinted = enhancer.enhance(0.1)
        
        return blue_tinted
    
    def _apply_dreamy_filter(self, image):
        """Apply dreamy filter with soft glow"""
        # Apply gaussian blur and blend with original
        blurred = image.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Blend original with blurred version
        result = Image.blend(image, blurred, 0.3)
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(1.1)
        
        return result
    
    def _apply_golden_filter(self, image):
        """Apply golden hour filter"""
        # Add warm golden tint
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        cv2_image = self._pil_to_cv2(image)
        golden_kernel = np.array([[0.9, 1.0, 1.3]])
        cv2_image = cv2_image * golden_kernel
        cv2_image = np.clip(cv2_image, 0, 255).astype(np.uint8)
        
        return self._cv2_to_pil(cv2_image)
    
    def _apply_ethereal_filter(self, image):
        """Apply ethereal, otherworldly filter"""
        # High key effect with soft highlights
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.9)
        
        # Apply soft blur
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        return image
    
    def _apply_moody_filter(self, image):
        """Apply moody, atmospheric filter"""
        # Reduce brightness and increase contrast
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.8)
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Desaturate slightly
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.85)
        
        return image
    
    def _apply_bright_filter(self, image):
        """Apply bright, cheerful filter"""
        # Increase brightness and saturation
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        return image
