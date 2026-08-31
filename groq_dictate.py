# /// script
# requires-python = ">=3.12"
# dependencies = ["groq", "sounddevice", "numpy", "scipy", "pynput", "pyperclip"]
# ///
"""
groq-dictate — push-to-talk speech-to-text for macOS, powered by Groq Whisper.

Long-press the ` / ~ key (top-left, below Esc), speak, release. The audio is
sent to Groq, transcribed, and pasted straight into whatever text field is
focused (browser, editor, chat). A quick tap of the key still types ` or ~
as normal — only a hold longer than LONG_PRESS_SECS triggers recording.

Run with uv (recommended):   uv run groq_dictate.py
Or inside a venv:            python groq_dictate.py
Quit a manual run:          Ctrl-C
"""

import os
import sys
import tempfile
import threading
import time

import numpy as np
import pyperclip
import sounddevice as sd
import Quartz
from scipy.io import wavfile
from pynput import keyboard
from groq import Groq

# ============================ CONFIG ============================
# The push-to-talk key, as a macOS virtual keycode. 50 = the physical
# ` / ~ key on ANSI (US) keyboards. Hold it (with or without Shift) to
# record; a quick tap types the character as usual.
# Run keyprobe.py if you want to find another key's code.
RECORD_KEYCODE = 50

# Hold at least this long to start dictation; shorter presses are
# treated as normal typing of ` / ~.
LONG_PRESS_SECS = 0.35

# Groq model. "whisper-large-v3-turbo" is fast + multilingual.
# Use "whisper-large-v3" for slightly higher accuracy at lower speed.
MODEL = "whisper-large-v3-turbo"

# Pin a language ("en", "he", "es", ...) for better accuracy/latency,
# or leave None to auto-detect (good for mixed-language use).
LANGUAGE = None

# True  = auto-paste into the focused field (needs Accessibility permission).
# False = copy to clipboard only; you paste manually with Cmd+V.
AUTO_PASTE = True

SAMPLE_RATE = 16000  # Whisper's native rate; leave as-is.
# ===============================================================


def _load_api_key():
    """Prefer the GROQ_API_KEY env var; fall back to ~/.groq-dictate/key."""
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key.strip()
    keyfile = os.path.expanduser("~/.groq-dictate/key")
    if os.path.exists(keyfile):
        with open(keyfile) as f:
            return f.read().strip()
    return None


API_KEY = _load_api_key()
client = Groq(api_key=API_KEY) if API_KEY else None

_frames = []
_stream = None
_recording = False
_lock = threading.Lock()


def start_recording():
    global _stream, _frames, _recording
    with _lock:
        if _recording:
            return
        _frames = []
        _recording = True
        _stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            callback=lambda indata, *_: _frames.append(indata.copy()),
        )
        _stream.start()
    print("● recording…", flush=True)


def _close_stream():
    global _stream, _recording
    _recording = False
    if _stream is not None:
        _stream.stop()
        _stream.close()
        _stream = None


def cancel_recording():
    """Short tap: throw the audio away without calling the API."""
    with _lock:
        _close_stream()


def stop_and_transcribe():
    with _lock:
        _close_stream()

        if not _frames:
            print("(no audio captured — hold the key a beat longer)", flush=True)
            return
        audio = np.concatenate(_frames, axis=0)

    # Drop stray taps / silence before hitting the API.
    # Near-silent sub-second clips make Whisper hallucinate "Thank you."
    duration = len(audio) / SAMPLE_RATE
    rms = float(np.sqrt(np.mean(np.square(audio.astype(np.float64)))))
    if duration < 0.4 or rms < 50:
        print(f"(skipped - {duration:.2f}s, level {rms:.0f})", flush=True)
        return

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
    wavfile.write(path, SAMPLE_RATE, audio)

    print("… transcribing", flush=True)
    kwargs = dict(
        file=(os.path.basename(path), open(path, "rb").read()),
        model=MODEL,
        response_format="text",
    )
    if LANGUAGE:
        kwargs["language"] = LANGUAGE

    try:
        text = client.audio.transcriptions.create(**kwargs)
    except Exception as exc:  # noqa: BLE001
        print(f"!! transcription failed: {exc}", flush=True)
        os.remove(path)
        return
    os.remove(path)

    text = (str(text) or "").strip()
    if not text:
        print("(empty transcript)", flush=True)
        return

    pyperclip.copy(text)
    print(f"→ {text}\n", flush=True)

    if AUTO_PASTE:
        time.sleep(0.05)
        kb = keyboard.Controller()
        with kb.pressed(keyboard.Key.cmd):
            kb.press("v")
            kb.release("v")


# ---------------- long-press key interception (macOS) ----------------
# We tap the record key at the CGEvent level so that while it is held
# nothing is typed into the focused app. On a quick tap we replay the
# original key-down/key-up so ` / ~ types exactly as it would have.

_press_time = 0.0
_key_held = False
_pending = []      # copied CGEvents to replay on a short tap
_replaying = False


def _replay(events):
    global _replaying
    _replaying = True
    try:
        for ev in events:
            Quartz.CGEventPost(Quartz.kCGSessionEventTap, ev)
        time.sleep(0.01)
    finally:
        _replaying = False


def _intercept(event_type, event):
    global _press_time, _key_held, _pending
    if event_type not in (Quartz.kCGEventKeyDown, Quartz.kCGEventKeyUp):
        return event
    if _replaying:
        return event
    keycode = Quartz.CGEventGetIntegerValueField(
        event, Quartz.kCGKeyboardEventKeycode
    )
    if keycode != RECORD_KEYCODE:
        return event

    if event_type == Quartz.kCGEventKeyDown:
        if Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventAutorepeat
        ):
            return None  # swallow auto-repeat while holding
        if not _key_held:
            _key_held = True
            _press_time = time.monotonic()
            _pending = [Quartz.CGEventCreateCopy(event)]
            threading.Thread(target=start_recording, daemon=True).start()
        return None

    # key up
    if not _key_held:
        return event
    _key_held = False
    if time.monotonic() - _press_time >= LONG_PRESS_SECS:
        _pending = []
        threading.Thread(target=stop_and_transcribe, daemon=True).start()
    else:
        events = _pending + [Quartz.CGEventCreateCopy(event)]
        _pending = []
        threading.Thread(target=cancel_recording, daemon=True).start()
        threading.Thread(target=_replay, args=(events,), daemon=True).start()
    return None


def main():
    if client is None:
        sys.exit(
            "No Groq API key found.\n"
            "Set it with:  export GROQ_API_KEY='gsk_...'\n"
            "or write it to ~/.groq-dictate/key"
        )
    print(
        "Ready. Long-press the ` / ~ key to record, release to transcribe. "
        "A quick tap types the character as usual. Ctrl-C to quit.",
        flush=True,
    )
    with keyboard.Listener(darwin_intercept=_intercept) as listener:
        listener.join()


if __name__ == "__main__":
    main()
