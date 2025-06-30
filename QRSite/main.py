import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import webbrowser
import PyPDF2
import random

# Global style settings for our D&D theme.
BG_COLOR = "#3b2f2f"         # A dark, muted brown background.
FG_COLOR = "gold"            # Gold text.
FONT_MAIN = ("Garamond", 12)
FONT_BOLD = ("Garamond", 12, "bold")
FONT_SMALL = ("Garamond", 10)
FONT_TINY = ("Garamond", 8)

####################################
# Extra Widget Function for Classes
####################################
def create_class_buttons(parent):
    class_urls = {
        "Barbarian": "https://www.dndbeyond.com/classes/barbarian",
        "Bard": "https://www.dndbeyond.com/classes/bard",
        "Cleric": "https://www.dndbeyond.com/classes/cleric",
        "Druid": "https://www.dndbeyond.com/classes/druid",
        "Fighter": "https://www.dndbeyond.com/classes/fighter",
        "Monk": "https://www.dndbeyond.com/classes/monk",
        "Paladin": "https://www.dndbeyond.com/classes/paladin",
        "Ranger": "https://www.dndbeyond.com/classes/ranger",
        "Rogue": "https://www.dndbeyond.com/classes/rogue",
        "Sorcerer": "https://www.dndbeyond.com/classes/sorcerer",
        "Warlock": "https://www.dndbeyond.com/classes/warlock",
        "Wizard": "https://www.dndbeyond.com/classes/wizard",
    }

    for idx, (name, url) in enumerate(class_urls.items()):
        button = tk.Button(parent, text=name, font=FONT_MAIN, command=lambda link=url: webbrowser.open(link))
        button.grid(row=idx//3, column=idx%3, padx=5, pady=5, sticky="ew")

####################################
# PDF Character Sheet Parser
####################################
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

def open_pdf_and_display(text_widget):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)

####################################
# Tab Creation Functions
####################################
def create_classes_feats_tab(notebook):
    tab = tk.Frame(notebook, bg=BG_COLOR)
    label = tk.Label(tab, text="Choose Your Class", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    label.pack(pady=10)
    frame = tk.Frame(tab, bg=BG_COLOR)
    frame.pack()
    create_class_buttons(frame)
    return tab

def create_other_search_tab(notebook):
    tab = tk.Frame(notebook, bg=BG_COLOR)
    label = tk.Label(tab, text="Other Resources", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    label.pack(pady=10)
    links = {
        "Feats": "https://www.dndbeyond.com/feats",
        "Spells": "https://www.dndbeyond.com/spells",
        "Magic Items": "https://www.dndbeyond.com/magic-items"
    }
    for name, url in links.items():
        b = tk.Button(tab, text=name, font=FONT_MAIN, command=lambda link=url: webbrowser.open(link))
        b.pack(pady=5)
    return tab

def create_npc_tracker_tab(notebook):
    tab = tk.Frame(notebook, bg=BG_COLOR)
    label = tk.Label(tab, text="NPC Tracker", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    label.pack(pady=10)
    text_area = scrolledtext.ScrolledText(tab, width=60, height=20, font=FONT_MAIN)
    text_area.pack(padx=10, pady=10)
    return tab

def create_character_pdf_tab(notebook):
    tab = tk.Frame(notebook, bg=BG_COLOR)
    label = tk.Label(tab, text="Load Character Sheet (PDF)", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    label.pack(pady=10)
    text_area = scrolledtext.ScrolledText(tab, width=60, height=20, font=FONT_MAIN)
    text_area.pack(padx=10, pady=10)
    button = tk.Button(tab, text="Open PDF", font=FONT_MAIN, command=lambda: open_pdf_and_display(text_area))
    button.pack(pady=5)
    return tab

def create_dice_roller_tab(notebook):
    tab = tk.Frame(notebook, bg=BG_COLOR)
    header = tk.Label(tab, text="D&D Dice Roller", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    header.pack(pady=(10, 5))

    result_label = tk.Label(tab, text="Result: ", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    result_label.pack(pady=10)

    def roll(sides):
        result = random.randint(1, sides)
        result_label.config(text=f"Result: d{sides} → {result}")

    dice_frame = tk.Frame(tab, bg=BG_COLOR)
    dice_frame.pack(pady=10)

    for sides in [4, 6, 8, 10, 12, 20, 100]:
        b = tk.Button(dice_frame, text=f"d{sides}", font=FONT_MAIN, width=6, command=lambda s=sides: roll(s))
        b.pack(side="left", padx=5, pady=5)

    return tab

####################################
# Main Application Setup
####################################
def main():
    root = tk.Tk()
    root.title("D&D Toolkit")
    root.configure(bg=BG_COLOR)
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Create and add all tabs
    classes_feats_tab = create_classes_feats_tab(notebook)
    other_search_tab = create_other_search_tab(notebook)
    npc_tracker_tab = create_npc_tracker_tab(notebook)
    character_pdf_tab = create_character_pdf_tab(notebook)
    dice_roller_tab = create_dice_roller_tab(notebook)

    notebook.add(classes_feats_tab, text="Classes & Feats")
    notebook.add(other_search_tab, text="Other Searches")
    notebook.add(npc_tracker_tab, text="NPC Tracker")
    notebook.add(character_pdf_tab, text="Character PDF")
    notebook.add(dice_roller_tab, text="Dice Roller")

    root.mainloop()

if __name__ == "__main__":
    main()
