import random
def open_dice_roller():
    win = tk.Toplevel()
    win.title("Dice Roller")
    win.configure(bg=BG_COLOR)

    def roll(die):
        result = random.randint(1, die)
        result_label.config(text=f"d{die} → {result}")

    tk.Label(win, text="Select a die to roll:", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
    for die in [4, 6, 8, 10, 12, 20, 100]:
        tk.Button(win, text=f"d{die}", font=FONT_MAIN, width=6, command=lambda d=die: roll(d)).pack(pady=2)

    result_label = tk.Label(win, text="", font=FONT_BOLD, bg=BG_COLOR, fg="white")
    result_label.pack(pady=10)
