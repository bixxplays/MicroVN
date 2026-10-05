# MicroVN
### MicroPython Visual Novel Core Engine

A highly optimized, zero-allocation-overhead **MicroPython game engine** designed to run branching visual novels natively on resource-constrained microcontrollers and desktops.

## 🤖 Specification & Licensing
While the **MicroVN** engine core was **AI-generated**, it was custom-engineered to meet a highly rigid, human-defined **engine software specification**.

Because it represents an original, functional work engineered to these specific software constraints, the **MIT License is fully valid** and applies to this repository. You are free to use, modify, and distribute it.

## 🚀 Core Philosophy
This repository contains only the **strict MicroVN engine core** responsible for parsing scene state trees, validating decision flags, managing layered asset buffers, and compiling pixel streams into a shared memory array.

* **State Machine & Canvas Only:** The engine tracks scene progress, conditional choices, and handles multi-layer binary blitting into a standardized screen buffer.
* **Microcontroller-Safe:** Built with memory-efficient loops to prevent memory allocation (heap fragmentation) errors common in MicroPython.

## 📝 UI Line Slicing & Custom Fonts
To ensure dialogue fits perfectly on small displays without lagging, **MicroVN** eliminates heavy text wrapping calculations and native desktop font engine requirements.

* **High-Efficiency Slicing:** Text wrapping is achieved using linear character-length slicing (`text[i:i+max_chars]`). This approach avoids dynamic word-parsing array generations, shielding microcontrollers from memory fragmentation crashes.
* **Custom Binary Fonts:** Built with a lightweight, native binary font map loader (`load_custom_font`) that reads raw uncompressed `.bin` character profiles.
* **Configurable Scaling:** Resolution limits, font sizes, colors, and layout positions are completely customized via top-level variables inside the core script file, removing project-level config file reading overhead.

## ⏳ Integrated Typewriter Effect
* **Native Typewriter Engine:** Dialogue can be animated letter-by-letter down the canvas bounding area using a hardware-safe text frame routine.
* **Granular Speed Tuning:** Managed entirely by the engine through a top-level `TYPEWRITER_SPEED` timing delay tracker.
* **Instant Fallback Toggle:** The animation pipeline can be instantly disabled globally via the `TYPEWRITER_ACTIVE` boolean flag to switch to default flat character blitting.

## 🖼️ Bitmap & Transparency Pipeline
Because standard microcontrollers lack the processing power and RAM to decode compressed `.png` alpha channels on the fly, **MicroVN** officially standardizes on **uncompressed 16-bit RGB565 `.bmp` (Bitmap)** asset tags.

* **Native Byte Parsing:** The engine reads binary pixel chunks from the disk structure and renders them directly into a managed memory canvas via the built-in `framebuf` module.
* **First-Class Transparency Support:** To eliminate blocky, square character sprites, the core rendering pipeline features built-in **Color Key Transparency**.
* **Customizable Color Keying:** By default, **MicroVN** establishes pure Magenta (`#FF00FF` / RGB565: `0xF81F`) as the designated transparency mask. Any pixels matching this color are dynamically skipped during the canvas draw loop, exposing the background layer below.

## 💾 Memory Canvas & Scope Boundary
The entire visual scene is drawn directly into an engine-managed memory byte array (`master_buffer`).

Because **MicroVN** itself is optimized for minimum overhead, **any failure to fit a project into your device's available memory is considered a project scope or asset design issue.**

Advanced optimization workarounds—such as dynamically loading only the current required scenes from disk, downscaling asset resolutions, or stream-reading art blocks—must be handled at the project level rather than being integrated into this universal engine core.

## 🛠️ Software Requirements

### 🌐 For Microcontrollers:
* **Runtime:** MicroPython firmware installed on your board (Raspberry Pi Pico, ESP32, ESP8266, etc.).
* **Dependencies:** None. Uses the built-in native firmware `framebuf` library.
* **Hardware Interfacing:** A tiny 1-line project-level loop is required to push the compiled `master_buffer` straight to your display controller data pins (SPI/I2C).

### 🪟 For Desktop (Windows, Mac, Linux):
The engine runs perfectly on desktop PCs, but requires a standalone dependency to mimic the microcontroller's canvas chip memory.

Follow the instructions below for your specific operating system:

#### 1. Install Framebuf Layer
* **Windows (Command Prompt / PowerShell):**
  ```cmd
  pip install adafruit-circuitpython-framebuf
  ```
* **Mac / Linux (Terminal / Bash):**
  ```bash
  pip3 install adafruit-circuitpython-framebuf
  ```

#### 2. Display Window Wrapper
Because desktop environments cannot read raw pins directly, a tiny project wrapper (such as **Pygame** or **Tkinter**) is required outside of the engine to load `master_buffer` and render it inside an OS window frame.

## 💻 Compatibility
Because **MicroVN** uses pure, standard **MicroPython** syntax, it is completely platform-agnostic and OS-agnostic. It runs seamlessly out of the box on:

* 🌐 **Microcontrollers** (Raspberry Pi Pico, ESP32, ESP8266 running MicroPython)
* 🪟 **Windows / Mac / Linux** (Running standard Python 3 interpreters with the framebuf layer)
* 🤖 **Android** (Via terminal environments like Termux or Pydroid 3 running a Python environment)

## 🚧 Scope & Customization (Forking)
To keep the core engine lightweight and hardware-agnostic, **large feature additions are considered game-design specific** and will not be added to the main branch.

If you want to implement features such as:
* 🔊 **Audio/Buzzer support**
* 🎮 **Hardware button input handling** (GPIO interrupts)
* 🖼️ **Dynamic 9-Slice Border math** (Custom text windows are loaded via `textbox.bmp` instead)

You are highly encouraged to **fork this repository** and build your custom hardware-level and design-level features right on top of this core layout.

## 📋 File Architecture
* **`main.py`**: The game engine runner, pixel canvas generator, binary font text rasterizer, and condition validator.
* **`scenes.py`**: Your custom script containing the branching `story` dictionary array layout.
