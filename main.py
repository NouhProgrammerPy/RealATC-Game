from tkinter import *
import sys
import subprocess


def load_game():
    performance = performance_var.get()
    print(f"Starting game with {performance} performance mode...")
    window.destroy()
    subprocess.run(
        [sys.executable, "atcgame.py", performance]
    )


BG_COLOR = "#77E4C8"
ENTRY_BG_COLOR = "#36C2CE"

window = Tk()
window.title("ATC Game")
window.config(padx=50, pady=50, bg=BG_COLOR)
window.resizable(False, False)

canvas = Canvas(
    width=200,
    height=200,
    bg=BG_COLOR,
    highlightthickness=0
)

logo = PhotoImage(file="icon.png")
canvas.create_image(100, 100, image=logo)

performance_var = StringVar(value="HIGH")

title_label = Label(
    text="Air Traffic Control Simulator",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR
)

subtitle_label = Label(
    text="Choose your settings and start the game",
    font=("Arial", 10),
    bg=BG_COLOR
)

performance_label = Label(
    text="Performance:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

performance_sub_label = Label(
    text="Low performance mode turns trails off",
    font=("Arial", 10),
    bg=BG_COLOR
)

high_radio = Radiobutton(
    text="High Performance (Recommended)",
    variable=performance_var,
    value="HIGH",
    bg=BG_COLOR,
    activebackground=BG_COLOR
)

low_radio = Radiobutton(
    text="Low Performance",
    variable=performance_var,
    value="LOW",
    bg=BG_COLOR,
    activebackground=BG_COLOR
)

start_button = Button(
    text="Start Game",
    width=30,
    height=2,
    command=load_game
)

version_label = Label(
    text="Pre-Release",
    font=("Arial", 8),
    bg=BG_COLOR
)

canvas.grid(row=0, column=0, columnspan=2, pady=(0, 10))

title_label.grid(row=1, column=0, columnspan=2)
subtitle_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))

performance_label.grid(row=4, column=0, sticky="e", padx=(0, 10))
performance_sub_label.grid(row=3, column=1, sticky="e", padx=(0, 10))

high_radio.grid(row=4, column=1, sticky="w")
low_radio.grid(row=5, column=1, sticky="w")

start_button.grid(row=6, column=0, columnspan=2, pady=25)

version_label.grid(row=7, column=0, columnspan=2)

window.mainloop()
