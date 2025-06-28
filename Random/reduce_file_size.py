from PIL import Image
import os

def compress_image(input_path, output_path, target_size_kb):
    """
    Compress an image to ensure its size is below the target size in KB.
    
    Parameters:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.
        target_size_kb (int): Target file size in KB.
    """
    # Open the image
    img = Image.open(input_path)
    
    # Initial quality for compression
    quality = 85
    
    # Reduce dimensions if necessary
    width, height = img.size
    scaling_factor = 0.9  # Scale down by 10% iteratively if needed
    
    while True:
        # Save the image with reduced quality
        img.save(output_path, optimize=True, quality=quality)
        
        # Check file size
        file_size_kb = os.path.getsize(output_path) / 1024
        
        if file_size_kb <= target_size_kb:
            break
        
        # Reduce quality further or scale down dimensions if needed
        if quality > 10:
            quality -= 5
        else:
            width = int(width * scaling_factor)
            height = int(height * scaling_factor)
            img = img.resize((width, height), Image.ANTIALIAS)
    
    print(f"Compression complete. Final size: {file_size_kb:.2f} KB")

# Input and output paths
input_image_path = "Passport Photo (No Smile Allowed).jpeg"  # Replace with your image path
output_image_path = "compressed_passport_photo.jpeg"

# Target size in KB
target_size_kb = 30

# Compress the image
compress_image(input_image_path, output_image_path, target_size_kb)
