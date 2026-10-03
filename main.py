# main.py (MicroVN Complete Core Engine)
import framebuf
import scenes

# Global Game Flags
game_flags = {
    "brave": False,
    "has_key": False
}

current_scene_label = "start"

# Core Transparency Constants (Magenta Masking)
COLOR_KEY_HEX = "#FF00FF"
COLOR_KEY_RGB565 = 0xF81F

# Define screen boundaries and canvas buffer parameters
UI_WIDTH = 48
SCREEN_W = 240
SCREEN_H = 320

# Create a master display canvas in native MicroPython memory (RGB565 = 2 Bytes/pixel)
master_buffer = bytearray(SCREEN_W * SCREEN_H * 2)
canvas = framebuf.FrameBuffer(master_buffer, SCREEN_W, SCREEN_H, framebuf.RGB565)

def load_bmp_to_canvas(filename, dest_x, dest_y, use_transparency=False):
    """Natively reads uncompressed 16-bit RGB565 BMP files straight into memory."""
    try:
        with open(filename, "rb") as f:
            # Read standard 54-byte BMP metadata header
            header = f.read(54)
            if not header or header[0:2] != b'BM':
                return

            # Extract dimensions directly from file structural byte markers
            img_w = int.from_bytes(header[18:22], "little")
            img_h = int.from_bytes(header[22:26], "little")
            
            # Read pixel array size (2 bytes per pixel for RGB565 structures)
            data_size = img_w * img_h * 2
            pixel_data = bytearray(f.read(data_size))
            
            # Convert raw byte array into a blittable MicroPython FrameBuffer object
            sprite_fbuf = framebuf.FrameBuffer(pixel_data, img_w, img_h, framebuf.RGB565)
            
            # Blit directly to master canvas with hardware-level color-key transparency
            if use_transparency:
                canvas.blit(sprite_fbuf, dest_x, dest_y, COLOR_KEY_RGB565)
            else:
                canvas.blit(sprite_fbuf, dest_x, dest_y)
                
            print("[RENDER ENGINE]: Natively blitted '" + filename + "' (" + str(img_w) + "x" + str(img_h) + ")")
    except Exception as e:
        print("[RENDER ERROR]: Could not decode file " + filename + " -> " + str(e))

def blit_background(image_name):
    if not image_name:
        canvas.fill(0) # Clear display to a solid black background
        return
    # Force full screen backgrounds down to the coordinate origin (0, 0)
    load_bmp_to_canvas(image_name, 0, 0, use_transparency=False)

def blit_character(image_name, position):
    if not image_name:
        return
    
    # Calculate coordinate markers based on position tokens
    dest_x = 20 if position == "left" else 140
    dest_y = 60 # Leave top clearance buffer zone for scenery assets
    
    load_bmp_to_canvas(image_name, dest_x, dest_y, use_transparency=True)

def render_ui(name, text):
    print("=" * UI_WIDTH)
    print(" " + name + ":")
    
    words = text.split(" ")
    current_line = "   "
    
    for word in words:
        if len(current_line) + len(word) + 1 > (UI_WIDTH - 2):
            print(current_line)
            current_line = "   " + word
        else:
            if current_line == "   ":
                current_line += word
            else:
                current_line += " " + word
    
    if current_line.strip():
        print(current_line)
        
    print("=" * UI_WIDTH)

def display_choices(choice_list):
    print("\n   [ CHOICES ]")
    for index in range(len(choice_list)):
        print("   \t" + str(index + 1) + ". " + choice_list[index]["text"])
    
    while True:
        user_input = input("\nSelect option number: ")
        if user_input.isdigit():
            selection = int(user_input) - 1
            if 0 <= selection < len(choice_list):
                return choice_list[selection]
        print("Invalid choice.")

def run_engine():
    global current_scene_label
    print("--- MICROVN ENGINE LIVE ---")
    
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

                chosen_option = display_choices(valid_choices)
                
                if "set_flag" in chosen_option:
                    flag_dict = chosen_option["set_flag"]
                    for flag_key in flag_dict:
                        game_flags[flag_key] = flag_dict[flag_key]
                        print("   -> Flag Updated: " + flag_key + " = " + str(flag_dict[flag_key]))
                
                current_scene_label = chosen_option["next_scene"]
                break
        else:
            input("\n[Enter to advance]")
            if "choices" not in line:
                break

    print("\n--- END OF SCENARIO ---")

if __name__ == "__main__":
    run_engine()
