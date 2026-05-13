from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import math
from config.settings import THUMBNAIL_DIR

def generate_anime_thumbnail(video_path, output_path):
    """
    Generate anime-style thumbnail with glowing effects
    Mimics the aesthetic of high-quality anime character art
    """
    try:
        # Mobile-friendly vertical size (like anime profile)
        width, height = 1080, 1920
        
        # Create image with transparency
        img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Random anime color palette (vibrant gradients)
        palettes = [
            # Purple/Blue mystical
            [(30, 10, 80), (80, 20, 150), (120, 100, 200)],
            # Pink/Purple dream
            [(100, 30, 80), (180, 80, 150), (220, 150, 200)],
            # Blue/Cyan ice
            [(10, 60, 120), (50, 150, 200), (100, 200, 220)],
            # Green/Teal nature
            [(20, 80, 60), (60, 180, 140), (100, 220, 180)],
            # Orange/Red fire
            [(150, 50, 20), (220, 100, 40), (255, 150, 80)],
        ]
        
        chosen_palette = random.choice(palettes)
        color1, color2, color3 = chosen_palette
        
        # Create gradient background
        for y in range(height):
            # Smooth gradient interpolation
            ratio = y / height
            if ratio < 0.5:
                # Blend color1 to color2
                r = int(color1[0] + (color2[0] - color1[0]) * (ratio * 2))
                g = int(color1[1] + (color2[1] - color1[1]) * (ratio * 2))
                b = int(color1[2] + (color2[2] - color1[2]) * (ratio * 2))
            else:
                # Blend color2 to color3
                r = int(color2[0] + (color3[0] - color2[0]) * ((ratio - 0.5) * 2))
                g = int(color2[1] + (color3[1] - color2[1]) * ((ratio - 0.5) * 2))
                b = int(color2[2] + (color3[2] - color2[2]) * ((ratio - 0.5) * 2))
            
            draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b, 255))
        
        # Add light particles (bokeh effect)
        num_particles = random.randint(30, 50)
        for _ in range(num_particles):
            px = random.randint(0, width)
            py = random.randint(0, height)
            psize = random.randint(5, 30)
            alpha = random.randint(50, 180)
            
            # Draw glowing circles
            draw.ellipse(
                [(px - psize, py - psize), (px + psize, py + psize)],
                fill=(255, 255, 255, alpha)
            )
        
        # Add central glow effect
        glow_x, glow_y = width // 2, height // 2
        for radius in range(400, 0, -20):
            alpha = int(100 * (1 - radius / 400))
            draw.ellipse(
                [(glow_x - radius, glow_y - radius), (glow_x + radius, glow_y + radius)],
                fill=(255, 200, 255, alpha)
            )
        
        # Add geometric elements (anime style accents)
        # Triangles
        for _ in range(3):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 80)
            points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
            draw.polygon(points, fill=(255, 255, 255, 20))
        
        # Add text overlay
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            title_font = subtitle_font = ImageFont.load_default()
        
        # Title
        title = "🎬 ENCODED"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = height // 2 - 100
        
        # Add text shadow
        draw.text((title_x + 3, title_y + 3), title, fill=(0, 0, 0, 150), font=title_font)
        draw.text((title_x, title_y), title, fill=(255, 255, 255, 255), font=title_font)
        
        # Subtitle
        subtitle = "✨ Professional Encoding ✨"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = title_y + 120
        
        draw.text((subtitle_x + 2, subtitle_y + 2), subtitle, fill=(0, 0, 0, 100), font=subtitle_font)
        draw.text((subtitle_x, subtitle_y), subtitle, fill=(220, 200, 255, 220), font=subtitle_font)
        
        # Add border glow
        border_width = 8
        draw.rectangle(
            [(border_width, border_width), (width - border_width, height - border_width)],
            outline=(255, 255, 255, 180),
            width=border_width
        )
        
        # Add inner border
        inner_border = border_width + 5
        draw.rectangle(
            [(inner_border, inner_border), (width - inner_border, height - inner_border)],
            outline=(200, 150, 255, 100),
            width=2
        )
        
        # Apply subtle blur for depth (anime aesthetic)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Convert to RGB for JPEG compatibility
        final_img = Image.new('RGB', (width, height), color=(0, 0, 0))
        final_img.paste(img, (0, 0), img)
        
        # Save thumbnail
        final_img.save(output_path, quality=95)
        print(f"✨ Anime thumbnail created: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Thumbnail generation error: {e}")
        return None
