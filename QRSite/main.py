import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import webbrowser
import PyPDF2

# Optional: Uncomment these lines if you want to use a background image (requires Pillow)
# from PIL import Image, ImageTk

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
    """
    Creates a grid of class buttons for the Classes section.
    Uses the "PHB D&D Free Rules (2024)" classes.
    """
    class_urls = {
        "Barbarian": "https://www.dndbeyond.com/classes/2190875-barbarian",
        "Bard": "https://www.dndbeyond.com/classes/2190876-bard",
        "Cleric": "https://www.dndbeyond.com/classes/2190877-cleric",
        "Druid": "https://www.dndbeyond.com/classes/2190878-druid",
        "Fighter": "https://www.dndbeyond.com/classes/2190879-fighter",
        "Monk": "https://www.dndbeyond.com/classes/2190880-monk",
        "Paladin": "https://www.dndbeyond.com/classes/2190881-paladin",
        "Ranger": "https://www.dndbeyond.com/classes/2190882-ranger",
        "Rogue": "https://www.dndbeyond.com/classes/2190883-rogue",
        "Sorcerer": "https://www.dndbeyond.com/classes/2190884-sorcerer",
        "Warlock": "https://www.dndbeyond.com/classes/2190885-warlock",
        "Wizard": "https://www.dndbeyond.com/classes/2190886-wizard"
    }
    btn_frame = tk.Frame(parent, bg=BG_COLOR)
    btn_frame.pack(anchor="center", padx=10, pady=(0,4))
    i = 0
    for cls, url in class_urls.items():
        btn = tk.Button(btn_frame, text=cls, command=lambda u=url: webbrowser.open(u),
                        width=20, height=2, font=FONT_MAIN)
        btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        i += 1

####################################
# Extra Widget Function for Feats
####################################
def create_default_feats_button(parent):
    """
    Creates a "Default Feats" button for the Feats section.
    Clicking this button opens the default feats page.
    """
    btn = tk.Button(parent, text="Default Feats", command=lambda: webbrowser.open("https://www.dndbeyond.com/feats"),
                    font=FONT_MAIN)
    btn.pack(anchor="center", pady=(0,4))

