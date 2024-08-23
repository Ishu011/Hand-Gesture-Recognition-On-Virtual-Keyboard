# Hand-Gesture-Recognition-On-Virtual-Keyboard
# Virtual Keyboard with Hand Gesture Recognition

## Overview

This project implements a virtual keyboard using hand gesture recognition. It leverages OpenCV and MediaPipe to track hand movements and map them to keyboard inputs. The keyboard supports basic functionality, including shift and caps lock, and provides sentence suggestions based on user input.

## Features

- **Real-Time Hand Gesture Tracking:** Uses MediaPipe for hand tracking and OpenCV for rendering.
- **Virtual Keyboard:** A graphical virtual keyboard with keys for typing.
- **Sentence Suggestions:** Provides predefined sentence suggestions based on the typed input.
- **Shift and Caps Lock:** Supports shift and caps lock functionalities.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Ishu011/virtual-keyboard-hand-gesture-recognition.git
    ```

2. Navigate to the project directory:

    ```bash
    cd virtual-keyboard-hand-gesture-recognition
    ```

3. Install the required dependencies:

    ```bash
    pip install opencv-python mediapipe numpy
    ```

## Usage

1. Run the Python script:

    ```bash
    python hand_gesture_recognition_on_virtual_keyboard.py
    ```

2. Use hand gestures to interact with the virtual keyboard displayed in the video feed.

## Example

The virtual keyboard displays on your screen, and you can type using hand gestures. The application will suggest sentences based on the typed words.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenCV](https://opencv.org/) for computer vision tools.
- [MediaPipe](https://mediapipe.dev/) for hand tracking solutions.
