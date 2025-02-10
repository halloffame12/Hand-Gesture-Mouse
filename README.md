# Hand Gesture Mouse

## 📌 Overview
The **Hand Gesture Mouse** allows users to control their mouse using hand gestures via a webcam. It utilizes **MediaPipe Hands, OpenCV, and PyAutoGUI** to track hand movements and execute mouse actions like clicking, scrolling, dragging, and window switching.

---

## 🚀 Features
✅ **Mouse movement** using index finger tracking  
✅ **Clicking & Right-Clicking** via thumb and finger gestures  
✅ **Scrolling** with finger positioning  
✅ **Drag-and-drop** functionality  
✅ **Zoom in/out** with pinch gestures  
✅ **Window switching** via swipe gestures  

---

## 📂 Installation
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/halloffame12/Hand-Gesture-Mouse.git
cd Hand-Gesture-Mouse
```

### 2️⃣ **Install Dependencies**
Ensure you have Python installed, then run:
```bash
pip install opencv-python mediapipe numpy pyautogui
```

---

## 🎯 How It Works
### 🔹 1. **Importing Libraries**
```python
import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
```
- **OpenCV (cv2)** → Captures video from the webcam  
- **NumPy** → Performs numerical calculations  
- **MediaPipe** → Detects and tracks hand landmarks  
- **PyAutoGUI** → Controls mouse actions  

### 🔹 2. **Hand Tracking with MediaPipe**
```python
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
```
- Detects hand position with **70% confidence**  
- Tracks up to **two hands** for gestures like swiping  

### 🔹 3. **Mapping Hand to Cursor Movement**
```python
x, y = int(index_tip.x * w), int(index_tip.y * h)
screen_x = np.interp(x, [0, w], [0, screen_width])
screen_y = np.interp(y, [0, h], [0, screen_height])
pyautogui.moveTo(screen_x, screen_y, duration=0.05)
```
- Converts hand position to **screen coordinates**  
- **Smooths movement** to avoid cursor jumps  

### 🔹 4. **Gesture Controls**
✅ **Click** → Thumb and index finger close together  
✅ **Right-Click** → Thumb and middle finger close  
✅ **Scrolling** → Index & middle finger position  
✅ **Drag & Drop** → Holding thumb & index close  
✅ **Zoom** → Pinch open (zoom in) / Pinch close (zoom out)  
✅ **Swipe Gesture** → Moves between windows (Alt + Tab)  

### 🔹 5. **Stopping the Program**
```python
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```
- Press **'q'** to exit the program  

---



## ⚡ Usage
1. **Run the script**
   ```bash
   python hand_gesture_mouse.py
   ```
2. **Ensure your webcam is working**
3. **Use hand gestures to control the mouse**
4. **Press 'q' to exit**

---

## 🛠️ Customization
- Adjust **gesture sensitivity** in `click_threshold` values  
- Modify **cursor speed** via `smoothing_factor`  
- Add **new gestures** for more interactions  

---

## 🤝 Contributing
Pull requests are welcome! Feel free to **improve the code** or **add new features**. If you find a bug, open an issue.

---

## 📜 License
This project is licensed under the **APACHE 2.0**.

---

### 📧 Contact
For questions or collaborations, reach out at **sumitchauhan10062004@gmail.com** or visit [Your GitHub](https://github.com/halloffame12).