####################################
# Helper Function: Create a Search Section
####################################
def create_search_section(parent, category, default_url, search_template_url, extra_widget_func=None):
    """
    Creates a section for the D&D Beyond Search tab.
    Each section includes:
      - A header label (centered) with the category name.
      - A frame with a search Entry and a "Go" button to its right.
      - Optionally extra widgets added via extra_widget_func.
      - A horizontal separator line.
    
    If the entry is empty, clicking "Go" opens default_url;
    otherwise, it opens the URL created by substituting {term} in search_template_url.
    """
    section_frame = tk.Frame(parent, bg=BG_COLOR)
    
    header = tk.Label(section_frame, text=category, font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
    header.pack(anchor="center", pady=(4,2))
    
    search_bar_frame = tk.Frame(section_frame, bg=BG_COLOR)
    search_bar_frame.pack(pady=2, fill="x", padx=10)
    
    entry = tk.Entry(search_bar_frame, font=FONT_MAIN, width=40)
    entry.pack(side="left", padx=(0, 5))
    
    go_button = tk.Button(search_bar_frame, text="Go", font=FONT_BOLD, padx=6, pady=2,
                          command=lambda: webbrowser.open(entry.get().strip() and search_template_url.format(term=entry.get().strip()) or default_url))
    go_button.pack(side="left")
    
    if extra_widget_func:
        extra_widget_func(section_frame)
    
    separator = ttk.Separator(section_frame, orient="horizontal")
    separator.pack(fill="x", pady=5)
    
    return section_frame

####################################
# D&D Beyond Search Tab
####################################
def create_dnd_search_tab(notebook):
    search_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Define categories.
    categories = [
        {
            "name": "Magic Items",
            "default_url": "https://www.dndbeyond.com/magic-items",
            "template_url": ("https://www.dndbeyond.com/magic-items?filter-search={term}"
                             "&filter-type=0&filter-requires-attunement=&filter-effect-type=&filter-effect-subtype=&filter-has-charges=&filter-partnered-content=f")
        },
        {
            "name": "Classes",
            "default_url": "https://www.dndbeyond.com/rules",
            "template_url": "https://www.dndbeyond.com/rules?filter-search={term}",
            "extra_func": create_class_buttons
        },
        {
            "name": "Spells",
            "default_url": "https://www.dndbeyond.com/spells",
            "template_url": "https://www.dndbeyond.com/spells?filter-search={term}"
        },
        {
            "name": "Feats",
            "default_url": "https://www.dndbeyond.com/feats",
            "template_url": "https://www.dndbeyond.com/feats?filter-name={term}&filter-prereq-subtype=&filter-partnered-content=f",
            "extra_func": create_default_feats_button
        },
        {
            "name": "Equipment",
            "default_url": "https://www.dndbeyond.com/equipment",
            "template_url": "https://www.dndbeyond.com/equipment?filter-search={term}"
        },
        {
            "name": "Monsters",
            "default_url": "https://www.dndbeyond.com/monsters",
            "template_url": "https://www.dndbeyond.com/monsters?filter-search={term}"
        }
    ]
    
    for cat in categories:
        extra = cat.get("extra_func", None)
        section = create_search_section(search_frame, cat["name"], cat["default_url"], cat["template_url"], extra_widget_func=extra)
        section.pack(fill="x", padx=10, pady=5)
    
    return search_frame

####################################
# NPC Tracker Tab Functions
####################################
class NPCFrame(tk.Frame):
    def __init__(self, master, npc_number, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.npc_number = npc_number
        self.health = 0
        self.spell_slots = {1: 4, 2: 3, 3: 3, 4: 3}
        self.create_widgets()
    
    def create_widgets(self):
        self.configure(bg=BG_COLOR)
        title = tk.Label(self, text=f"NPC {self.npc_number}", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
        title.grid(row=0, column=0, columnspan=4, pady=(2,4))
        
        tk.Label(self, text="Name:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN).grid(row=1, column=0, sticky="e", padx=2, pady=2)
        self.name_entry = tk.Entry(self, width=12, font=FONT_MAIN)
        self.name_entry.grid(row=1, column=1, sticky="w", padx=2, pady=2)
        
        tk.Label(self, text="Level:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN).grid(row=1, column=2, sticky="e", padx=2, pady=2)
        self.level_entry = tk.Entry(self, width=4, font=FONT_MAIN)
        self.level_entry.grid(row=1, column=3, sticky="w", padx=2, pady=2)
        
        tk.Label(self, text="Health:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN).grid(row=2, column=0, sticky="e", padx=2, pady=2)
        self.health_entry = tk.Entry(self, width=8, justify="center", font=FONT_MAIN)
        self.health_entry.grid(row=2, column=1, sticky="w", padx=2, pady=2)
        self.health_entry.insert(0, str(self.health))
        
        self.set_health_btn = tk.Button(self, text="Set", command=self.set_health, padx=2, pady=1, font=FONT_MAIN)
        self.set_health_btn.grid(row=2, column=2, padx=2, pady=2)
        
        tk.Label(self, text="Adj:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN).grid(row=3, column=0, sticky="e", padx=2, pady=2)
        self.adjustment_entry = tk.Entry(self, width=8, justify="center", font=FONT_MAIN)
        self.adjustment_entry.grid(row=3, column=1, sticky="w", padx=2, pady=2)
        self.adjustment_entry.insert(0, "0")
        
        self.adjust_health_btn = tk.Button(self, text="Apply", command=self.adjust_health, padx=2, pady=1, font=FONT_MAIN)
        self.adjust_health_btn.grid(row=3, column=2, padx=2, pady=2)
        
        quick_frame = tk.Frame(self, bg=BG_COLOR)
        quick_frame.grid(row=4, column=0, columnspan=4, padx=2, pady=(2,4))
        plus_frame = tk.Frame(quick_frame, bg=BG_COLOR)
        plus_frame.pack(pady=(0,2))
        for inc in [1, 2, 5, 10, 15]:
            btn = tk.Button(plus_frame, text=f"+{inc}", command=lambda inc=inc: self.quick_adjust(inc),
                            padx=2, pady=1, font=FONT_TINY)
            btn.pack(side="left", padx=2)
        minus_frame = tk.Frame(quick_frame, bg=BG_COLOR)
        minus_frame.pack()
        for dec in [1, 2, 5, 10, 15]:
            btn = tk.Button(minus_frame, text=f"-{dec}", command=lambda dec=dec: self.quick_adjust(-dec),
                            padx=2, pady=1, font=FONT_TINY)
            btn.pack(side="left", padx=2)
        
        row = 5
        self.spell_slot_labels = {}
        for lvl in range(1, 5):
            tk.Label(self, text=f"Lvl {lvl}:", font=FONT_TINY, bg=BG_COLOR, fg=FG_COLOR).grid(row=row, column=0, sticky="e", padx=2, pady=1)
            self.spell_slot_labels[lvl] = tk.Label(self, text=str(self.spell_slots[lvl]), width=3, relief="sunken", font=FONT_TINY, bg="white")
            self.spell_slot_labels[lvl].grid(row=row, column=1, sticky="w", padx=2, pady=1)
            btn_consume = tk.Button(self, text="-", command=lambda l=lvl: self.adjust_spell_slot(l, -1), padx=2, pady=1, font=FONT_TINY)
            btn_consume.grid(row=row, column=2, padx=2, pady=1)
            btn_restore = tk.Button(self, text="+", command=lambda l=lvl: self.adjust_spell_slot(l, 1), padx=2, pady=1, font=FONT_TINY)
            btn_restore.grid(row=row, column=3, padx=2, pady=1)
            row += 1

    def set_health(self):
        try:
            new_health = int(self.health_entry.get())
            self.health = new_health
        except ValueError:
            pass
        self.health_entry.delete(0, tk.END)
        self.health_entry.insert(0, str(self.health))
    
    def adjust_health(self):
        try:
            delta = int(self.adjustment_entry.get())
            self.health += delta
        except ValueError:
            pass
        self.health_entry.delete(0, tk.END)
        self.health_entry.insert(0, str(self.health))
        self.adjustment_entry.delete(0, tk.END)
        self.adjustment_entry.insert(0, "0")
    
    def quick_adjust(self, amount):
        self.health += amount
        self.health_entry.delete(0, tk.END)
        self.health_entry.insert(0, str(self.health))
    
    def adjust_spell_slot(self, level, delta):
        self.spell_slots[level] += delta
        if self.spell_slots[level] < 0:
            self.spell_slots[level] = 0
        self.spell_slot_labels[level].config(text=str(self.spell_slots[level]))

####################################
# Character PDF Tab Functions
####################################
def create_character_pdf_tab(notebook):
    pdf_frame = tk.Frame(notebook, bg=BG_COLOR)
    status_label = tk.Label(pdf_frame, text="Upload your Goody83 PDF", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR)
    status_label.pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(pdf_frame, wrap=tk.WORD, width=100, height=30, font=FONT_MAIN)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)
    
    def upload_pdf():
        file_path = filedialog.askopenfilename(
            title="Select Goody83 PDF",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="Goody83.pdf"
        )
        if not file_path:
            status_label.config(text="No file selected.")
            return
        try:
            pdf_text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"
            text_area.config(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, pdf_text)
            text_area.config(state=tk.DISABLED)
            status_label.config(text="PDF loaded successfully.")
        except Exception as e:
            status_label.config(text=f"Error loading PDF: {e}")
    
    tk.Button(pdf_frame, text="Upload PDF", command=upload_pdf, padx=4, pady=2, font=FONT_MAIN).pack(pady=8)
    return pdf_frame

####################################
# Initiative Tracker Window
####################################
def create_initiative_tracker_window():
    init_win = tk.Toplevel()
    init_win.title("Initiative Tracker")
    init_win.geometry("500x500")
    init_win.configure(bg=BG_COLOR)
    
    initiative_order = []
    current_turn_index = [0]
    
    # Top frame: Name, Pos entry and Reset Order button.
    top_frame = tk.Frame(init_win, bg=BG_COLOR)
    top_frame.pack(pady=10, fill="x")
    
    tk.Label(top_frame, text="Name:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(top_frame, width=20, font=FONT_MAIN)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(top_frame, text="Pos:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5)
    position_var = tk.StringVar()
    pos_display = tk.Entry(top_frame, textvariable=position_var, width=8, justify="center", state="readonly", font=FONT_MAIN)
    pos_display.grid(row=0, column=3, padx=5, pady=5)
    
    reset_btn = tk.Button(top_frame, text="Reset Order", command=lambda: reset_initiative(), font=FONT_MAIN)
    reset_btn.grid(row=0, column=4, padx=5, pady=5)
    
    # "Up Next" section.
    up_next_frame = tk.Frame(init_win, bg=BG_COLOR)
    up_next_frame.pack(pady=10, fill="x")
    up_next_label = tk.Label(up_next_frame, text="Up Next: N/A", font=("Garamond", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    up_next_label.pack(anchor="center", padx=5)
    
    # Prev/Next buttons below "Up Next"
    nav_frame = tk.Frame(init_win, bg=BG_COLOR)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Prev", width=8, command=lambda: prev_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    tk.Button(nav_frame, text="Next", width=8, command=lambda: next_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    
    # Keypad frame.
    keypad_frame = tk.Frame(init_win, bg=BG_COLOR)
    keypad_frame.pack(pady=5)
    for i, digit in enumerate(["0", "1", "2", "3", "4"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=0, column=i, padx=3, pady=3)
    for i, digit in enumerate(["5", "6", "7", "8", "9"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=1, column=i, padx=3, pady=3)
    
    # Control frame for Clear and Set buttons.
    control_frame = tk.Frame(init_win, bg=BG_COLOR)
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Clear", width=8, command=lambda: clear_position(), font=FONT_MAIN).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Set", width=8, command=lambda: add_initiative(), font=FONT_MAIN).grid(row=0, column=1, padx=5, pady=5)
    
    # Listbox for full initiative order.
    listbox = tk.Listbox(init_win, width=60, height=10, font=FONT_MAIN)
    listbox.pack(pady=10)
    
    def update_listbox():
        listbox.delete(0, tk.END)
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        for pos, name in sorted_order:
            listbox.insert(tk.END, f"{pos} | {name}")
        update_up_next()
    
    def add_initiative():
        name = name_entry.get().strip()
        pos_text = position_var.get().strip()
        if not name or not pos_text:
            return
        try:
            pos = int(pos_text)
        except ValueError:
            return
        initiative_order.append((pos, name))
        current_turn_index[0] = 0
        update_listbox()
        name_entry.delete(0, tk.END)
        position_var.set("")
    
    def reset_initiative():
        nonlocal initiative_order
        initiative_order = []
        current_turn_index[0] = 0
        update_listbox()
    
    def append_digit(digit):
        current = position_var.get()
        position_var.set(current + str(digit))
    
    def clear_position():
        position_var.set("")
    
    def update_up_next():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order and 0 <= current_turn_index[0] < len(sorted_order):
            pos, name = sorted_order[current_turn_index[0]]
            up_next_label.config(text=f"Up Next: {pos} | {name}")
        else:
            up_next_label.config(text="Up Next: N/A")
    
    def next_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] < len(sorted_order) - 1:
                current_turn_index[0] += 1
            else:
                current_turn_index[0] = 0
            update_up_next()
    
    def prev_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] > 0:
                current_turn_index[0] -= 1
            else:
                current_turn_index[0] = len(sorted_order) - 1
            update_up_next()
    
    update_listbox()
    tk.Button(init_win, text="Reset Order", command=reset_initiative, font=FONT_MAIN).pack(pady=10)
    update_up_next()

####################################
# Tab: Classes & Feats
####################################
def create_classes_feats_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Classes section.
    classes_section = create_search_section(tab_frame,
                                            "Classes",
                                            "https://www.dndbeyond.com/rules",
                                            "https://www.dndbeyond.com/rules?filter-search={term}",
                                            extra_widget_func=create_class_buttons)
    classes_section.pack(fill="x", padx=10, pady=5)
    
    # Feats section.
    feats_section = create_search_section(tab_frame,
                                          "Feats",
                                          "https://www.dndbeyond.com/feats",
                                          "https://www.dndbeyond.com/feats?filter-name={term}&filter-prereq-subtype=&filter-partnered-content=f",
                                          extra_widget_func=create_default_feats_button)
    feats_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# Tab: Other Searches
####################################
def create_other_search_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Magic Items section.
    magic_section = create_search_section(tab_frame,
                                          "Magic Items",
                                          "https://www.dndbeyond.com/magic-items",
                                          ("https://www.dndbeyond.com/magic-items?filter-search={term}"
                                           "&filter-type=0&filter-requires-attunement=&filter-effect-type=&filter-effect-subtype=&filter-has-charges=&filter-partnered-content=f"))
    magic_section.pack(fill="x", padx=10, pady=5)
    
    # Spells section.
    spells_section = create_search_section(tab_frame,
                                           "Spells",
                                           "https://www.dndbeyond.com/spells",
                                           "https://www.dndbeyond.com/spells?filter-search={term}")
    spells_section.pack(fill="x", padx=10, pady=5)
    
    # Equipment section.
    equipment_section = create_search_section(tab_frame,
                                              "Equipment",
                                              "https://www.dndbeyond.com/equipment",
                                              "https://www.dndbeyond.com/equipment?filter-search={term}")
    equipment_section.pack(fill="x", padx=10, pady=5)
    
    # Monsters section.
    monsters_section = create_search_section(tab_frame,
                                             "Monsters",
                                             "https://www.dndbeyond.com/monsters",
                                             "https://www.dndbeyond.com/monsters?filter-search={term}")
    monsters_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# NPC Tracker Tab Functions
####################################
def create_npc_tracker_tab(notebook):
    tracker_frame = ttk.Frame(notebook)
    container = ttk.Frame(tracker_frame)
    container.pack(padx=8, pady=8, fill="both", expand=True)
    
    total_npcs = 12  # 12 NPC panels
    cols = 4         # 4 columns
    for npc in range(1, total_npcs + 1):
        npc_panel = NPCFrame(container, npc_number=npc, borderwidth=1, relief="groove")
        row = (npc - 1) // cols
        col = (npc - 1) % cols
        npc_panel.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
    for col in range(cols):
        container.grid_columnconfigure(col, weight=1)
    return tracker_frame

####################################
# Character PDF Tab Functions
####################################
def create_character_pdf_tab(notebook):
    pdf_frame = tk.Frame(notebook, bg=BG_COLOR)
    status_label = tk.Label(pdf_frame, text="Upload your Goody83 PDF", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR)
    status_label.pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(pdf_frame, wrap=tk.WORD, width=100, height=30, font=FONT_MAIN)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)
    
    def upload_pdf():
        file_path = filedialog.askopenfilename(
            title="Select Goody83 PDF",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="Goody83.pdf"
        )
        if not file_path:
            status_label.config(text="No file selected.")
            return
        try:
            pdf_text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"
            text_area.config(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, pdf_text)
            text_area.config(state=tk.DISABLED)
            status_label.config(text="PDF loaded successfully.")
        except Exception as e:
            status_label.config(text=f"Error loading PDF: {e}")
    
    tk.Button(pdf_frame, text="Upload PDF", command=upload_pdf, padx=4, pady=2, font=FONT_MAIN).pack(pady=8)
    return pdf_frame

####################################
# Initiative Tracker Window
####################################
def create_initiative_tracker_window():
    init_win = tk.Toplevel()
    init_win.title("Initiative Tracker")
    init_win.geometry("500x500")
    init_win.configure(bg=BG_COLOR)
    
    initiative_order = []
    current_turn_index = [0]
    
    # Top frame: Name, Pos entry and Reset Order button.
    top_frame = tk.Frame(init_win, bg=BG_COLOR)
    top_frame.pack(pady=10, fill="x")
    
    tk.Label(top_frame, text="Name:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(top_frame, width=20, font=FONT_MAIN)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(top_frame, text="Pos:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5)
    position_var = tk.StringVar()
    pos_display = tk.Entry(top_frame, textvariable=position_var, width=8, justify="center", state="readonly", font=FONT_MAIN)
    pos_display.grid(row=0, column=3, padx=5, pady=5)
    
    reset_btn = tk.Button(top_frame, text="Reset Order", command=lambda: reset_initiative(), font=FONT_MAIN)
    reset_btn.grid(row=0, column=4, padx=5, pady=5)
    
    # "Up Next" section.
    up_next_frame = tk.Frame(init_win, bg=BG_COLOR)
    up_next_frame.pack(pady=10, fill="x")
    up_next_label = tk.Label(up_next_frame, text="Up Next: N/A", font=("Garamond", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    up_next_label.pack(anchor="center", padx=5)
    
    # Prev/Next buttons below "Up Next"
    nav_frame = tk.Frame(init_win, bg=BG_COLOR)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Prev", width=8, command=lambda: prev_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    tk.Button(nav_frame, text="Next", width=8, command=lambda: next_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    
    # Keypad frame.
    keypad_frame = tk.Frame(init_win, bg=BG_COLOR)
    keypad_frame.pack(pady=5)
    for i, digit in enumerate(["0", "1", "2", "3", "4"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=0, column=i, padx=3, pady=3)
    for i, digit in enumerate(["5", "6", "7", "8", "9"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=1, column=i, padx=3, pady=3)
    
    # Control frame for Clear and Set buttons.
    control_frame = tk.Frame(init_win, bg=BG_COLOR)
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Clear", width=8, command=lambda: clear_position(), font=FONT_MAIN).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Set", width=8, command=lambda: add_initiative(), font=FONT_MAIN).grid(row=0, column=1, padx=5, pady=5)
    
    # Listbox for full initiative order.
    listbox = tk.Listbox(init_win, width=60, height=10, font=FONT_MAIN)
    listbox.pack(pady=10)
    
    def update_listbox():
        listbox.delete(0, tk.END)
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        for pos, name in sorted_order:
            listbox.insert(tk.END, f"{pos} | {name}")
        update_up_next()
    
    def add_initiative():
        name = name_entry.get().strip()
        pos_text = position_var.get().strip()
        if not name or not pos_text:
            return
        try:
            pos = int(pos_text)
        except ValueError:
            return
        initiative_order.append((pos, name))
        current_turn_index[0] = 0
        update_listbox()
        name_entry.delete(0, tk.END)
        position_var.set("")
    
    def reset_initiative():
        nonlocal initiative_order
        initiative_order = []
        current_turn_index[0] = 0
        update_listbox()
    
    def append_digit(digit):
        current = position_var.get()
        position_var.set(current + str(digit))
    
    def clear_position():
        position_var.set("")
    
    def update_up_next():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order and 0 <= current_turn_index[0] < len(sorted_order):
            pos, name = sorted_order[current_turn_index[0]]
            up_next_label.config(text=f"Up Next: {pos} | {name}")
        else:
            up_next_label.config(text="Up Next: N/A")
    
    def next_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] < len(sorted_order) - 1:
                current_turn_index[0] += 1
            else:
                current_turn_index[0] = 0
            update_up_next()
    
    def prev_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] > 0:
                current_turn_index[0] -= 1
            else:
                current_turn_index[0] = len(sorted_order) - 1
            update_up_next()
    
    update_listbox()
    tk.Button(init_win, text="Reset Order", command=reset_initiative, font=FONT_MAIN).pack(pady=10)
    update_up_next()

####################################
# Tab: Classes & Feats
####################################
def create_classes_feats_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Classes section.
    classes_section = create_search_section(tab_frame,
                                            "Classes",
                                            "https://www.dndbeyond.com/rules",
                                            "https://www.dndbeyond.com/rules?filter-search={term}",
                                            extra_widget_func=create_class_buttons)
    classes_section.pack(fill="x", padx=10, pady=5)
    
    # Feats section.
    feats_section = create_search_section(tab_frame,
                                          "Feats",
                                          "https://www.dndbeyond.com/feats",
                                          "https://www.dndbeyond.com/feats?filter-name={term}&filter-prereq-subtype=&filter-partnered-content=f",
                                          extra_widget_func=create_default_feats_button)
    feats_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# Tab: Other Searches
####################################
def create_other_search_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Magic Items section.
    magic_section = create_search_section(tab_frame,
                                          "Magic Items",
                                          "https://www.dndbeyond.com/magic-items",
                                          ("https://www.dndbeyond.com/magic-items?filter-search={term}"
                                           "&filter-type=0&filter-requires-attunement=&filter-effect-type=&filter-effect-subtype=&filter-has-charges=&filter-partnered-content=f"))
    magic_section.pack(fill="x", padx=10, pady=5)
    
    # Spells section.
    spells_section = create_search_section(tab_frame,
                                           "Spells",
                                           "https://www.dndbeyond.com/spells",
                                           "https://www.dndbeyond.com/spells?filter-search={term}")
    spells_section.pack(fill="x", padx=10, pady=5)
    
    # Equipment section.
    equipment_section = create_search_section(tab_frame,
                                              "Equipment",
                                              "https://www.dndbeyond.com/equipment",
                                              "https://www.dndbeyond.com/equipment?filter-search={term}")
    equipment_section.pack(fill="x", padx=10, pady=5)
    
    # Monsters section.
    monsters_section = create_search_section(tab_frame,
                                             "Monsters",
                                             "https://www.dndbeyond.com/monsters",
                                             "https://www.dndbeyond.com/monsters?filter-search={term}")
    monsters_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# NPC Tracker Tab Functions
####################################
def create_npc_tracker_tab(notebook):
    tracker_frame = ttk.Frame(notebook)
    container = ttk.Frame(tracker_frame)
    container.pack(padx=8, pady=8, fill="both", expand=True)
    
    total_npcs = 12  # 12 NPC panels
    cols = 4         # 4 columns
    for npc in range(1, total_npcs + 1):
        npc_panel = NPCFrame(container, npc_number=npc, borderwidth=1, relief="groove")
        row = (npc - 1) // cols
        col = (npc - 1) % cols
        npc_panel.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
    for col in range(cols):
        container.grid_columnconfigure(col, weight=1)
    return tracker_frame

####################################
# Character PDF Tab Functions
####################################
def create_character_pdf_tab(notebook):
    pdf_frame = tk.Frame(notebook, bg=BG_COLOR)
    status_label = tk.Label(pdf_frame, text="Upload your Goody83 PDF", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR)
    status_label.pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(pdf_frame, wrap=tk.WORD, width=100, height=30, font=FONT_MAIN)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)
    
    def upload_pdf():
        file_path = filedialog.askopenfilename(
            title="Select Goody83 PDF",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="Goody83.pdf"
        )
        if not file_path:
            status_label.config(text="No file selected.")
            return
        try:
            pdf_text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"
            text_area.config(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, pdf_text)
            text_area.config(state=tk.DISABLED)
            status_label.config(text="PDF loaded successfully.")
        except Exception as e:
            status_label.config(text=f"Error loading PDF: {e}")
    
    tk.Button(pdf_frame, text="Upload PDF", command=upload_pdf, padx=4, pady=2, font=FONT_MAIN).pack(pady=8)
    return pdf_frame

####################################
# Initiative Tracker Window
####################################
def create_initiative_tracker_window():
    init_win = tk.Toplevel()
    init_win.title("Initiative Tracker")
    init_win.geometry("500x500")
    init_win.configure(bg=BG_COLOR)
    
    initiative_order = []
    current_turn_index = [0]
    
    # Top frame: Name, Pos entry and Reset Order button.
    top_frame = tk.Frame(init_win, bg=BG_COLOR)
    top_frame.pack(pady=10, fill="x")
    
    tk.Label(top_frame, text="Name:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(top_frame, width=20, font=FONT_MAIN)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(top_frame, text="Pos:", font=FONT_MAIN, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5)
    position_var = tk.StringVar()
    pos_display = tk.Entry(top_frame, textvariable=position_var, width=8, justify="center", state="readonly", font=FONT_MAIN)
    pos_display.grid(row=0, column=3, padx=5, pady=5)
    
    reset_btn = tk.Button(top_frame, text="Reset Order", command=lambda: reset_initiative(), font=FONT_MAIN)
    reset_btn.grid(row=0, column=4, padx=5, pady=5)
    
    # "Up Next" section.
    up_next_frame = tk.Frame(init_win, bg=BG_COLOR)
    up_next_frame.pack(pady=10, fill="x")
    up_next_label = tk.Label(up_next_frame, text="Up Next: N/A", font=("Garamond", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    up_next_label.pack(anchor="center", padx=5)
    
    # Prev/Next buttons below "Up Next"
    nav_frame = tk.Frame(init_win, bg=BG_COLOR)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Prev", width=8, command=lambda: prev_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    tk.Button(nav_frame, text="Next", width=8, command=lambda: next_turn(), font=FONT_MAIN).pack(side="left", padx=10)
    
    # Keypad frame.
    keypad_frame = tk.Frame(init_win, bg=BG_COLOR)
    keypad_frame.pack(pady=5)
    for i, digit in enumerate(["0", "1", "2", "3", "4"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=0, column=i, padx=3, pady=3)
    for i, digit in enumerate(["5", "6", "7", "8", "9"]):
        btn = tk.Button(keypad_frame, text=digit, width=4, font=FONT_MAIN,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=1, column=i, padx=3, pady=3)
    
    # Control frame for Clear and Set buttons.
    control_frame = tk.Frame(init_win, bg=BG_COLOR)
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Clear", width=8, command=lambda: clear_position(), font=FONT_MAIN).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Set", width=8, command=lambda: add_initiative(), font=FONT_MAIN).grid(row=0, column=1, padx=5, pady=5)
    
    # Listbox for full initiative order.
    listbox = tk.Listbox(init_win, width=60, height=10, font=FONT_MAIN)
    listbox.pack(pady=10)
    
    def update_listbox():
        listbox.delete(0, tk.END)
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        for pos, name in sorted_order:
            listbox.insert(tk.END, f"{pos} | {name}")
        update_up_next()
    
    def add_initiative():
        name = name_entry.get().strip()
        pos_text = position_var.get().strip()
        if not name or not pos_text:
            return
        try:
            pos = int(pos_text)
        except ValueError:
            return
        initiative_order.append((pos, name))
        current_turn_index[0] = 0
        update_listbox()
        name_entry.delete(0, tk.END)
        position_var.set("")
    
    def reset_initiative():
        nonlocal initiative_order
        initiative_order = []
        current_turn_index[0] = 0
        update_listbox()
    
    def append_digit(digit):
        current = position_var.get()
        position_var.set(current + str(digit))
    
    def clear_position():
        position_var.set("")
    
    def update_up_next():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order and 0 <= current_turn_index[0] < len(sorted_order):
            pos, name = sorted_order[current_turn_index[0]]
            up_next_label.config(text=f"Up Next: {pos} | {name}")
        else:
            up_next_label.config(text="Up Next: N/A")
    
    def next_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] < len(sorted_order) - 1:
                current_turn_index[0] += 1
            else:
                current_turn_index[0] = 0
            update_up_next()
    
    def prev_turn():
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        if sorted_order:
            if current_turn_index[0] > 0:
                current_turn_index[0] -= 1
            else:
                current_turn_index[0] = len(sorted_order) - 1
            update_up_next()
    
    update_listbox()
    tk.Button(init_win, text="Reset Order", command=reset_initiative, font=FONT_MAIN).pack(pady=10)
    update_up_next()

####################################
# Tab: Classes & Feats
####################################
def create_classes_feats_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Classes section.
    classes_section = create_search_section(tab_frame,
                                            "Classes",
                                            "https://www.dndbeyond.com/rules",
                                            "https://www.dndbeyond.com/rules?filter-search={term}",
                                            extra_widget_func=create_class_buttons)
    classes_section.pack(fill="x", padx=10, pady=5)
    
    # Feats section.
    feats_section = create_search_section(tab_frame,
                                          "Feats",
                                          "https://www.dndbeyond.com/feats",
                                          "https://www.dndbeyond.com/feats?filter-name={term}&filter-prereq-subtype=&filter-partnered-content=f",
                                          extra_widget_func=create_default_feats_button)
    feats_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# Tab: Other Searches
####################################
def create_other_search_tab(notebook):
    tab_frame = tk.Frame(notebook, bg=BG_COLOR)
    
    # Magic Items section.
    magic_section = create_search_section(tab_frame,
                                          "Magic Items",
                                          "https://www.dndbeyond.com/magic-items",
                                          ("https://www.dndbeyond.com/magic-items?filter-search={term}"
                                           "&filter-type=0&filter-requires-attunement=&filter-effect-type=&filter-effect-subtype=&filter-has-charges=&filter-partnered-content=f"))
    magic_section.pack(fill="x", padx=10, pady=5)
    
    # Spells section.
    spells_section = create_search_section(tab_frame,
                                           "Spells",
                                           "https://www.dndbeyond.com/spells",
                                           "https://www.dndbeyond.com/spells?filter-search={term}")
    spells_section.pack(fill="x", padx=10, pady=5)
    
    # Equipment section.
    equipment_section = create_search_section(tab_frame,
                                              "Equipment",
                                              "https://www.dndbeyond.com/equipment",
                                              "https://www.dndbeyond.com/equipment?filter-search={term}")
    equipment_section.pack(fill="x", padx=10, pady=5)
    
    # Monsters section.
    monsters_section = create_search_section(tab_frame,
                                             "Monsters",
                                             "https://www.dndbeyond.com/monsters",
                                             "https://www.dndbeyond.com/monsters?filter-search={term}")
    monsters_section.pack(fill="x", padx=10, pady=5)
    
    return tab_frame

####################################
# Main Application Execution
####################################
def main():
    root = tk.Tk()
    root.title("D&D Toolset: Search, NPC Tracker & Character PDF")
    root.geometry("1000x800")
    
    # Apply custom D&D-themed styles.
    root.configure(bg=BG_COLOR)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", foreground=FG_COLOR, background=BG_COLOR, font=FONT_MAIN, padding=5)
    style.configure("TLabel", foreground=FG_COLOR, background=BG_COLOR, font=FONT_MAIN)
    style.configure("TEntry", foreground="black", background="white", font=FONT_MAIN)
    
    # Optionally, add a background image.
    """
    from PIL import Image, ImageTk
    try:
        bg_image = Image.open("parchment_bg.png")
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image not loaded:", e)
    """
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    # Create separate tabs for Classes & Feats and for Other Searches.
    classes_feats_tab = create_classes_feats_tab(notebook)
    other_search_tab = create_other_search_tab(notebook)
    npc_tracker_tab = create_npc_tracker_tab(notebook)
    character_pdf_tab = create_character_pdf_tab(notebook)
    
    notebook.add(classes_feats_tab, text="Classes & Feats")
    notebook.add(other_search_tab, text="Other Searches")
    notebook.add(npc_tracker_tab, text="NPC Tracker")
    notebook.add(character_pdf_tab, text="Character PDF")
    
    create_initiative_tracker_window()
    
    root.mainloop()

if __name__ == "__main__":
    main()
