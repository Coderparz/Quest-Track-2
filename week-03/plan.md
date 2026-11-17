# week-03 · Bongo Dog desktop pet — plan

## What to build
A fluffy Pomeranian with a drum that lives on top of your desktop.

- **Launcher window**: a small window with a **START** button in the middle and a **QP** counter under it.
  ```
  ┌──────────────────────┐
  │     Bongo Dog 🐶     │
  │                      │
  │      [  START  ]     │
  │                      │
  │       QP: 0          │
  └──────────────────────┘
  ```
- Press START → the dog appears in the **bottom-right corner** of the screen.
- **Typing anywhere** (even in other apps) → the dog hits the drum, paws taking turns: left, right, left, right… **No sound.** Each key press adds 1 to **QP**.
- **QP** counts key presses only. It starts at 0 every time the pet opens.
- **No typing for 10 seconds** → the dog falls asleep (zZ pose). The next key press wakes him up.
- **Click the dog** → he plays a little beat **with sound**: "bom-bom-ba-BOM!" (about 2 seconds), ending in the both-paws-up "ta-da" pose.
- **Pick him up** (drag) → he shows the both-paws-up pose. **Drop him** → he slides back to his home spot (bottom-right) and keeps playing. (The dog and drum move together for now.)
- **Right-click the dog** → a small menu with **Quit**.
- Size: about **250 px**.

## Where it runs
- On the Windows desktop as a **Python** program (not in a browser).
- The dog window has no border, a see-through background, and stays on top of other windows.
- While building: start it with a command (`python launcher.py`) so we can see errors.
- When finished: a file you **double-click** (`.pyw`) to open the launcher with no black terminal window.

## Materials
| What | Where / how |
|---|---|
| Python | already installed |
| tkinter (windows, buttons, pictures) | comes with Python |
| winsound (play sound) | comes with Python on Windows |
| wave (make our own drum sound file) | comes with Python |
| pynput (notice key presses in any app) | **needs install → ask first** |
| Pillow (cut and resize the picture), only if needed | **needs install → ask first** |
| Sticker sheet with 4 poses | `week-03/art/sheet.png` |

The 4 poses in `sheet.png`:
| Spot | Pose | Used for |
|---|---|---|
| Top-left | both paws up | ready / picked up / "ta-da" |
| Top-right | left paw hits drum | left hit |
| Bottom-left | right paw hits drum | right hit |
| Bottom-right | eyes closed, zZ | sleeping |

## Steps
Do one step at a time. Don't start the next step until "what to check" works.

### Step 1 · Cut the 4 poses out of the sheet
- Make 4 separate pictures (about 250 px) in `week-03/art/`: ready, left hit, right hit, sleep.
- **What to check:** Open each of the 4 pictures. Each one is a single whole dog, nothing cut off, and the right size.
- **Commit:** "Cut 4 pet poses from sticker sheet"

### Step 2 · Launcher window
- A small window with "Bongo Dog 🐶", a **START** button in the middle, and **QP: 0** under it.
- **What to check:** `python launcher.py` opens the window. It looks like the picture above. START doesn't do anything yet.
- **Commit:** "Add launcher window with START button and QP counter"

### Step 3 · The dog appears
- START → the dog (ready pose) appears in the bottom-right corner, with no border, a see-through background, and on top of other windows.
- **What to check:** Only the dog shows, with no box or black edge around it. He stays on top when you click another app. He doesn't cover the taskbar.
- **Commit:** "Show the pet on the desktop when START is pressed"

### Step 4 · Right-click → Quit
- Right-click the dog → small menu → Quit closes the pet.
- **What to check:** Quit closes the dog. Closing the launcher also closes the dog.
- **Commit:** "Add right-click menu with Quit"

### Step 5 · Pick up and drop
- Drag the dog → both-paws-up pose while held. Let go → he slides back home to the bottom-right.
- **What to check:** Dragging is smooth. After dropping, he slides back, not jumps. A quick click doesn't count as a drag.
- **Commit:** "Let the pet be picked up and slide back home"

### Step 6 · Click beat with sound
- Make a drum sound file with Python (no download).
- Click the dog → "bom-bom-ba-BOM!" with sound and changing poses → ends in the both-paws-up pose.
- **What to check:** The sound plays in time with the paws. Clicking again during the beat doesn't break it. Dragging does NOT start the beat.
- **Commit:** "Add click beat with drum sound"

### Step 7 · Typing anywhere makes him drum (ask before installing pynput)
- Install `pynput` **only after you say yes**.
- Every key press in any app → next paw hits (left, right, left…), no sound, QP +1.
- **What to check:** Type in another app, like Notepad, and the dog drums. The paws take turns. QP goes up by 1 per key. Holding a key down doesn't go crazy. No sound while typing.
- **Commit:** "Make the pet drum when typing anywhere and count QP"

### Step 8 · Falls asleep
- 10 seconds with no typing → sleep pose (zZ). The next key → wakes up and drums.
- **What to check:** Wait 10 seconds and he sleeps. Press a key and he wakes right away. The click beat also wakes him.
- **Commit:** "Pet falls asleep after 10 seconds without typing"

### Step 9 · Double-click to start
- Make the `.pyw` file so double-clicking opens the launcher with no black terminal window.
- **What to check:** Double-click the file in File Explorer and everything works the same as with the command.
- **Commit:** "Add double-click start file"

### Later (maybe)
- Separate pictures for the dog and the drum, so only the dog gets picked up and walks back to a drum that stays in place.

## What not to do
- **Never save or show what keys were typed.** Only count them for QP. Nothing typed goes into any file.
- Don't install anything (pynput, Pillow, …) without asking first.
- Don't make the pet start automatically when Windows turns on, and don't change Windows settings.
- Don't read or change files outside the workshop folder.
- Don't do more than one step at a time. Don't skip "what to check".
- Don't rewrite whole files when fixing something. Fix just the part that's wrong and say in one line what changed.
- Don't put real names, phone numbers, addresses or school names in any file (public repo).
- Don't delete or rename files without asking. That includes the early draft `bongo-dog.html`.
- Don't push to GitHub unless asked.
