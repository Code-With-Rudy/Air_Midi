import cv2
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

# 🎹 Initialize Pygame MIDI
pygame.midi.init()

# 🎵 List of MIDI Instruments (0-127)
instruments = {
    0: "Acoustic Grand Piano", 30: "Distortion Guitar", 40: "Violin", 56: "Trumpet", 
    73: "Flute", 81: "Lead 2 (Sawtooth)", 90: "Pad 2 (Warm)", 121: "FX 5 (Brightness)"
}

# 🎛️ Select Instrument
def select_instrument():
    print("Available Instruments:")
    for num, name in instruments.items():
        print(f"{num}: {name}")
    
    while True:
        try:
            choice = int(input("Enter the instrument number (0-127): "))
            if 0 <= choice <= 127:
                return choice
            else:
                print("Invalid choice. Enter a number between 0-127.")
        except ValueError:
            print("Invalid input. Please enter a number.")

instrument_choice = select_instrument()
player = pygame.midi.Output(0)
player.set_instrument(instrument_choice)

# 🎐 Initialize Hand Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

# 🎼 Piano Notes (C Major Scale - Middle Octave)
notes = {
    "left": {
        "thumb": 60,   # C4
        "index": 62,   # D4
        "middle": 64,  # E4
        "ring": 65,    # F4
        "pinky": 67    # G4
    },
    "right": {
        "thumb": 69,   # A4
        "index": 71,   # B4
        "middle": 72,  # C5
        "ring": 74,    # D5
        "pinky": 76    # E5
    }
}

# Sustain Time (in seconds) after the finger is lowered
SUSTAIN_TIME = 0.5

# Track Previous States to Stop Notes
prev_states = {hand: {finger: 0 for finger in notes[hand]} for hand in notes}

# 🎵 Function to Play a Note
def play_note(note):
    player.note_on(note, 127)  # Start playing

# 🎵 Function to Stop a Note After a Delay
def stop_note_after_delay(note):
    time.sleep(SUSTAIN_TIME)  # Sustain for specified time
    player.note_off(note, 127)  # Stop playing

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera not capturing frames")
        continue

    hands, img = detector.findHands(img, draw=True)

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):
                if finger in notes[hand_type]:  # Only check assigned notes
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        play_note(notes[hand_type][finger])  # Play note
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        threading.Thread(target=stop_note_after_delay, args=(notes[hand_type][finger],), daemon=True).start()
                    prev_states[hand_type][finger] = fingers[i]  # Update state
    else:
        # If no hands detected, stop all notes after delay
        for hand in notes:
            for finger in notes[hand]:
                threading.Thread(target=stop_note_after_delay, args=(notes[hand][finger],), daemon=True).start()
        prev_states = {hand: {finger: 0 for finger in notes[hand]} for hand in notes}

    cv2.imshow("Hand Tracking MIDI Piano", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.midi.quit()