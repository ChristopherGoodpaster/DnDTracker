import tkinter as tk
import webbrowser

def perform_search():
    option = search_option.get()
    search_term = entry.get().strip()
    search_term_lower = search_term.lower()
    
    if option == "magic":
        # For Magic Items, build the URL with several query parameters
        url = (
            "https://www.dndbeyond.com/magic-items?"
            "filter-type=0&"
            f"filter-search={search_term_lower}&"
            "filter-requires-attunement=&"
            "filter-effect-type=&"
            "filter-effect-subtype=&"
            "filter-has-charges=&"
            "filter-partnered-content=f"
        )
    elif option == "classes":
        base_url = "https://www.dndbeyond.com/classes"
        url = f"{base_url}?filter-search={search_term_lower}" if search_term else base_url
    elif option == "spells":
        base_url = "https://www.dndbeyond.com/spells"
        url = f"{base_url}?filter-search={search_term_lower}" if search_term else base_url
    elif option == "feats":
        base_url = "https://www.dndbeyond.com/feats"
        url = f"{base_url}?filter-search={search_term_lower}" if search_term else base_url
    elif option == "equipment":
        base_url = "https://www.dndbeyond.com/equipment"
        url = f"{base_url}?filter-search={search_term_lower}" if search_term else base_url
    elif option == "monsters":
        base_url = "https://www.dndbeyond.com/monsters"
        url = f"{base_url}?filter-search={search_term_lower}" if search_term else base_url
    else:
        status_label.config(text="Please select an option.", fg="red")
        return

    status_label.config(text=f"Opening {option} page...", fg="green")
    webbrowser.open(url)

# Create the main window
root = tk.Tk()
root.title("D&D Beyond Search")
root.geometry("550x250")

# Create a StringVar to store the selected option
search_option = tk.StringVar(value="magic")  # Default option

# Frame for radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack(pady=10)

# Define radio buttons for each option
options = [
    ("Magic Items", "magic"),
    ("Classes", "classes"),
    ("Spells", "spells"),
    ("Feats", "feats"),
    ("Equipment", "equipment"),
    ("Monsters", "monsters"),
]

for text, value in options:
    rb = tk.Radiobutton(
        radio_frame, text=text, variable=search_option,
        value=value
    )
    rb.pack(side="left", padx=5)

# Label for the entry widget
entry_label = tk.Label(root, text="Enter search term (optional):")
entry_label.pack(pady=5)

# Entry widget for typing the search term
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Button to perform the search
search_button = tk.Button(root, text="Go", command=perform_search)
search_button.pack(pady=10)

# Status label to show messages to the user
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
