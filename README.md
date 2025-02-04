# DnDTracker

D&D Toolset GUI
A Python-based desktop application that provides a suite of tools for Dungeons & Dragons players and Dungeon Masters. This toolset features integrated searches on D&D Beyond, NPC tracking, character PDF uploads, and an initiative tracker—all wrapped in a custom D&D-themed graphical user interface built with Tkinter.

Overview
The D&D Toolset GUI is designed to streamline various aspects of your D&D game management:

D&D Beyond Search:

Classes & Feats Tab: Search for classes and feats quickly. The Classes section displays a grid of buttons (linked to the "PHB D&D Free Rules (2024)") and the Feats section includes a default feats button.
Other Searches Tab: Search for Magic Items, Spells, Equipment, and Monsters—all organized as separate sections with their own search bars.
NPC Tracker:
Easily track up to 12 NPCs with details such as name, level, health, and spell slots. Quick-adjust buttons allow you to update health in real time.

Character PDF Viewer:
Upload and view your character sheet PDFs directly within the application.

Initiative Tracker:
A separate window to manage turn order during combat. Features include a numeric keypad, navigation buttons (next/prev), and a list displaying the full initiative order.

The application uses a custom D&D-themed color scheme and fonts (using Garamond and gold accents) to enhance the overall experience.

Features
Integrated D&D Beyond Searches:
Two separate tabs for:

Classes & Feats: Contains dedicated sections for classes (with clickable buttons) and feats (with a default button).
Other Searches: Separate sections for Magic Items, Spells, Equipment, and Monsters.
NPC Tracker:
Manage NPC health, levels, and spell slots with quick adjustments and a grid layout.

Character PDF Upload:
Easily upload and display character PDF files.

Initiative Tracker:
Manage and view initiative order with an intuitive interface including a numeric keypad and navigation controls.

Requirements
Python 3.x
Tkinter: Comes pre-installed with most Python distributions.
PyPDF2: For reading and extracting text from PDF files.
Install via pip:
bash
Copy
pip install PyPDF2
Pillow (Optional): For background image support.
Install via pip:
bash
Copy
pip install pillow
Installation
Clone the repository:
bash
Copy
git clone https://github.com/yourusername/your-repo-name.git
Navigate to the project directory:
bash
Copy
cd your-repo-name
(Optional) Set up a virtual environment and install dependencies:
bash
Copy
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install PyPDF2 pillow
Usage
Run the application by executing the main Python file:

bash
Copy
python main.py
The main window will open with multiple tabs:

Classes & Feats: Use the search bars to query D&D Beyond for class and feat information.
Other Searches: Search for Magic Items, Spells, Equipment, and Monsters.
NPC Tracker: Manage NPC details.
Character PDF: Upload and view character sheets.
An additional Initiative Tracker window will open for managing combat order.
Contributing
Contributions, suggestions, and bug reports are welcome! Please feel free to submit an issue or pull request.

License
This project is licensed under the MIT License.
