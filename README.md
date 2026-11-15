# AI Virtual Painter 🎨

A real-time hand gesture-based virtual painting application built using Python, OpenCV, and MediaPipe.

Draw on a virtual canvas using your fingers without touching your computer screen!

## 🚀 Features

- Real-time hand tracking using MediaPipe.
- Detects 21 hand landmarks.
- Draw using your index finger.
- Select drawing colors using a two-finger gesture.
- Pause drawing using a closed-fist gesture.
- Switch between brush and eraser.
- Adjust brush thickness.
- Clear the canvas.
- Save your drawings as images.

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/rahulkumaryenugula0308-dev/AI-Virtual-Painter.git
   ```

2. Navigate to the project folder:

   ```bash
   cd AI-Virtual-Painter
   ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## 🎮 Controls

| Gesture / Key | Action |
|---|---|
| Index finger | Draw |
| Index + Middle fingers | Select color |
| Closed fist | Pause drawing |
| B | Brush |
| E | Eraser |
| C | Clear canvas |
| S | Save drawing |
| [ | Decrease brush size |
| ] | Increase brush size |
| Q | Quit application |

## 📂 Project Structure

```text
AI-Virtual-Painter/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── output/
```

## 🎯 Learning Outcomes

- Real-time computer vision application development.
- Hand landmark detection and tracking.
- Gesture recognition.
- Image processing using OpenCV.
- Working with MediaPipe.

## 👨‍💻 Author

Developed as a hands-on Computer Vision project using Python.