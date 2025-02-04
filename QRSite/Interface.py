import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import webbrowser
import PyPDF2

####################################
# D&D Beyond Search Tab Functions  #
####################################
def create_dnd_search_tab(notebook):
    search_frame = ttk.Frame(notebook)
    
    # Dictionary mapping ruleset section to its class URLs.
    # Only one section ("PHB D&D Free Rules (2024)") is retained.
    ruleset_classes = {
        "PHB D&D Free Rules (2024)": {
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
    }

    search_option = tk.StringVar(value="magic")

    radio_frame = tk.Frame(search_frame)
    radio_frame.pack(pady=8)

    options = [
        ("Magic Items", "magic"),
        ("Classes", "classes"),
        ("Spells", "spells"),
        ("Feats", "feats"),
        ("Equipment", "equipment"),
        ("Monsters", "monsters"),
    ]
    for text, value in options:
        rb = tk.Radiobutton(radio_frame, text=text, variable=search_option, value=value)
        rb.pack(side="left", padx=4)

    tk.Label(search_frame, text="Enter search term (optional):").pack(pady=4)
    
    search_bar_frame = tk.Frame(search_frame)
    search_bar_frame.pack(pady=4)
    
    entry = tk.Entry(search_bar_frame, width=40)
    entry.pack(side="left", padx=(0, 5))
    
    go_button = tk.Button(search_bar_frame, text="Go", padx=6, pady=2)
    go_button.pack(side="left")
    
    default_button_frame = tk.Frame(search_frame)
    default_button_frame.pack(pady=4)
    
    def update_default_button(*args):
        for widget in default_button_frame.winfo_children():
            widget.destroy()
        if search_option.get() == "feats":
            btn = tk.Button(default_button_frame, text="Default Feats", 
                            command=lambda: show_default_feats())
            btn.pack()
    def show_default_feats():
        entry.delete(0, tk.END)
        perform_search()
        
    search_option.trace_add("write", update_default_button)
    update_default_button()

    classes_buttons_frame = tk.Frame(search_frame)
    classes_buttons_frame.pack(pady=4, fill="x")

    def update_class_buttons(*args):
        for widget in classes_buttons_frame.winfo_children():
            widget.destroy()
        if search_option.get() == "classes":
            for section, classes in ruleset_classes.items():
                header = tk.Label(classes_buttons_frame, text=section, font=("Arial", 10, "bold"))
                header.pack(anchor="center", pady=(4,0))
                btn_frame = tk.Frame(classes_buttons_frame)
                btn_frame.pack(anchor="center", padx=10, pady=(0,4))
                i = 0
                for cls, url in classes.items():
                    btn = tk.Button(btn_frame, text=cls, command=lambda u=url: webbrowser.open(u),
                                    width=20, height=2)
                    btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
                    i += 1
    search_option.trace_add("write", update_class_buttons)
    update_class_buttons()

    status_label = tk.Label(search_frame, text="")
    status_label.pack(pady=4)

    def perform_search():
        option = search_option.get()
        search_term = entry.get().strip().lower()

        if option == "magic":
            url = (
                "https://www.dndbeyond.com/magic-items?"
                "filter-type=0&"
                f"filter-search={search_term}&"
                "filter-requires-attunement=&"
                "filter-effect-type=&"
                "filter-effect-subtype=&"
                "filter-has-charges=&"
                "filter-partnered-content=f"
            )
        elif option == "classes":
            found = False
            for section, classes in ruleset_classes.items():
                for cls, url_candidate in classes.items():
                    if search_term == cls.lower():
                        url = url_candidate
                        found = True
                        break
                if found:
                    break
            if not found:
                base_url = "https://www.dndbeyond.com/rules"
                url = f"{base_url}?filter-search={search_term}" if search_term else base_url
        elif option == "feats":
            if search_term:
                url = f"https://www.dndbeyond.com/feats?filter-name={search_term}&filter-prereq-subtype=&filter-partnered-content=f"
            else:
                url = "https://www.dndbeyond.com/feats"
        else:
            base_urls = {
                "spells": "https://www.dndbeyond.com/spells",
                "equipment": "https://www.dndbeyond.com/equipment",
                "monsters": "https://www.dndbeyond.com/monsters"
            }
            base_url = base_urls.get(option, "")
            url = f"{base_url}?filter-search={search_term}" if search_term else base_url

        status_label.config(text=f"Opening {option} page...", fg="green")
        webbrowser.open(url)

    go_button.config(command=perform_search)
    return search_frame

####################################
# NPC Tracker Tab Functions        #
####################################
class NPCFrame(tk.Frame):
    def __init__(self, master, npc_number, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.npc_number = npc_number
        self.health = 0
        self.spell_slots = {1: 4, 2: 3, 3: 3, 4: 3}
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text=f"NPC {self.npc_number}", font=("Arial", 10, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=(2,4))

        tk.Label(self, text="Name:").grid(row=1, column=0, sticky="e", padx=2, pady=2)
        self.name_entry = tk.Entry(self, width=12)
        self.name_entry.grid(row=1, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self, text="Level:").grid(row=1, column=2, sticky="e", padx=2, pady=2)
        self.level_entry = tk.Entry(self, width=4)
        self.level_entry.grid(row=1, column=3, sticky="w", padx=2, pady=2)

        tk.Label(self, text="Health:").grid(row=2, column=0, sticky="e", padx=2, pady=2)
        self.health_entry = tk.Entry(self, width=8, justify="center")
        self.health_entry.grid(row=2, column=1, sticky="w", padx=2, pady=2)
        self.health_entry.insert(0, str(self.health))
        
        self.set_health_btn = tk.Button(self, text="Set", command=self.set_health, padx=2, pady=1)
        self.set_health_btn.grid(row=2, column=2, padx=2, pady=2)

        tk.Label(self, text="Adj:").grid(row=3, column=0, sticky="e", padx=2, pady=2)
        self.adjustment_entry = tk.Entry(self, width=8, justify="center")
        self.adjustment_entry.grid(row=3, column=1, sticky="w", padx=2, pady=2)
        self.adjustment_entry.insert(0, "0")
        
        self.adjust_health_btn = tk.Button(self, text="Apply", command=self.adjust_health, padx=2, pady=1)
        self.adjust_health_btn.grid(row=3, column=2, padx=2, pady=2)

        quick_frame = tk.Frame(self)
        quick_frame.grid(row=4, column=0, columnspan=4, padx=2, pady=(2,4))
        plus_frame = tk.Frame(quick_frame)
        plus_frame.pack(pady=(0,2))
        for inc in [1, 2, 5, 10, 15]:
            btn = tk.Button(plus_frame, text=f"+{inc}", command=lambda inc=inc: self.quick_adjust(inc),
                            padx=2, pady=1, font=("Arial", 8))
            btn.pack(side="left", padx=2)
        minus_frame = tk.Frame(quick_frame)
        minus_frame.pack()
        for dec in [1, 2, 5, 10, 15]:
            btn = tk.Button(minus_frame, text=f"-{dec}", command=lambda dec=dec: self.quick_adjust(-dec),
                            padx=2, pady=1, font=("Arial", 8))
            btn.pack(side="left", padx=2)

        row = 5
        self.spell_slot_labels = {}
        for lvl in range(1, 5):
            tk.Label(self, text=f"Lvl {lvl}:", font=("Arial", 8)).grid(row=row, column=0, sticky="e", padx=2, pady=1)
            self.spell_slot_labels[lvl] = tk.Label(self, text=str(self.spell_slots[lvl]), width=3, relief="sunken", font=("Arial", 8))
            self.spell_slot_labels[lvl].grid(row=row, column=1, sticky="w", padx=2, pady=1)
            btn_consume = tk.Button(self, text="-", command=lambda l=lvl: self.adjust_spell_slot(l, -1), padx=2, pady=1, font=("Arial", 8))
            btn_consume.grid(row=row, column=2, padx=2, pady=1)
            btn_restore = tk.Button(self, text="+", command=lambda l=lvl: self.adjust_spell_slot(l, 1), padx=2, pady=1, font=("Arial", 8))
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
# Character PDF Tab Functions      #
####################################
def create_character_pdf_tab(notebook):
    pdf_frame = ttk.Frame(notebook)
    
    status_label = tk.Label(pdf_frame, text="Upload your Goody83 PDF", font=("Arial", 12))
    status_label.pack(pady=5)

    text_area = scrolledtext.ScrolledText(pdf_frame, wrap=tk.WORD, width=100, height=30)
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

    tk.Button(pdf_frame, text="Upload PDF", command=upload_pdf, padx=4, pady=2).pack(pady=8)
    return pdf_frame

####################################
# Initiative Tracker Window        #
####################################
def create_initiative_tracker_window():
    init_win = tk.Toplevel()
    init_win.title("Initiative Tracker")
    init_win.geometry("500x500")
    
    initiative_order = []
    current_turn_index = [0]  # one-element list for mutable index
    
    # Top frame: Name, Pos entry and Reset Order button.
    top_frame = ttk.Frame(init_win)
    top_frame.pack(pady=10, fill="x")
    
    tk.Label(top_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(top_frame, width=20)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(top_frame, text="Pos:").grid(row=0, column=2, padx=5, pady=5)
    position_var = tk.StringVar()
    pos_display = tk.Entry(top_frame, textvariable=position_var, width=8, justify="center", state="readonly")
    pos_display.grid(row=0, column=3, padx=5, pady=5)
    
    reset_btn = tk.Button(top_frame, text="Reset Order", command=lambda: reset_initiative())
    reset_btn.grid(row=0, column=4, padx=5, pady=5)
    
    # "Up Next" section.
    up_next_frame = ttk.Frame(init_win)
    up_next_frame.pack(pady=10, fill="x")
    up_next_label = tk.Label(up_next_frame, text="Up Next: N/A", font=("Arial", 12, "bold"))
    up_next_label.pack(anchor="center", padx=5)
    
    # Prev/Next buttons placed immediately below "Up Next"
    nav_frame = ttk.Frame(init_win)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Prev", width=8, command=lambda: prev_turn()).pack(side="left", padx=10)
    tk.Button(nav_frame, text="Next", width=8, command=lambda: next_turn()).pack(side="left", padx=10)
    
    # Keypad frame.
    keypad_frame = ttk.Frame(init_win)
    keypad_frame.pack(pady=5)
    for i, digit in enumerate(["0", "1", "2", "3", "4"]):
        btn = tk.Button(keypad_frame, text=digit, width=4,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=0, column=i, padx=3, pady=3)
    for i, digit in enumerate(["5", "6", "7", "8", "9"]):
        btn = tk.Button(keypad_frame, text=digit, width=4,
                        command=lambda t=digit: append_digit(t))
        btn.grid(row=1, column=i, padx=3, pady=3)
    
    # Control frame for Clear and Set buttons.
    control_frame = ttk.Frame(init_win)
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Clear", width=8, command=lambda: clear_position()).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Set", width=8, command=lambda: add_initiative()).grid(row=0, column=1, padx=5, pady=5)
    
    # Listbox for full initiative order.
    listbox = tk.Listbox(init_win, width=60, height=10, font=("Arial", 12))
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
    tk.Button(init_win, text="Reset Order", command=reset_initiative).pack(pady=10)
    update_up_next()

####################################
# Main Application Execution       #
####################################
def main():
    root = tk.Tk()
    root.title("D&D Toolset: Search, NPC Tracker & Character PDF")
    root.geometry("1000x800")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    dnd_search_tab = create_dnd_search_tab(notebook)
    npc_tracker_tab = create_npc_tracker_tab(notebook)
    character_pdf_tab = create_character_pdf_tab(notebook)

    notebook.add(dnd_search_tab, text="D&D Beyond Search")
    notebook.add(npc_tracker_tab, text="NPC Tracker")
    notebook.add(character_pdf_tab, text="Character PDF")

    create_initiative_tracker_window()

    root.mainloop()

if __name__ == "__main__":
    main()
