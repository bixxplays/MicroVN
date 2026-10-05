# main.py (MicroVN Complete Core Engine)
import framebuf
import scenes
import time

# ==============================================================================
#                 PROJECT LAYOUT & PERFORMANCE CONFIGURATION VARIABLES
# ==============================================================================
# Game developers can modify these variables directly inside the core code.
SCREEN_W = 240
SCREEN_H = 320
UI_BOX_Y = 235
UI_BOX_H = 85

# Font Asset Decisions
FONT_FILE = "arcade_12px.bin"  # Project font data asset file
FONT_SIZE = 2                 # Scaled text pixel width multiplier (e.g. 1x, 2x)
FONT_COLOR = 0xFFFF           # Clear white dialogue text hex value
NAME_COLOR = 0xF800           # Deep red character title name hex value

# Typewriter System Core Toggles
TYPEWRITER_ACTIVE = True      # Set to False to disable the typewriter effect
TYPEWRITER_SPEED = 0.03       # Frame pause delay calculation in seconds
# ==============================================================================

# Global Engine Game Flags
game_flags = {
    "brave": False,
    "has_key": False
}

current_scene_label = "start"
_font_cache = {}

# Create a master display canvas in native MicroPython memory (RGB565 = 2 Bytes/pixel)
master_buffer = bytearray(SCREEN_W * SCREEN_H * 2)
canvas = framebuf.FrameBuffer(master_buffer, SCREEN_W, SCREEN_H, framebuf.RGB565)

def load_custom_font(filename):
    """Loads a raw custom pixel font map into RAM buffer arrays."""
    if filename in _font_cache:
        return _font_cache[filename]
    try:
        with open(filename, "rb") as f:
            _font_cache[filename] = f.read()
            print("[ENGINE]: Loaded project font: " + filename)
            return _font_cache[filename]
    except Exception as e:
        return None

def draw_custom_text(text, x, y, size, color, font_file):
    """Renders custom binary font maps to canvas with scaling attributes."""
    font_data = load_custom_font(font_file)
    if not font_data:
        canvas.text(text, x, y, color) # Fallback to default low-resolution system font
        return

    char_h = 12 # Native pixel height of your custom font file asset
    char_w = 8  # Native pixel width of your custom font file asset
    
    current_x = x
    for char in text:
        ascii_val = ord(char)
        if ascii_val < 32 or ascii_val > 126:
            current_x += char_w * size
            continue
            
        offset = (ascii_val - 32) * char_h
        
        for row in range(char_h):
            bits = font_data[offset + row]
            for col in range(char_w):
                if bits & (1 << (7 - col)):
                    if size == 1:
                        canvas.pixel(current_x + col, y + row, color)
                    else:
                        canvas.fill_rect(current_x + (col * size), y + (row * size), size, size, color)
                        
        current_x += char_w * size

def load_bmp_to_canvas(filename, dest_x, dest_y, use_transparency=False):
    """Natively reads uncompressed 16-bit RGB565 BMP files straight into memory."""
    try:
        with open(filename, "rb") as f:
            header = f.read(54)
            if not header or header[0:2] != b'BM':
                return

            img_w = int.from_bytes(header[18:22], "little")
            img_h = int.from_bytes(header[22:26], "little")
            
            data_size = img_w * img_h * 2
            pixel_data = bytearray(f.read(data_size))
            
            sprite_fbuf = framebuf.FrameBuffer(pixel_data, img_w, img_h, framebuf.RGB565)
            
            if use_transparency:
                canvas.blit(sprite_fbuf, dest_x, dest_y, 0xF81F) # Magenta transparency mask
            else:
                canvas.blit(sprite_fbuf, dest_x, dest_y)
    except:
        pass # Protect loop execution if assets fail to load

def blit_background(image_name):
    if not image_name:
        canvas.fill(0)
        return
    load_bmp_to_canvas(image_name, 0, 0, use_transparency=False)

def blit_character(image_name, position):
    if not image_name:
        return
    dest_x = 20 if position == "left" else 140
    dest_y = 60 
    load_bmp_to_canvas(image_name, dest_x, dest_y, use_transparency=True)

