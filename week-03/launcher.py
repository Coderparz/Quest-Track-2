# Bongo Dog desktop pet
# Run while building:  python launcher.py
# Double-click start:  Bongo Dog.pyw
#
# Privacy rule: we only COUNT key presses for QP.
# We never save or show WHICH keys were typed.

import math
import queue
import struct
import time
import tkinter as tk
import wave
import winsound
from pathlib import Path

try:
    from pynput import keyboard  # lets us notice typing in ANY app
except ImportError:
    keyboard = None  # not installed: typing only works when our window is selected

HERE = Path(__file__).parent
ART = HERE / "art"
SOUNDS = HERE / "sounds"

KEY_COLOR = "#010203"   # this exact color becomes see-through around the dog
SLEEP_AFTER = 10        # seconds without typing before the dog falls asleep
HIT_TIME = 110          # ms a paw stays down after a key press
DRAG_START = 6          # px the mouse must move before a click becomes a drag

# The little beat: (pose, sound, how long in ms)  "bom-bom-ba-BOM!" then ta-da
BEAT = [
    ("left",  "bom", 260),
    ("right", "bom", 260),
    ("left",  "ba",  170),
    ("right", "boom", 420),
    ("ready", None,  800),
]


# ---------- sounds (made with Python, no downloads) ----------

def make_drum(path, pitch, length, volume):
    """Write a short drum hit .wav: a low tone that drops in pitch and fades out."""
    rate = 22050
    frames = bytearray()
    phase = 0.0
    for i in range(int(rate * length)):
        t = i / rate
        freq = pitch * (0.5 + 0.5 * math.exp(-t * 18))  # pitch drops quickly
        phase += 2 * math.pi * freq / rate
        amp = volume * math.exp(-t * 9)                   # sound fades out
        frames += struct.pack("<h", int(amp * 32767 * math.sin(phase)))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))


def ensure_sounds():
    SOUNDS.mkdir(exist_ok=True)
    recipes = {"bom": (180, 0.30, 0.7), "ba": (260, 0.18, 0.6), "boom": (130, 0.50, 0.95)}
    for name, (pitch, length, volume) in recipes.items():
        path = SOUNDS / f"{name}.wav"
        if not path.exists():
            make_drum(path, pitch, length, volume)


def play(name):
    winsound.PlaySound(str(SOUNDS / f"{name}.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)


# ---------- the pet ----------

class Pet:
    def __init__(self, root, on_key):
        self.root = root
        self.on_key = on_key  # tells the launcher to add 1 to QP

        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)            # no border / title bar
        self.win.attributes("-topmost", True)      # stay on top of other apps
        self.win.config(bg=KEY_COLOR)
        self.win.attributes("-transparentcolor", KEY_COLOR)

        self.poses = {n: tk.PhotoImage(file=ART / f"{n}.png")
                      for n in ("ready", "left", "right", "sleep")}
        self.label = tk.Label(self.win, image=self.poses["ready"], bg=KEY_COLOR, bd=0)
        self.label.pack()

        size = self.poses["ready"].width()
        self.home_x = root.winfo_screenwidth() - size - 20
        self.home_y = root.winfo_screenheight() - size - 60   # above the taskbar
        self.x, self.y = self.home_x, self.home_y
        self.move_to(self.x, self.y)

        self.next_paw = "left"
        self.busy = False        # playing the click beat
        self.dragging = False
        self.sleeping = False
        self.last_active = time.time()
        self.hit_job = None
        self.alive = True

        # mouse
        self.label.bind("<ButtonPress-1>", self.mouse_down)
        self.label.bind("<B1-Motion>", self.mouse_move)
        self.label.bind("<ButtonRelease-1>", self.mouse_up)
        self.menu = tk.Menu(self.win, tearoff=0)
        self.menu.add_command(label="Quit", command=self.quit)
        self.label.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))

        self.check_sleep()

    # --- helpers ---
    def show(self, pose):
        self.label.config(image=self.poses[pose])

    def move_to(self, x, y):
        self.x, self.y = int(x), int(y)
        self.win.geometry(f"+{self.x}+{self.y}")

    def wake(self):
        self.last_active = time.time()
        if self.sleeping:
            self.sleeping = False
            self.show("ready")

    # --- typing ---
    def key_hit(self):
        self.on_key()
        self.wake()
        if self.busy or self.dragging:
            return
        self.show(self.next_paw)
        self.next_paw = "right" if self.next_paw == "left" else "left"
        if self.hit_job:
            self.root.after_cancel(self.hit_job)
        self.hit_job = self.root.after(HIT_TIME, lambda: self.alive and self.show("ready"))

    # --- sleeping ---
    def check_sleep(self):
        if not self.alive:
            return
        idle = time.time() - self.last_active
        if idle > SLEEP_AFTER and not (self.busy or self.dragging or self.sleeping):
            self.sleeping = True
            self.show("sleep")
        self.root.after(500, self.check_sleep)

    # --- mouse: click = beat, drag = pick up ---
    def mouse_down(self, e):
        self.press_at = (e.x_root, e.y_root)
        self.grab_offset = (e.x_root - self.x, e.y_root - self.y)
        self.dragging = False

    def mouse_move(self, e):
        if not self.dragging:
            dx, dy = e.x_root - self.press_at[0], e.y_root - self.press_at[1]
            if abs(dx) < DRAG_START and abs(dy) < DRAG_START:
                return
            if self.busy:
                return
            self.dragging = True
            self.wake()
            self.show("ready")   # "whoa, I'm being picked up!"
        self.move_to(e.x_root - self.grab_offset[0], e.y_root - self.grab_offset[1])

    def mouse_up(self, e):
        if self.dragging:
            self.slide_home()
        elif not self.busy:
            self.wake()
            self.play_beat(0)

    def slide_home(self, step=0, start=None):
        steps = 30
        if start is None:
            start = (self.x, self.y)
        t = (step + 1) / steps
        ease = 1 - (1 - t) ** 3   # fast at first, slow at the end
        self.move_to(start[0] + (self.home_x - start[0]) * ease,
                     start[1] + (self.home_y - start[1]) * ease)
        if step + 1 < steps:
            self.root.after(16, lambda: self.alive and self.slide_home(step + 1, start))
        else:
            self.dragging = False
            self.last_active = time.time()

    def play_beat(self, i):
        if not self.alive:
            return
        if i == len(BEAT):
            self.busy = False
            self.show("ready")
            self.last_active = time.time()
            return
        self.busy = True
        pose, sound, wait = BEAT[i]
        self.show(pose)
        if sound:
            play(sound)
        self.root.after(wait, lambda: self.play_beat(i + 1))

    def quit(self):
        self.alive = False
        self.win.destroy()


