# **ATAP - Animation Tool for Adorable Preschoolers 🥰**

## **What is ATAP?**
**ATAP** (abbr. Animation Tool for Adorable Preschoolers) is a **simple, fun, and easy-to-use** 2D animation program designed specifically for **young kids**. With an **intuitive interface, minimal complexity, and essential animation tools**, ATAP allows children to create **frame-by-frame animations effortlessly**!  

Kids can **draw, erase, fill colors, adjust brush sizes, play animations, undo changes, and even save unfinished projects to continue later**. ATAP makes animation accessible to everyone! 🎨✨  

---

# **Table of Contents**
- [Motivation](#motivation)
- [Installation For Users](#installation-for-users)
- [Features](#features)
- [Installation For Developers](#installation-for-developers)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Demo Gif](#demo-gif)

---

# **Motivation**
Most animation tools are **too complex for kids** or lack a **beginner-friendly experience**. **ATAP** was created to provide **preschoolers and young kids** with an intuitive, fun animation tool that **requires no learning curve**.  

With simple drawing tools, frame-by-frame animation, and an easy export option, ATAP makes **creating animations effortless!** 🚀🎨  

A huge shoutout to the project [**zide**](https://github.com/bitspaceorg/zide) from which I drew few inspirations.

---

# **Installation (For Users)**
- Download the executable program from the releases tab.
- After downloading, provide proper permissions to run it.
- Use and enjoy the ATAP application.
---

# **Features**
### 🎨 **Simple Freehand Drawing**
Kids can **draw, erase, and fill** their artwork with simple tools.  

### 🎞️ **Frame-by-Frame Animation**
Create animations by adding and managing multiple frames.  

### ✏️ **Adjustable Brush & Colors**
Select different **brush sizes and colors** to enhance creativity.  

### 🔄 **Undo & Redo**
**Easily revert mistakes** with **Undo (Ctrl+Z)** and **Redo (Ctrl+Y)** functionality.  

### 🎨 **Any Color Selection & Custom Palette**
- Choose colors from **a full spectrum** 🎨  
- Create a **custom color palette** for quick selection.  

### 🌈 **Gradient Fill Tool**
- Select **two colors** and fill areas with **smooth gradient transitions**.  
- Choose between **linear, radial, or conical gradients**.  

### 🖌️ **Various Brush Tools & Eraser**
Use **pen, eraser, fill tool**, and **adjustable brush size** to customize the drawing experience.  

### 🎥 **Play & Preview Animation**
**Watch animations come to life** instantly using the built-in preview option.  

### 🎬 **Set FPS (Frames Per Second)**
Control the **speed of animations** with adjustable **FPS settings**.  

### 🔄 **Toggle UI Panes**
**Show/Hide the Tools & Color Panels** to maximize the drawing space.  

### 📏 **Change Canvas Size**
- Resize the canvas **dynamically** while preserving existing drawings.  
- Choose a **custom width and height** for projects.  

### 💾 **Save & Load Projects**
- **Save unfinished projects** and **continue later**.  
- Files are saved in a **custom `.atap` format** that stores all frames.  

### 📤 **Export Animation as Video**
- Save animations as **MP4 video files**.  
- Share your creations with **friends & family!** 🎥✨  

---

# **Installation (For Developers)**

## 🛠 **Prerequisites**
Make sure you have the following installed on your system:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/) (3.8 or higher)

## 📥 **Installation Steps**
### 🔹 Linux (Ubuntu/Debian)
1. **Update package list** (Recommended to avoid dependency issues):
   ```bash
   sudo apt update
   ```

2. **Install system dependencies**:
   ```bash
   sudo apt install python3-pyqt5 python3-venv ffmpeg
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/arunpranav-at/atap.git
   cd atap
   ```

4. **Create and activate a virtual environment** (Recommended to avoid system Python conflicts):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

### 🔹 macOS
1. **Install Homebrew (if not installed)**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python and PyQt**:
   ```bash
   brew install python3 pyqt ffmpeg
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/arunpranav-at/atap.git
   cd atap
   ```

4. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

### 🔹 Windows
1. **Install Python** (if not installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure you check **"Add Python to PATH"** during installation

2. **Install Git** (if not installed):
   - Download from [git-scm.com](https://git-scm.com/)

3. **Clone the repository**:
   ```powershell
   git clone https://github.com/arunpranav-at/atap.git
   cd atap
   ```

4. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```powershell
   python main.py
   ```

## ❗ **Troubleshooting**
### 🔸 `externally-managed-environment` Error (Linux)
If you encounter an error while running `pip install -r requirements.txt`, try:
```bash
sudo apt update
sudo apt install python3-pyqt5
```
This installs the necessary system dependencies for PyQt5.

### 🔸 `pip` or `venv` Not Found (Linux/macOS)
Ensure Python is installed correctly:
```bash
sudo apt install python3 python3-venv python3-pip  # Ubuntu/Debian
brew install python3                                # macOS
```

### 🔸 Virtual Environment Activation Issues (Windows)
If `venv\Scripts\activate` doesn't work, try:
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```
This allows running scripts in PowerShell temporarily.

### 🔸 Video Exporting Issues (Windows)
If video exporting doesn't work, you may need to install `ffmpeg` manually:

1. **Download `ffmpeg`** from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
2. Add it to your **system PATH** following [this guide](https://www.wikihow.com/Install-FFmpeg-on-Windows).
3. Restart your terminal and check if it's installed by running:

```powershell
ffmpeg -version
```
---

# **Usage**
1. **Open ATAP**
2. **Select a brush** and start drawing.  
3. **Add new frames** to create an animation.  
4. **Adjust FPS** to control playback speed.  
5. **Use Undo/Redo** if needed.  
6. **Resize the canvas** dynamically.  
7. **Preview the animation** before saving.  
8. **Export it as a video** and share! 🎬  

---

# **Contribution**
### 💡 **Want to contribute to ATAP?**  
We welcome **bug fixes, feature improvements, and new ideas!**  

### 🛠 **How to Contribute**
1. **Fork the repository**  
   Click on the **Fork** button at the top right of the repo.  
2. **Clone your forked repository**  
   ```bash
   git clone https://github.com/arunpranav-at/atap.git
   cd atap
   ```
3. **Create a new branch**  
   ```bash
   git checkout -b feature-name
   ```
4. **Make your changes**  
   - Fix a bug 🐞  
   - Improve UI/UX 🎨  
   - Add a new feature ✨  
5. **Test your changes**  
   Ensure everything runs smoothly by testing locally.  
6. **Commit & Push**  
   ```bash
   git add .
   git commit -m "Added feature-name"
   git push origin feature-name
   ```
7. **Create a Pull Request (PR)**  
   - Go to **GitHub → Your Fork → Pull Requests → New PR**  
   - Select `main` as the base branch and `feature-name` as the compare branch.  
   - Describe your changes and submit your PR!  

### ✅ **Contribution Guidelines**
✔ Follow **PEP 8** for Python code.  
✔ Keep **code modular and well-documented**.  
✔ Submit **small, focused PRs** for easy review.  
✔ Be **kind and respectful** in discussions.  

Your contributions **make ATAP better!** 🚀  

---

# **License**
This project is licensed under the **GNU General Public License Version 3 (GPLv3)**.  
You are free to **use, modify, and distribute** this software under the terms of the [GNU GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).  

For more details, see the [LICENSE file](/LICENSE)

---

# **Demo Gif**
![Demo Gif](/assets/demo_gif.gif)

---
