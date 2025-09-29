"""
Image Preprocessing Module
Handles robust image preprocessing for emotion recognition.
Includes resize, noise reduction, histogram equalization, CLAHE, 
brightness normalization, and contrast enhancement.
"""

import cv2
import numpy as np
from enum import Enum

class PreprocessingMethod(Enum):
    """Available preprocessing methods"""
    GRAYSCALE_EQUALIZATION = "grayscale_equalization"
    COLOR_EQUALIZATION = "color_equalization"
    CLAHE = "clahe"
    CLAHE_COLOR = "clahe_color"
    BRIGHTNESS_NORMALIZATION = "brightness_normalization"
    CONTRAST_ENHANCEMENT = "contrast_enhancement"
    COMBINED = "combined"

class ImagePreprocessor:
    """
    Robust image preprocessing for emotion recognition.
    Supports multiple preprocessing methods and combinations.
    """
    
    def __init__(self, target_size=(224, 224), preprocessing_method=PreprocessingMethod.COMBINED):
        """
        Initialize the image preprocessor.
        
        Args:
            target_size (tuple): Target size for resizing (width, height)
            preprocessing_method (PreprocessingMethod): Method to use for preprocessing
        """
        self.target_size = target_size
        self.preprocessing_method = preprocessing_method
        
        # CLAHE parameters
        self.clahe_clip_limit = 3.0
        self.clahe_tile_grid_size = (8, 8)
        
        # Initialize CLAHE
        self.clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip_limit,
            tileGridSize=self.clahe_tile_grid_size
        )
    
    def resize_image(self, image):
        """
        Resize image to target size while maintaining aspect ratio.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Resized image
        """
        return cv2.resize(image, self.target_size, interpolation=cv2.INTER_AREA)
    
    def reduce_noise(self, image):
        """
        Apply noise reduction using bilateral filter.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Denoised image
        """
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    def grayscale_equalization(self, image):
        """
        Apply histogram equalization to grayscale image.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Equalized grayscale image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        return cv2.equalizeHist(gray)
    
    def color_equalization(self, image):
        """
        Apply histogram equalization to each color channel.
        
        Args:
            image (numpy.ndarray): Input BGR image
            
        Returns:
            numpy.ndarray: Equalized color image
        """
        if len(image.shape) != 3:
            return image
        
        # Split channels
        b, g, r = cv2.split(image)
        
        # Equalize each channel
        b_eq = cv2.equalizeHist(b)
        g_eq = cv2.equalizeHist(g)
        r_eq = cv2.equalizeHist(r)
        
        # Merge channels
        return cv2.merge([b_eq, g_eq, r_eq])
    
    def apply_clahe_grayscale(self, image):
        """
        Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to grayscale image.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: CLAHE enhanced grayscale image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        return self.clahe.apply(gray)
    
    def apply_clahe_color(self, image):
        """
        Apply CLAHE to color image in LAB color space.
        
        Args:
            image (numpy.ndarray): Input BGR image
            
        Returns:
            numpy.ndarray: CLAHE enhanced color image
        """
        if len(image.shape) != 3:
            return image
        
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        l_clahe = self.clahe.apply(l)
        
        # Merge channels and convert back to BGR
        lab_clahe = cv2.merge([l_clahe, a, b])
        return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    
    def normalize_brightness(self, image, target_brightness=128):
        """
        Normalize image brightness to target value.
        
        Args:
            image (numpy.ndarray): Input image
            target_brightness (int): Target brightness value (0-255)
            
        Returns:
            numpy.ndarray: Brightness normalized image
        """
        # Calculate current brightness
        current_brightness = np.mean(image)
        
        # Calculate adjustment factor
        if current_brightness > 0:
            adjustment = target_brightness / current_brightness
            # Apply adjustment with clipping
            normalized = np.clip(image * adjustment, 0, 255).astype(np.uint8)
        else:
            normalized = image.copy()
        
        return normalized
    
    def enhance_contrast(self, image, alpha=1.2, beta=10):
        """
        Enhance image contrast using linear transformation.
        
        Args:
            image (numpy.ndarray): Input image
            alpha (float): Contrast control (1.0 = no change, >1.0 = more contrast)
            beta (int): Brightness control (0 = no change, >0 = brighter)
            
        Returns:
            numpy.ndarray: Contrast enhanced image
        """
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    def preprocess(self, image):
        """
        Apply comprehensive preprocessing based on selected method.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Preprocessed image
        """
        if image is None:
            raise ValueError("Input image is None")
        
        # Start with a copy
        processed = image.copy()
        
        # Apply preprocessing based on selected method
        if self.preprocessing_method == PreprocessingMethod.GRAYSCALE_EQUALIZATION:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.grayscale_equalization(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.COLOR_EQUALIZATION:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.color_equalization(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.CLAHE:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.apply_clahe_grayscale(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.CLAHE_COLOR:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.apply_clahe_color(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.BRIGHTNESS_NORMALIZATION:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.normalize_brightness(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.CONTRAST_ENHANCEMENT:
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            processed = self.enhance_contrast(processed)
            
        elif self.preprocessing_method == PreprocessingMethod.COMBINED:
            # Apply comprehensive preprocessing pipeline
            processed = self.resize_image(processed)
            processed = self.reduce_noise(processed)
            
            # Apply CLAHE in LAB color space for better results
            if len(processed.shape) == 3:
                processed = self.apply_clahe_color(processed)
            else:
                processed = self.apply_clahe_grayscale(processed)
            
            # Normalize brightness
            processed = self.normalize_brightness(processed)
            
            # Enhance contrast slightly
            processed = self.enhance_contrast(processed, alpha=1.1, beta=5)
        
        return processed
    
    def set_preprocessing_method(self, method):
        """
        Change the preprocessing method.
        
        Args:
            method (PreprocessingMethod): New preprocessing method
        """
        self.preprocessing_method = method
    
    def set_clahe_parameters(self, clip_limit, tile_grid_size):
        """
        Update CLAHE parameters.
        
        Args:
            clip_limit (float): CLAHE clip limit
            tile_grid_size (tuple): CLAHE tile grid size
        """
        self.clahe_clip_limit = clip_limit
        self.clahe_tile_grid_size = tile_grid_size
        self.clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip_limit,
            tileGridSize=self.clahe_tile_grid_size
        )

# Example usage and testing
if __name__ == "__main__":
    # Test the preprocessor with different methods
    import os
    
    # Create test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test different preprocessing methods
    methods = [
        PreprocessingMethod.GRAYSCALE_EQUALIZATION,
        PreprocessingMethod.COLOR_EQUALIZATION,
        PreprocessingMethod.CLAHE,
        PreprocessingMethod.CLAHE_COLOR,
        PreprocessingMethod.COMBINED
    ]
    
    for method in methods:
        preprocessor = ImagePreprocessor(preprocessing_method=method)
        processed = preprocessor.preprocess(test_image)
        print(f"Method {method.value}: Input shape {test_image.shape}, Output shape {processed.shape}")
