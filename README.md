# 🧤🚗 Glove Shift: Drive with Your Hands!

<p>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/></a>
  <a href="https://developers.google.com/mediapipe"><img src="https://img.shields.io/badge/MediaPipe-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe"/></a>
</p>

**Experience a whole new level of racing immersion with Glove Shift!** This hand gesture recognition system lets you control your racing game's car intuitively, **controlling speed and navigating turns with just your hands**. It's open-source, customizable, and brings a **fun and unique twist to your virtual driving adventures**. [Check out the demostration video on LinkedIn.](https://www.linkedin.com/posts/bushaangunatilake_racinggames-handgesturerecognition-computervision-activity-7187445360850616320-A-6p?utm_source=share&utm_medium=member_desktop)

---

## ✨ Features

* **Gesture-based control:** Master the racetrack using intuitive hand gestures for acceleration, braking, steering, and reverse.
* **No complex setup:** Just install and run. No extra calibration or coding required.
* **Universal game compatibility:** Works with any racing game, no special integrations needed.  

---

## ⚙ Technologies Used

* [Python](https://www.python.org/)
* [Open Source Computer Vision Library (OpenCV)](https://opencv.org/) 
* [MediaPipe](https://developers.google.com/mediapipe) (for efficient hand detection and pose estimation)

---

## 📦 Installation (End Users)

- **Option 1 — Installer (recommended)**

  1. Download the latest `GloveShift-Setup.exe` from the Releases.
  2. Run the installer.
  3. Launch `GloveShift.exe` and let it run in the background.
  4. If an error occurs, install the Visual C++ Redistributable 2015–2022 (both x64 and x86 versions are included in the release).
  5. Open your racing game and make sure the driving controls are mapped to W (accelerate), A (left), S (brake/reverse), and D (right) for proper gesture control.
  6. Have Fun !

- **Option 2 — Portable version**

  1. Download `GloveShift-Portable.exe`.
  2. Run directly (no installation required).


> [!NOTE]
> The portable version (Option 2) is *plug-and-play*. It **does not** create a desktop shortcut, will **not** appear in *Add/Remove Programs*, and has **no** uninstaller. The installer (Option 1) does create shortcuts and an uninstall entry.

  
### 🖥 Requirements
- Windows 10/11 (64-bit recommended)
- Webcam (for gesture recognition)
- Visual C++ Redistributable 2015–2022 (included in release)

--- 

## 🧑‍💻 Installation (Developers)

Want to hack on the code? Use this setup:
1. Ensure you have Python 3 installed (https://www.python.org/downloads/).
2. Clone or download the project repository.
```bash
git clone https://github.com/BUSHAAN/Glove-Shift.git
```
3. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

4.  Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

5. Run the application
```bash
python app.py
```

---

## 🔨 Build from Source
To build the standalone EXE and the Windows installer, follow the step-by-step guide:

See: [Build and Package (Windows)](README-BUILD.md)

---

## Gesture Controls for the application... Have Fun!!!
<img src="images/Gesture_Controls.png?raw=true" height="400">

> [!NOTE]
> This application currently uses right-hand gestures for optimal control. Left hand functionalities will be added soon.
--- 

## 🤝 Contributing

We welcome contributions to improve **Glove Shift** and make virtual racing with hand gestures even more fun and accessible! 🚗💨

- **Current focus areas:**
  - Improving gesture detection accuracy and stability.
  - Enhancing the PyQt6 interface (usability, design, error handling).
  - Expanding cross-platform compatibility (Windows/Linux).
  - Packaging improvements (PyInstaller/Inno Setup).

- **How to contribute:**
  1. Fork the repository.
  2. Create a new branch:  
     ```bash
     git checkout -b feature-name
     ```
  3. Make your changes and commit:  
     ```bash
     git commit -m "Added new feature/fix"
     ```
  4. Push your branch and open a Pull Request:  
     ```bash
     git push origin feature-name
     ```

- **Guidelines:**
  - Please test your changes locally before submitting.
  - For major updates, open an issue first to discuss your proposal.
  - Stick to existing code style and keep commits clear and concise.

