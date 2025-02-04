import tkinter as tk
from tkinter import ttk

def create_initiative_tracker_gui():
    root = tk.Tk()
    root.title("Initiative Tracker")
    root.geometry("400x300")

    # This list will store tuples: (initiative_position, name)
    initiative_order = []

    def update_listbox():
        listbox.delete(0, tk.END)
        # Sort by initiative position (numerical order)
        sorted_order = sorted(initiative_order, key=lambda x: x[0])
        for pos, name in sorted_order:
            listbox.insert(tk.END, f"Position {pos}: {name}")

    def add_initiative():
        name = name_entry.get().strip()
        pos_text = pos_entry.get().strip()
        if not name:
            return
        try:
            pos = int(pos_text)
        except ValueError:
            return
        initiative_order.append((pos, name))
        update_listbox()
        # Clear entries after adding
        name_entry.delete(0, tk.END)
        pos_entry.delete(0, tk.END)

    def reset_initiative():
        nonlocal initiative_order
        initiative_order = []
        update_listbox()

    # Create input frame for adding a new initiative entry
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(input_frame, width=20)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Position:").grid(row=0, column=2, padx=5, pady=5)
    pos_entry = tk.Entry(input_frame, width=5)
    pos_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Button(input_frame, text="Confirm", command=add_initiative).grid(row=0, column=4, padx=5, pady=5)

    # Listbox to display the initiative order
    listbox = tk.Listbox(root, width=50)
    listbox.pack(pady=10)

    # Button to reset the initiative order
    tk.Button(root, text="Reset Order", command=reset_initiative).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_initiative_tracker_gui()