# ---------- the launcher window ----------

class Launcher:
    def __init__(self):
        ensure_sounds()
        self.root = tk.Tk()
        self.root.title("Bongo Dog")
        self.root.geometry("280x220")
        self.root.resizable(False, False)
        self.root.config(bg="#fff3e0")

        tk.Label(self.root, text="Bongo Dog 🐶", font=("Segoe UI", 16, "bold"),
                 bg="#fff3e0", fg="#6b3e1f").pack(pady=(18, 10))
        self.start_btn = tk.Button(self.root, text="START", font=("Segoe UI", 14, "bold"),
                                   width=10, bg="#e74c3c", fg="white", relief="flat",
                                   activebackground="#c0392b", command=self.start)
        self.start_btn.pack(pady=6)
        self.qp_label = tk.Label(self.root, text="QP: 0", font=("Segoe UI", 14),
                                 bg="#fff3e0", fg="#6b3e1f")
        self.qp_label.pack(pady=8)
        note = "" if keyboard else "(pynput not installed: typing only\ncounts while this window or the dog is selected)"
        tk.Label(self.root, text=note, font=("Segoe UI", 8), bg="#fff3e0",
                 fg="#a07050").pack()

        self.pet = None
        self.qp = 0
        self.keys_down = set()          # stops a held-down key from counting many times
        self.key_queue = queue.Queue()  # pynput runs in another thread; it drops a note here

        if keyboard:
            self.listener = keyboard.Listener(on_press=self.any_key_down,
                                              on_release=self.any_key_up)
            self.listener.daemon = True
            self.listener.start()
        else:
            self.root.bind_all("<KeyPress>", lambda e: self.any_key_down(e.keysym))
            self.root.bind_all("<KeyRelease>", lambda e: self.any_key_up(e.keysym))

        self.check_keys()

    def any_key_down(self, key):
        if key in self.keys_down:
            return
        self.keys_down.add(key)
        self.key_queue.put(1)   # only "a key was pressed", never which key

    def any_key_up(self, key):
        self.keys_down.discard(key)

    def check_keys(self):
        while not self.key_queue.empty():
            self.key_queue.get()
            if self.pet and self.pet.alive:
                self.pet.key_hit()
        self.root.after(15, self.check_keys)

    def add_qp(self):
        self.qp += 1
        self.qp_label.config(text=f"QP: {self.qp}")

    def start(self):
        if self.pet and self.pet.alive:
            return
        self.qp = 0
        self.qp_label.config(text="QP: 0")
        self.pet = Pet(self.root, self.add_qp)

    def run(self):
        self.root.mainloop()


def main():
    Launcher().run()


if __name__ == "__main__":
    main()
