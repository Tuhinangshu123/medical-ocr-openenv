#!/usr/bin/env python3
"""
Generate synthetic prescription images from JSON ground truth
Creates realistic-looking prescription images for testing
"""
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


def create_prescription_image(text: str, difficulty: str, output_path: str):
    """Create a prescription image from text"""
    
    # Image settings based on difficulty
    if difficulty == "easy":
        # Clear, printed text
        width, height = 800, 1000
        bg_color = (255, 255, 255)
        text_color = (0, 0, 0)
        font_size = 24
        noise_level = 0
    elif difficulty == "medium":
        # Handwritten style (simulated with different font)
        width, height = 800, 1000
        bg_color = (250, 248, 245)  # Slightly off-white
        text_color = (20, 20, 50)
        font_size = 22
        noise_level = 5
    else:  # hard
        # Complex, dense text
        width, height = 800, 1200
        bg_color = (248, 245, 240)
        text_color = (30, 30, 60)
        font_size = 20
        noise_level = 10
    
    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        if difficulty == "medium":
            # Try to simulate handwriting
            font = ImageFont.truetype("arial.ttf", font_size)
        else:
            font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Add text with wrapping
    y_position = 50
    x_margin = 50
    line_spacing = 10
    
    for line in text.split('\n'):
        # Wrap long lines
        wrapped_lines = textwrap.wrap(line, width=50) if len(line) > 50 else [line]
        
        for wrapped_line in wrapped_lines:
            # Add slight randomness for medium/hard
            x_offset = 0
            if difficulty == "medium":
                import random
                x_offset = random.randint(-3, 3)
            elif difficulty == "hard":
                import random
                x_offset = random.randint(-5, 5)
            
            draw.text((x_margin + x_offset, y_position), wrapped_line, 
                     fill=text_color, font=font)
            y_position += font_size + line_spacing
    
    # Add noise for medium/hard
    if noise_level > 0:
        import random
        pixels = img.load()
        for _ in range(noise_level * 100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            noise = random.randint(-20, 20)
            current = pixels[x, y]
            pixels[x, y] = tuple(max(0, min(255, c + noise)) for c in current)
    
    # Save image
    img.save(output_path, 'JPEG', quality=85)
    print(f"Created: {output_path}")


def generate_all_images():
    """Generate images for all JSON files"""
    
    base_dir = Path(__file__).parent / "test_data"
    
    for difficulty in ["easy", "medium", "hard"]:
        difficulty_dir = base_dir / difficulty
        
        if not difficulty_dir.exists():
            print(f"Directory not found: {difficulty_dir}")
            continue
        
        # Process each JSON file
        for json_file in difficulty_dir.glob("*.json"):
            # Load ground truth
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Create image filename
            image_file = json_file.with_suffix('.jpg')
            
            # Generate image
            create_prescription_image(
                text=data['text'],
                difficulty=difficulty,
                output_path=str(image_file)
            )
    
    print("\n✅ All prescription images generated!")
    print("\nNext steps:")
    print("1. Review images in test_data/ directories")
    print("2. Replace with real prescription images if available")
    print("3. Test the environment with: python test_environment.py")


if __name__ == "__main__":
    generate_all_images()
