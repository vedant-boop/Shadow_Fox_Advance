import cv2
import mediapipe as mp
import pyautogui
import random
import util
from pynput.mouse import Button, Controller
import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice

engine.setProperty('voice', voices[0].id)    #0-male... 1-female
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

mouse = Controller()


screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x*screen_width)
        y = int(index_finger_tip.y /2*screen_height)
        pyautogui.moveTo(x, y)


def is_left_click(landmark_list, thumb_index_dist):
    if  (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50
        ):
        speak("Left click detected")
        return True
    return False


def is_right_click(landmark_list, thumb_index_dist):
    if(
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and
        thumb_index_dist > 50
        ):
        speak("Right click detected")
        return True
    return False
    

def is_double_click(landmark_list, thumb_index_dist):
    if(
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
        ):
        speak("Double click detected")
        return True
    return False



def is_screenshot(landmark_list, thumb_index_dist):
    if (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
        ):
        speak("Screenshot clicked")
        return True
    return False


def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:

        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if util.get_distance([landmark_list[4], landmark_list[5]]) < 50  and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list,  thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list,thumb_index_dist ):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


# def main():
#     draw = mp.solutions.drawing_utils
#     cap = cv2.VideoCapture(0)

#     try:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame = cv2.flip(frame, 1)
#             frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             processed = hands.process(frameRGB)

#             landmark_list = []
#             if processed.multi_hand_landmarks:
#                 hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
#                 draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
#                 for lm in hand_landmarks.landmark:
#                     landmark_list.append((lm.x, lm.y))

#             detect_gesture(frame, landmark_list, processed)

#             cv2.imshow('Frame', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()



def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    landmark_list.append((lm.x, lm.y))

                    if id == 8:  # Index fingertip
                        x = int(lm.x * frame_width)
                        y = int(lm.y * frame_height)

                        # Draw concentric white circles
                        for r in range(25, 14, -1):  # From radius 25 to 15
                            cv2.circle(img=frame, center=(x, y), radius=r, color=(255, 255, 255), thickness=1)

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return landmark_list





    # cap = cv2.VideoCapture(0)
    # hand_detector = mp.solutions.hands.Hands()
    # drawing_utils = mp.solutions.drawing_utils
    # screen_width, screen_height = pyautogui.size()
    # index_y = 0

    # while True:
    #     _, frame = cap.read()
    #     frame = cv2.flip(frame, 1)
    #     frame_height, frame_width, _ = frame.shape

    #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     output = hand_detector.process(rgb_frame)
    #     hands = output.multi_hand_landmarks

    #     if hands:
    #         for hand in hands:
    #             drawing_utils.draw_landmarks(frame, hand)
    #             landmarks = hand.landmark

    #             for id, landmark in enumerate(landmarks):
    #                 x = int(landmark.x * frame_width)
    #                 y = int(landmark.y * frame_height)

    #                 if id ==8:
    #                     cv2.circle(img=frame, center=(x,y), radius=25, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=24, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=20, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=19, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=18, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=17, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=16, color=(255,255,255))
    #                     cv2.circle(img=frame, center=(x,y), radius=15, color=(255,255,255))
    #                     index_x = int(screen_width/frame_width*x)
    #                     index_y =int(screen_height/frame_height*y)
    #                     pyautogui.moveTo(index_x,index_y)
    #                 if id == 4:
    #                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
    #                     thumb_x = int(screen_width/frame_width*x)
    #                     thumb_y = int(screen_height/frame_height*y)
    #                     # print('max',abs(index_y - thumb_y))
    #                     if abs(index_y - thumb_y) < 80:
    #                         pyautogui.click()
    #                 if id == 20:
    #                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
    #                     right_x = screen_width/frame_width*x
    #                     right_y = screen_height/frame_height*y
    #                     # print('min',abs(thumb_y - right_y))



    #     cv2.imshow('Virtual Mouse', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()

drawing = False
draw_points = []



def is_drawing_gesture(landmark_list):
    if len(landmark_list) < 21:
        return False
    # Check if index, middle, and ring fingers are extended
    angles = [
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]),    # Index
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]),  # Middle
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])  # Ring
    ]
    return all(angle < 50 for angle in angles)



def detect_gesture(frame, landmark_list, processed):
    global drawing, draw_points

    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if is_drawing_gesture(landmark_list):
            drawing = True
            if index_finger_tip:
                x = int(index_finger_tip.x * screen_width)
                y = int(index_finger_tip.y * screen_height)
                draw_points.append((x, y))
                cv2.putText(frame, "Drawing...", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            drawing = False

        if drawing:
            for i in range(1, len(draw_points)):
                cv2.line(frame, draw_points[i - 1], draw_points[i], (0, 255, 255), 3)

        elif thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50,                                                                                                                                                                                                                                                                                                                                  50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)






if __name__ == '__main__':
    main()




