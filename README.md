# Virtual Piano

A webcam-controlled virtual piano built with **Python, OpenCV, MediaPipe Hands, and Pygame**.

Virtual Piano Hands uses real-time hand tracking to turn your webcam into a playable piano. The application detects hand landmarks and maps fingertip positions to two circular virtual keyboards, allowing the left and right hands to control separate keyboards.

## Features

- Real-time hand tracking using MediaPipe Hands
- Webcam input through OpenCV
- Two independent circular keyboards
- Left-hand and right-hand keyboard control
- 12 chromatic notes per keyboard
- Fingertip-based key detection
- Multiple-finger and chord support
- Visual hand landmark tracking
- Key hover and press animations
- Sample-based piano audio
- Modular Python architecture

## Tech Stack

- **Python**
- **OpenCV** — webcam capture and frame processing
- **MediaPipe** — real-time hand landmark detection
- **Pygame** — rendering and audio playback
- **NumPy** — numerical and image-processing operations

## How It Works

```text
              Webcam
                 │
                 ▼
          OpenCV Capture
                 │
                 ▼
          MediaPipe Hands
                 │
          ┌──────┴──────┐
          ▼             ▼
      Left Hand     Right Hand
          │             │
          ▼             ▼
   Left Keyboard   Right Keyboard
          │             │
          └──────┬──────┘
                 ▼
          Key Detection
                 │
                 ▼
           Audio Engine
                 │
                 ▼
         Visual Feedback
```

Each circular keyboard contains 12 chromatic notes:

```text
C  C#  D  D#  E  F  F#  G  G#  A  A#  B
```

The application calculates the position of each detected fingertip relative to the keyboard and determines which sector of the circular keyboard it occupies.

## Project Structure

```text
VirtualPianoHands/
│
├── app.py
│
├── assets/
│   └── ...
│
├── config/
│   └── ...
│
├── src/
│   ├── audio/
│   ├── camera/
│   ├── core/
│   ├── graphics/
│   ├── piano/
│   ├── tracking/
│   └── utils/
│
├── tools/
│   └── ...
│
├── tests/
│   └── ...
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/thekarnik-aaryan/virtual-piano.git
cd VirtualPianoHands
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Make sure your webcam is available and allow camera access if your operating system asks for permission.

## Controls

The application is primarily controlled through hand movements:

| Input | Action |
|---|---|
| Left hand | Controls left keyboard |
| Right hand | Controls right keyboard |
| Fingertips | Activate virtual keys |
| Multiple fingertips | Play multiple notes/chords |

## Requirements

- Python 3.10+
- Working webcam
- Microphone is **not** required
- Audio output
- Adequate lighting for reliable hand tracking

Performance may vary depending on webcam resolution, lighting conditions, CPU/GPU performance, and MediaPipe tracking quality.

## Known Limitations

- Hand tracking can become less reliable with poor lighting or heavily occluded fingers.
- Audio latency depends on the local system and audio backend.
- Keyboard positioning is currently based on the application's configured window layout.
- The project is currently designed as an interactive desktop prototype.

## Future Improvements

- MIDI output support
- Sustain/pedal support
- Adjustable octaves
- User-configurable keyboard layouts
- Custom audio samples
- Piano recording and playback
- Improved gesture recognition
- Performance optimization
- Automated unit and integration tests

## Development

Create your own virtual environment when working on the project:

```bash
python -m venv .venv
```

The virtual environment should **not** be committed to GitHub. The included `.gitignore` already excludes it.

Install dependencies with:

```bash
pip install -r requirements.txt

later usage command key : 
.venv\Scripts\activate
python app.py
```
Later usage command key :
```bash
.venv\Scripts\activate
python app.py
```
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