def render_ui(name, text, skip_typewriter=False):
    """Draws the text window, using core performance variables for layout logic."""
    # 1. Slice layout string based on mathematical screen resolution limits
    char_width_px = 8 * FONT_SIZE
    max_chars = (SCREEN_W - 16) // char_width_px
    lines = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    line_spacing = (12 * FONT_SIZE) + 2

    # 2. Typewriter Effect Loop Sequence
    if TYPEWRITER_ACTIVE and not skip_typewriter:
        current_visible_text = ""
        for char in text:
            current_visible_text += char
            
            try:
                load_bmp_to_canvas("textbox.bmp", 0, UI_BOX_Y, use_transparency=True)
            except:
                canvas.fill_rect(0, UI_BOX_Y, SCREEN_W, UI_BOX_H, 0x0000)
                canvas.hline(0, UI_BOX_Y, SCREEN_W, 0xFFFF)

            name_y = UI_BOX_Y + 8
            draw_custom_text(name + ":", 8, name_y, FONT_SIZE, NAME_COLOR, FONT_FILE)

            visible_lines = [current_visible_text[i:i+max_chars] for i in range(0, len(current_visible_text), max_chars)]
            
            start_y = name_y + line_spacing
            for line in visible_lines[:3]:
                draw_custom_text(line.strip(), 8, start_y, FONT_SIZE, FONT_COLOR, FONT_FILE)
                start_y += line_spacing
                
            # Hook your physical display push frame method right here:
            # e.g., tft.blit_buffer(master_buffer)
            
            time.sleep(TYPEWRITER_SPEED)
    else:
        # 3. Instant Rendering Sequence (Fallback)
        try:
            load_bmp_to_canvas("textbox.bmp", 0, UI_BOX_Y, use_transparency=True)
        except:
            canvas.fill_rect(0, UI_BOX_Y, SCREEN_W, UI_BOX_H, 0x0000)
            canvas.hline(0, UI_BOX_Y, SCREEN_W, 0xFFFF)

        name_y = UI_BOX_Y + 8
        draw_custom_text(name + ":", 8, name_y, FONT_SIZE, NAME_COLOR, FONT_FILE)
        
        start_y = name_y + line_spacing
        for line in lines[:3]:
            draw_custom_text(line.strip(), 8, start_y, FONT_SIZE, FONT_COLOR, FONT_FILE)
            start_y += line_spacing
            
        # Update display once at the end
        # e.g., tft.blit_buffer(master_buffer)

def display_choices_on_screen(choice_list):
    """Draws selectable scenario decisions onto the UI box buffer space."""
    canvas.fill_rect(0, UI_BOX_Y, SCREEN_W, UI_BOX_H, 0x0000)
    canvas.hline(0, UI_BOX_Y, SCREEN_W, 0xFFFF)
    
    draw_custom_text("[ CHOICES AVAILABLE ]", 8, UI_BOX_Y + 8, FONT_SIZE, NAME_COLOR, FONT_FILE)
    
    start_y = UI_BOX_Y + 8 + ((12 * FONT_SIZE) + 2)
    for index in range(min(len(choice_list), 3)): 
        draw_custom_text(str(index + 1) + ". " + choice_list[index]["text"], 8, start_y, FONT_SIZE, FONT_COLOR, FONT_FILE)
        start_y += (12 * FONT_SIZE) + 2
        
    while True:
        user_input = input("\nSelect option number: ")
        if user_input.isdigit():
            selection = int(user_input) - 1
            if 0 <= selection < len(choice_list):
                return choice_list[selection]
        print("Invalid choice.")

def run_engine():
    global current_scene_label
    print("--- MICROVN ENGINE LIVE (CORE CONFIG LOADED) ---")
    
    while current_scene_label in scenes.story:
        current_lines = scenes.story[current_scene_label]
        for line in current_lines:
            bg_img = line.get("background_img", None)
            blit_background(bg_img)
            
            img = line.get("character_img", None)
            pos = line.get("position", "center")
            blit_character(img, pos)
            
            render_ui(line["name"], line["text"])
            
            if "choices" in line:
                valid_choices = []
                for choice in line["choices"]:
                    if "req_flag" in choice:
                        req_dict = choice["req_flag"]
                        is_valid = True
                        for flag_key in req_dict:
                            if game_flags.get(flag_key, False) != req_dict[flag_key]:
                                is_valid = False
                                break
                        if not is_valid:
                            continue
                    valid_choices.append(choice)

                chosen_option = display_choices_on_screen(valid_choices)
                
                if "set_flag" in chosen_option:
                    flag_dict = chosen_option["set_flag"]
                    for flag_key in flag_dict:
                        game_flags[flag_key] = flag_dict[flag_key]
                
                current_scene_label = chosen_option["next_scene"]
                break
        else:
            input("\n[Enter to advance text]")
            if "choices" not in line:
                break

    canvas.fill(0)
    draw_custom_text("--- SCENARIO END ---", 40, 150, FONT_SIZE, FONT_COLOR, FONT_FILE)
    print("\n--- END OF SCENARIO ---")

if __name__ == "__main__":
    run_engine()
