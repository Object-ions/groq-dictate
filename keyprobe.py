# /// script
# requires-python = ">=3.12"
# dependencies = ["pynput"]
# ///
"""
keyprobe — find out how your keyboard reports a given key.

Run with:  uv run keyprobe.py
Then press the key you want to use for push-to-talk. The number after
"keycode" is the value to set as RECORD_KEYCODE in groq_dictate.py.
Press Esc to quit.
"""

from pynput import keyboard


def _describe(key):
    vk = getattr(key, "vk", None)
    if vk is None:
        vk = getattr(getattr(key, "value", None), "vk", None)
    return f"{key!r}  (keycode {vk})"


def on_press(key):
    print(f"PRESS    {_describe(key)}", flush=True)


def on_release(key):
    print(f"RELEASE  {_describe(key)}", flush=True)
    if key == keyboard.Key.esc:
        return False


print("Press the key you want for push-to-talk. Press Esc to quit.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
