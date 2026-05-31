import os
import io
import math
from PIL import Image, ImageDraw, ImageFont, ImageChops

def get_font(size, bold=False):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, 'assets', 'fonts', 'Roboto-Bold.ttf' if bold else 'Roboto-Regular.ttf')
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

def draw_text_with_shadow(draw, position, text, font, text_color, shadow_color=(0, 0, 0, 180), offset=(2, 2)):
    x, y = position
    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
    draw.text(position, text, font=font, fill=text_color)

def draw_star(draw, x, y, size, fill):
    cx = x + size / 2
    cy = y + size / 2
    outer_r = size / 2
    inner_r = outer_r * 0.382
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def generate_materials_image(character_obj, data_manager):
    width, height = 1150, 850
    
    # Create base canvas with transparency support
    bg_color = (20, 24, 35)
    image = Image.new('RGBA', (width, height), color=bg_color)
    
    base_dir = data_manager.base_dir
    project_root = os.path.dirname(base_dir)

    # --- Background Image with Sleek Tint ---
    bg_img = None
    if hasattr(character_obj, 'background_url') and character_obj.background_url:
        try:
            import requests
            res = requests.get(character_obj.background_url, timeout=10)
            if res.status_code == 200:
                bg_img = Image.open(io.BytesIO(res.content)).convert("RGBA")
        except Exception as e:
            print(f"Failed to load background from URL: {e}")

    if not bg_img:
        bg_path = os.path.join(project_root, 'img', 'background.jpg')
        if os.path.exists(bg_path):
            try:
                bg_img = Image.open(bg_path).convert("RGBA")
            except Exception as e:
                print(f"Failed to load local background image: {e}")

    if bg_img:
        try:
            bg_ratio = max(width / bg_img.width, height / bg_img.height)
            new_bg_w = int(bg_img.width * bg_ratio)
            new_bg_h = int(bg_img.height * bg_ratio)
            bg_img = bg_img.resize((new_bg_w, new_bg_h), Image.Resampling.LANCZOS)
            offset_x = (new_bg_w - width) // 2
            offset_y = (new_bg_h - height) // 2
            bg_img = bg_img.crop((offset_x, offset_y, offset_x + width, offset_y + height))
            image.paste(bg_img, (0, 0))
            
            # Sophisticated gradient tint (darker at bottom for text readability)
            tint = Image.new('RGBA', (width, height))
            tint_draw = ImageDraw.Draw(tint)
            for y in range(height):
                alpha = int(140 + (y / height) * 60) # Fades from 140 to 200 opacity
                tint_draw.line([(0, y), (width, y)], fill=(15, 18, 25, alpha))
            image.paste(tint, (0, 0), tint)
        except Exception as e:
            print(f"Failed to process background image: {e}")

    draw = ImageDraw.Draw(image)

    # --- 1. Draw Character Portrait ---
    char_img = None
    if hasattr(character_obj, 'image_url') and character_obj.image_url:
        try:
            import requests
            res = requests.get(character_obj.image_url, timeout=10)
            if res.status_code == 200:
                char_img = Image.open(io.BytesIO(res.content)).convert("RGBA")
        except Exception as e:
            print(f"Failed to load character image from URL: {e}")

    if not char_img:
        char_img_path = os.path.join(project_root, character_obj.image_file) if character_obj.image_file else None
        if char_img_path and os.path.exists(char_img_path):
            try:
                char_img = Image.open(char_img_path).convert("RGBA")
            except Exception as e:
                print(f"Failed to load local character image: {e}")

    left_width = 450
    if char_img:
        try:
            ratio = height / char_img.height
            new_w = int(char_img.width * ratio)
            char_img = char_img.resize((new_w, height), Image.Resampling.LANCZOS)
            left_width = new_w
            
            # Smoothstep gradient mask
            mask = Image.new('L', char_img.size, color=255)
            mask_draw = ImageDraw.Draw(mask)
            fade_width = 100
            for x in range(left_width - fade_width, left_width):
                t = (x - (left_width - fade_width)) / float(fade_width)
                smooth_t = t * t * (3 - 2 * t)
                alpha = int(255 * (1.0 - smooth_t))
                mask_draw.line([(x, 0), (x, height)], fill=alpha)
                
            if char_img.mode == 'RGBA':
                r, g, b, a = char_img.split()
                new_a = ImageChops.multiply(a, mask)
                char_img.putalpha(new_a)
            
            image.paste(char_img, (0, 0), char_img)
        except Exception as e:
            print(f"Failed to load character image: {e}")
            draw.rectangle([0, 0, left_width, height], fill=(30, 35, 45))

    # --- 2. Typography and UI ---
    start_x = left_width + 40
    current_y = 50
    
    title_font = get_font(56, bold=True)
    section_font = get_font(28, bold=True)
    item_font = get_font(18, bold=True)
    
    # Title
    title_text = f"{character_obj.name.upper()}"
    draw_text_with_shadow(draw, (start_x, current_y), title_text, title_font, (255, 255, 255), offset=(3, 3))
    current_y += 60
    
    # Rarity
    if hasattr(character_obj, 'rarity') and character_obj.rarity:
        try:
            rarity_count = int(character_obj.rarity)
            star_size = 24
            star_spacing = 6
            star_x = start_x + 5
            star_y = current_y + 8
            for _ in range(rarity_count):
                # Draw shadow
                draw_star(draw, star_x + 2, star_y + 2, star_size, (0, 0, 0, 180))
                # Draw star
                draw_star(draw, star_x, star_y, star_size, (255, 215, 0))
                star_x += star_size + star_spacing
            current_y += 45
        except (ValueError, TypeError):
            current_y += 15
    else:
        current_y += 15
    
    
    # Element & Weapon Pills
    element_colors = {
        'Glacio': (114, 219, 255),
        'Fusion': (255, 102, 102),
        'Electro': (212, 115, 255),
        'Aero': (102, 255, 178),
        'Spectro': (255, 230, 102),
        'Havoc': (153, 51, 255)
    }
    el_color = element_colors.get(character_obj.element.capitalize(), (200, 200, 200))
    weap_color = (60, 65, 80)
    
    subtitle_font = get_font(18, bold=True)
    el_text = character_obj.element.upper()
    wp_text = character_obj.weapon_type.upper()
    
    el_w = draw.textbbox((0,0), el_text, font=subtitle_font)[2]
    wp_w = draw.textbbox((0,0), wp_text, font=subtitle_font)[2]
    
    # Element Pill
    draw.rounded_rectangle([start_x, current_y, start_x + el_w + 24, current_y + 32], radius=16, fill=el_color)
    draw.text((start_x + 12, current_y + 5), el_text, font=subtitle_font, fill=(20, 20, 20))
    
    # Weapon Pill
    start_wp = start_x + el_w + 36
    draw.rounded_rectangle([start_wp, current_y, start_wp + wp_w + 24, current_y + 32], radius=16, fill=weap_color)
    draw.text((start_wp + 12, current_y + 5), wp_text, font=subtitle_font, fill=(240, 240, 240))
    
    current_y += 75

    # Helper function to draw item grids
    def draw_item_grid(title, materials_dict, x_start, y_start, max_width):
        # Section Title with accent
        draw_text_with_shadow(draw, (x_start, y_start), title, section_font, (255, 215, 0)) # Gold text
        draw.line([(x_start, y_start + 35), (x_start + 40, y_start + 35)], fill=(255, 215, 0), width=3) # Small accent line
        
        y_pos = y_start + 55
        icon_size = 76
        spacing_x = 105
        spacing_y = 115
        
        items_per_row = (width - x_start - 20) // spacing_x
        if items_per_row < 1: items_per_row = 1
        row, col = 0, 0
        
        # We need a separate layer for translucent drawing
        ui_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        ui_draw = ImageDraw.Draw(ui_layer)
        
        for item_key, amount in materials_dict.items():
            if amount == 0: continue
            
            item = data_manager.items.get(item_key)
            icon_path = os.path.join(project_root, item.icon) if item and item.icon else None
            
            x = x_start + col * spacing_x
            y = y_pos + row * spacing_y
            
            # Glassmorphism Item Box
            box_fill = (255, 255, 255, 20)
            box_outline = (255, 255, 255, 50)
            ui_draw.rounded_rectangle([x-6, y-6, x+icon_size+6, y+icon_size+6], radius=14, fill=box_fill, outline=box_outline, width=1)
            
            if icon_path and os.path.exists(icon_path):
                try:
                    icon_img = Image.open(icon_path).convert("RGBA")
                    icon_img = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    # Paste icon directly to the main image since it handles alphas properly
                    image.paste(icon_img, (x, y), icon_img)
                except Exception:
                    pass
            
            # Amount Pill overlapping the bottom
            amount_str = f"{amount:,}"
            text_bbox = draw.textbbox((0, 0), amount_str, font=item_font)
            text_w = text_bbox[2] - text_bbox[0]
            text_x = x + (icon_size - text_w) // 2
            text_y = y + icon_size - 4
            
            pill_fill = (20, 25, 35, 240)
            ui_draw.rounded_rectangle([text_x - 10, text_y - 2, text_x + text_w + 10, text_y + 24], radius=12, fill=pill_fill)
            ui_draw.text((text_x, text_y), amount_str, font=item_font, fill=(255, 255, 255))
            
            col += 1
            if col >= items_per_row:
                col = 0
                row += 1
                
        # Composite the UI layer over the image
        image.paste(ui_layer, (0, 0), ui_layer)
        
        rows_used = row + 1 if col > 0 else row
        return y_pos + rows_used * spacing_y

    if character_obj.ascension_materials:
        current_y = draw_item_grid("Ascension Materials", character_obj.ascension_materials, start_x, current_y, width - start_x)
        current_y += 15
        
    if character_obj.skill_materials:
        draw_item_grid("Skill Materials", character_obj.skill_materials, start_x, current_y, width - start_x)

    # --- 3. Draw Watermark ---
    watermark_font = get_font(18, bold=True)
    watermark_text = "Made by Ms. Shorekeeper"
    text_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    text_w = text_bbox[2] - text_bbox[0]
    draw_text_with_shadow(draw, (width - text_w - 25, height - 35), watermark_text, watermark_font, (200, 205, 220, 200), shadow_color=(0,0,0,150))

    # Convert to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr
