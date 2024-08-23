import cv2
import mediapipe as mp
import numpy as np
import time


class Button:
    def __init__(self, pos, width, height, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, font_thickness=2):
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_scale = font_scale
        self.font_thickness = font_thickness
        self.is_pressed = False
        self.was_activated = False

    def draw(self, frame, transparency=0.5):
        x, y = self.pos
        overlay = frame.copy()
        color = (0, 255, 0) if self.is_pressed else (255, 0, 0)
        cv2.rectangle(overlay, self.pos, (x + self.width, y + self.height), color, -1)
        cv2.addWeighted(overlay, transparency, frame, 1 - transparency, 0, frame)

        text_size = cv2.getTextSize(self.text, self.font, self.font_scale, self.font_thickness)[0]
        text_x = x + (self.width - text_size[0]) // 2
        text_y = y + (self.height + text_size[1]) // 2
        cv2.putText(frame, self.text, (text_x, text_y), self.font, self.font_scale, (255, 255, 255),
                    self.font_thickness)

    def is_hovered(self, finger_tip, tolerance=10):
        x, y = self.pos
        return x - tolerance < finger_tip[0] < x + self.width + tolerance and y - tolerance < finger_tip[
            1] < y + self.height + tolerance


class VirtualKeyboard:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.buttons = self.create_keyboard()
        self.suggestion_buttons = self.create_suggestion_buttons()
        self.typed_text = ""
        self.is_shift_active = False
        self.is_caps_active = False
        self.is_hand_open = True

    def create_keyboard(self):
        button_list = []
        keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Shift', 'Caps']
        ]
        start_x, start_y = 50, 200
        button_width, button_height = 60, 60
        gap = 10

        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                x = start_x + col_index * (button_width + gap)
                y = start_y + row_index * (button_height + gap)
                button_list.append(Button((x, y), button_width, button_height, key))

        return button_list

    def create_suggestion_buttons(self):
        suggestions = ["Hello", "How", "Are", "You"]
        suggestion_buttons = []
        start_x, start_y = 50, 100
        button_width, button_height = 300, 60
        gap = 10

        for index, sentence in enumerate(suggestions):
            x = start_x + index * (button_width + gap)
            y = start_y
            suggestion_buttons.append(Button((x, y), button_width, button_height, sentence))

        return suggestion_buttons

    def update_suggestions(self):

        if "Hii" in self.typed_text:
            suggestions = [
                "Hii my name is Ishu-Parul and we are from IGDTUW",
                "Hii my name is Ishu-Parul and I love programming",
                "Hii my name is Ishu-Parul and I study at IGDTUW"
            ]
        elif "Hello" in self.typed_text:
            suggestions = [
                "Hello, how are you?",
                "Hello, what are you doing?",
                "Hello, where are you from?"
            ]
        else:
            suggestions = [
                "Hii my name is Ishu-Parul and we are from IGDTUW",
                "Hello, how are you?",
                "How can I help you today?"
            ]

        for i, button in enumerate(self.suggestion_buttons):
            button.text = suggestions[i] if i < len(suggestions) else ""

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture image")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            for button in self.buttons:
                button.draw(frame)

            for button in self.suggestion_buttons:
                button.draw(frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    finger_tip = self.get_finger_tip_position(hand_landmarks, frame)
                    self.is_hand_open = self.check_hand_open(hand_landmarks)

                    for button in self.buttons:
                        if button.is_hovered(finger_tip):
                            if self.is_hand_open and not button.was_activated:
                                button.is_pressed = True
                                self.handle_key_press(button.text)
                                button.was_activated = True
                            break
                        else:
                            button.is_pressed = False
                            button.was_activated = False

                    for button in self.suggestion_buttons:
                        if button.is_hovered(finger_tip):
                            if self.is_hand_open and not button.was_activated:
                                button.is_pressed = True
                                self.typed_text += f" {button.text}"
                                print(f"Typed Text: {self.typed_text}")
                                button.was_activated = True
                            break
                        else:
                            button.is_pressed = False
                            button.was_activated = False

            cv2.imshow("Virtual Keyboard - Ishu", frame)  # Updated to include your name

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def handle_key_press(self, key):
        if key == 'Shift':
            self.is_shift_active = not self.is_shift_active
        elif key == 'Caps':
            self.is_caps_active = not self.is_caps_active
        else:
            if self.is_shift_active or self.is_caps_active:
                key = key.upper()
            else:
                key = key.lower()

            self.typed_text += key
            print(f"Typed Text: {self.typed_text}")

            # Introduce a delay before updating suggestions
            time.sleep(0.2)
            self.update_suggestions()

        if self.is_shift_active:
            self.is_shift_active = False

    @staticmethod
    def get_finger_tip_position(hand_landmarks, frame):
        height, width, _ = frame.shape
        x = int(hand_landmarks.landmark[8].x * width)
        y = int(hand_landmarks.landmark[8].y * height)
        return (x, y)

    @staticmethod
    def check_hand_open(hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        distances = [
            np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y])),
            np.linalg.norm(np.array([index_tip.x, index_tip.y]) - np.array([middle_tip.x, middle_tip.y])),
            np.linalg.norm(np.array([middle_tip.x, middle_tip.y]) - np.array([ring_tip.x, ring_tip.y])),
            np.linalg.norm(np.array([ring_tip.x, ring_tip.y]) - np.array([pinky_tip.x, pinky_tip.y]))
        ]

        return all(distance > 0.1 for distance in distances)


if __name__ == "__main__":
    virtual_keyboard = VirtualKeyboard()
    virtual_keyboard.run()
