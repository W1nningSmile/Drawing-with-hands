# Drawing-with-hands

This project uses your webcam to track your hand, and when you pinch your thumb and index finger together, it draws a rainbow line on the screen.

Made for Champlain St-Lambert's 2026 open house and will be presented by Champain's Robotics Club.

## How it works

- **OpenCV** captures video from the webcam and displays it.
- **MediaPipe Hands** finds landmarks on your hand in each frame.
- When the distance between your thumb tip and index finger tip drops below a certain distance, it counts as a pinch and the midpoint between them becomes the "pen".
- Strokes are drawn on a separate canvas and overlaid on the live video so they stay on screen.
- There are a few premade brush colors that can be changed in the code.


## Controls

| Key | Action |
|-----|--------|
| Pinching | Draw |
| `c` | Clears the canvas |
| `p` | Save a photo as `frame.png` |
| `q` | Quit |


## Possible improvements

- Color picker and brush size controls
- Eraser gesture

## Built with

- OpenCV
- MediaPipe
- NumPy
