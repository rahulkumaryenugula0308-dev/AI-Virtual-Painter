# AI Virtual Painter 🎨

An interactive computer vision application that allows users to draw on a virtual canvas using hand gestures in front of a webcam.

## Features

- Real-time hand tracking using MediaPipe.
- Detection of all five fingers.
- Draw using the index finger.
- Select colors using the index and middle fingers.
- Pause drawing using a closed-fist gesture.
- Brush and eraser modes.
- Adjustable brush thickness.
- Clear and save drawings.
- Interactive OpenCV interface.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Navigate into the project folder:

   `cd AI_Virtual_Painter`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Run the application:

   `python main.py`

## Keyboard Controls

| Key | Action |
|---|---|
| E | Eraser |
| B | Brush |
| C | Clear canvas |
| S | Save drawing |
| [ | Decrease brush size |
| ] | Increase brush size |
| Q | Quit application |

## How It Works

The webcam captures real-time video frames. MediaPipe detects hand landmarks, and the application uses finger positions to recognize gestures. OpenCV processes the video frames and displays the drawing canvas.

## Future Improvements

- More reliable gesture recognition.
- Additional drawing tools.
- Undo and redo functionality.
- Background customization.

## Author

Developed as a Computer Vision project using Python.
