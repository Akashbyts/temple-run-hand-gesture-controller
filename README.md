# 🎮 Temple Run Hand Gesture Controller

Control the Temple Run game using your hand gestures via your webcam!

This AI project uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to detect palm direction and simulate keyboard controls. Great for AI/ML project demos or college submissions.

---

## 🛠 Technologies Used
- Python
- OpenCV
- MediaPipe (hand tracking)
- PyAutoGUI (keyboard simulation)

---

## 💡 Features

| Gesture         | Action          |
|----------------|------------------|
| Swipe Left      | Move Left (←)    |
| Swipe Right     | Move Right (→)   |
| Swipe Up        | Jump (↑)         |
| Swipe Down      | Slide (↓)        |
| ✊ Fist (Closed) | Pause/Resume (␣) |

---

## 🧠 How It Works

- Detects hand using MediaPipe’s 21 landmarks
- Tracks palm movement direction across multiple frames
- Triggers keyboard keys via PyAutoGUI based on movement
- Uses finger counting logic to detect fist and press space

---

## 📦 Installation

```bash
pip install -r requirements.txt

