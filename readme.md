🎹 Hand Tracking MIDI Piano
Play virtual piano notes using hand gestures via a webcam, OpenCV, and Pygame MIDI.

📝 Description
This project allows users to play simple piano notes using hand gestures. The system detects hand and finger movements through OpenCV and cvzone and maps them to corresponding MIDI piano notes. You can choose from 128 different MIDI instruments before starting, making it a versatile tool for gesture-based music interaction.

🎯 Features
✅ Play C Major Scale (C, D, E, F, G, A, B, C) using finger movements.
✅ Select from 128 MIDI instruments (Piano, Guitar, Violin, Trumpet, etc.).
✅ Uses OpenCV + MediaPipe for real-time hand tracking.
✅ Dynamic note sustain (keeps playing for a short time after lowering a finger).
✅ Multi-threaded execution for smooth performance.
✅ Works with both hands (left-hand plays lower notes, right-hand plays higher notes).

💻 How It Works
Select an instrument from the list at startup.

Start the webcam: It detects your hand gestures.

Raise fingers to play corresponding notes.

Lower fingers to stop notes (with slight sustain delay).

Press 'Q' to exit the program.

🎵 Note Mapping
Finger	Left Hand (Low Notes)	Right Hand (High Notes)
Thumb	C4 (60)	A4 (69)
Index	D4 (62)	B4 (71)
Middle	E4 (64)	C5 (72)
Ring	F4 (65)	D5 (74)
Pinky	G4 (67)	E5 (76)
🛠 Installation & Setup
🔹 1. Install Dependencies
Make sure you have Python installed (Python 3.7+ recommended). Then, install required libraries:

sh
Copy
Edit
pip install opencv-python pygame cvzone
pip install mediapipe
🔹 2. Run the Script
sh
Copy
Edit
python hand_tracking_piano.py
🚀 Code Overview
📌 Main Components
MIDI Initialization (pygame.midi)

Initializes MIDI player.

Allows user to choose an instrument from 128 options.

Starts MIDI playback.

Hand Tracking (cvzone.HandTrackingModule)

Uses OpenCV & MediaPipe to detect hands.

Identifies which fingers are raised.

Playing Notes (pygame.midi.note_on)

Each raised finger triggers a note.

The note stops when the finger is lowered after a short delay.
