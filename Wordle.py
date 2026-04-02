import tkinter as tk
import random

WORDS = [
    "APPLE","BEACH","CRANE","DRIVE","EARTH","FLAME","GRACE","HEART",
    "JUICE","KNIFE","LEMON","MONEY","NIGHT","OCEAN","PIANO","RIVER",
    "STONE","TIGER","WATER","BRAIN","CLOUD","DANCE","EAGLE","FROST",
    "HOUSE","LIGHT","MOUNT","OLIVE","PASTA","ROBOT","SNAKE","TOWER",
    "BLEND","CRISP","FLOOR","GRIND","LUNCH","ORBIT","PIXEL","RAPID",
    "SOLVE","TROUT","BOXER","MAGIC","NOISE","PERCH","RANCH","STOMP",
    "TULIP","CRAVE","HOTEL","PLANK","RAINY","SKUNK","TEMPO","WEARY",
    "ABIDE","CHAMP","FILTH","GUAVA","IRONY","JUMPY","KAYAK","MUDDY",
    "OXIDE","QUOTA","RAVEN","SCALD","TAPIR","VAGUE","WORDY","BATON",
    "CHURN","EQUIP","GRUFF","HOMER","JOULE","LUSTY","MOTIF","NIFTY",
    "OPTIC","PREEN","RENEW","SPUNK","TABOO","VIGOR","EXACT","CAULK",
    "EPOCH","FELON","HIPPO","KAZOO","MAXIM","NAVEL","POLKA","REPAY"
]

target = random.choice(WORDS)
current_row = 0
current_col = 0
game_over = False

window = tk.Tk()

import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

window.iconbitmap(resource_path("icon.ico"))

window.title("Wordle")
window.geometry("400x650")
window.configure(bg="white")

# ── Define show_hint FIRST before using it ───────────────────────────────────
def show_hint():
    vowels = "AEIOU"
    count = sum(1 for letter in target if letter in vowels)
    message.config(text=f"Hint: The word has {count} vowel(s)!")

# ── Title with 💡 beside it ───────────────────────────────────────────────────
title_frame = tk.Frame(window, bg="white")
title_frame.pack(pady=10)

title = tk.Label(title_frame, text="WORDLE", font=("Arial", 24, "bold"), bg="white")
title.pack(side="left")

hint_btn = tk.Button(
    title_frame, text="💡", font=("Arial", 18),
    relief="flat", bg="white", cursor="hand2",
    command=show_hint
)
hint_btn.pack(side="left", padx=5)

# ── Message ───────────────────────────────────────────────────────────────────
message = tk.Label(window, text="Guess the 5-letter word!", font=("Arial", 11), bg="white", fg="gray")
message.pack()

# ── Board ─────────────────────────────────────────────────────────────────────
board_frame = tk.Frame(window, bg="white")
board_frame.pack(pady=10)

tiles = []
for row in range(6):
    tile_row = []
    for col in range(5):
        tile = tk.Label(
            board_frame, text="", width=4, height=2,
            font=("Arial", 18, "bold"), relief="solid", borderwidth=1,
            bg="white"
        )
        tile.grid(row=row, column=col, padx=4, pady=4)
        tile_row.append(tile)
    tiles.append(tile_row)

# ── Keyboard ──────────────────────────────────────────────────────────────────
keyboard_frame = tk.Frame(window, bg="white")
keyboard_frame.pack(pady=10)

keyboard_rows = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["ENTER","Z","X","C","V","B","N","M","⌫"]
]

key_buttons = {}
for r, row in enumerate(keyboard_rows):
    row_frame = tk.Frame(keyboard_frame, bg="white")
    row_frame.pack(pady=2)
    for key in row:
        btn = tk.Button(
            row_frame, text=key, font=("Arial", 11, "bold"),
            width=3 if len(key) == 1 else 5, height=1,
            relief="solid", borderwidth=1, bg="#d3d6da",
            command=lambda k=key: handle_input(k)
        )
        btn.pack(side="left", padx=2)
        key_buttons[key] = btn

# ── Game logic ────────────────────────────────────────────────────────────────
def handle_input(key):
    global current_row, current_col, game_over
    if game_over:
        return
    if key == "⌫" or key == "BackSpace":
        if current_col > 0:
            current_col -= 1
            tiles[current_row][current_col].config(text="")
    elif key == "ENTER" or key == "Return":
        if current_col < 5:
            message.config(text="Not enough letters!")
            return
        submit_guess()
    elif len(key) == 1 and key.isalpha() and current_col < 5:
        tiles[current_row][current_col].config(text=key.upper())
        current_col += 1

def submit_guess():
    global current_row, current_col, game_over
    guess = "".join(tiles[current_row][c]["text"] for c in range(5))
    result = ["absent"] * 5
    target_arr = list(target)
    used = [False] * 5

    for i in range(5):
        if guess[i] == target_arr[i]:
            result[i] = "correct"
            used[i] = True

    for i in range(5):
        if result[i] == "correct":
            continue
        for j in range(5):
            if not used[j] and guess[i] == target_arr[j]:
                result[i] = "present"
                used[j] = True
                break

    colors = {"correct": "#6aaa64", "present": "#c9b458", "absent": "#787c7e"}
    for c in range(5):
        tiles[current_row][c].config(
            bg=colors[result[c]], fg="white", relief="flat"
        )
        key = guess[c]
        priority = {"correct": 3, "present": 2, "absent": 1}
        btn = key_buttons.get(key)
        if btn:
            state_map = {"#6aaa64": 3, "#c9b458": 2, "#787c7e": 1, "#d3d6da": 0}
            if state_map.get(btn.cget("bg"), 0) < priority[result[c]]:
                btn.config(bg=colors[result[c]], fg="white")

    if guess == target:
        message.config(text="You got it! 🎉")
        game_over = True
        return

    current_row += 1
    current_col = 0
    if current_row == 6:
        message.config(text=f"Game over! Word was: {target}")
        game_over = True
    else:
        message.config(text="Keep guessing!")

# ── Keyboard binding ──────────────────────────────────────────────────────────
def handle_key(event):
    handle_input(event.keysym)

window.bind("<Key>", handle_key)
window.mainloop()