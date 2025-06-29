# import cv2
# import mediapipe as mp
# import pyttsx3
# import speech_recognition as sr

# # Initialize components
# engine = pyttsx3.init()
# recognizer = sr.Recognizer()
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()

# def listen_command():
#     with sr.Microphone() as source:
#         print("Say something...")
#         audio = recognizer.listen(source)
#     try:
#         command = recognizer.recognize_google(audio)
#         print(f"You said: {command}")
#         return command
#     except sr.UnknownValueError:
#         return None

# def give_feedback(text):
#     print(f"Feedback: {text}")
#     engine.say(text)
#     engine.runAndWait()

# def main():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         # Gesture recognition logic here
#         # For demo, just show the video
#         cv2.imshow('Gesture Controller', frame)

#         # Example: listen for voice command on pressing 'v'
#         if cv2.waitKey(1) & 0xFF == ord('v'):
#             cmd = listen_command()
#             if cmd:
#                 if "hello" in cmd.lower():
#                     give_feedback("Hello! How can I help you?")
#                 # Add NLU parsing and action logic here

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()