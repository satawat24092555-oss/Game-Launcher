import json
import os
import customtkinter as ctk
from customtkinter import filedialog
import sys

data = []

# Functions

def save_data():
    file_path = os.path.join(os.path.dirname(__file__), "Data.json")

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "Data.json")

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump([], file)

    with open(file_path, "r") as file:
        data = json.load(file)

    return data

def show_pop_up():
    game_name_label.grid(row=0, column=1, pady=(20, 10))
    game_entry.grid(row=1, column=1, pady=(0, 15))
    confirm_button.grid(row=2, column=1, pady=(0, 20))
    
    pop_up.place(relx=0.5, rely=0.5, anchor="center")
    pop_up.lift()

selected_file_path = ""

def add_game():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()
    if selected_file_path:
        show_pop_up()

def confirm_add_game():
    game_name = game_entry.get()

    if game_name == "" or " " in game_name: return
    
    new_game = {
        "name": game_name,
        "path": selected_file_path
    }
    
    data.append(new_game)
    save_data()
    pop_up.place_forget()
    game_entry.delete(0, 'end')
    refresh_game_list()

def delete_game(game):
    data.remove(game)
    save_data()
    refresh_game_list()

def play_game(game):
    path = game["path"]

    os.startfile(path)

def refresh_game_list():
    for widget in scrollbox.winfo_children():
        widget.destroy()

    rowi = 0
    columni = 0

    for game in data:
        if columni == 3:
            rowi += 1
            columni = 0
        
        create_box_game(game, rowi, columni)
        columni += 1

def create_box_game(game, rowi, columni):
    game_box = ctk.CTkFrame(master=scrollbox, width=159, height=137, corner_radius=10, fg_color="#1b1b1c")
    game_box.columnconfigure(0, weight=1)
    game_box.columnconfigure(1, weight=1)
    game_box.columnconfigure(2, weight=1)
    game_box.grid_propagate(False)

    box_name = ctk.CTkLabel(master=game_box, font=("Prompt", 15), text="name", text_color="#f6f2ec")
    box_delete = ctk.CTkButton(master=game_box, width=120, height=33, fg_color="#f44336", hover_color="#f36257", text="Delete", text_color="#f6f2ec")
    box_play = ctk.CTkButton(master=game_box, width=120, height=33, fg_color="#69ae6c", hover_color="#7cce80", text="Play", text_color="#f6f2ec")

    game_box.grid(row=rowi, column=columni, padx=10, pady=10)
    box_name.grid(row=0, column=1, pady=5)
    box_name.configure(text=game["name"])
    box_delete.grid(row=1, column=1, pady=5)
    box_delete.configure(command=lambda game=game: delete_game(game))
    box_play.grid(row=2, column=1, pady=5)
    box_play.configure(command=lambda game=game: play_game(game))

data = load_data()

# Gui
# window

window = ctk.CTk()
window.geometry("700x500")
window.configure(fg_color="#cd9c8e")
window.title("Game Launcher")

if getattr(sys, "frozen", False):
    icon_path = os.path.join(sys._MEIPASS, "folderyellowgames.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "folderyellowgames.ico")

window.iconbitmap(icon_path)

# leftFrame

leftFrame = ctk.CTkFrame(master=window, width=153, height=500, corner_radius=0, fg_color="#1b1b1c")
leftFrame.columnconfigure(0, weight=1)
leftFrame.columnconfigure(1, weight=1)
leftFrame.columnconfigure(2, weight=1)
leftFrame.grid_propagate(False)

Menu_label = ctk.CTkLabel(master=leftFrame, font=("Prompt", 21), text_color="#f6f2ec", text="Menu")
game_list_button = ctk.CTkButton(master=leftFrame, width=95, height=24, font=("Prompt", 15), fg_color="#1b1b1c", hover_color="#2d2e2e", text="Game List")
add_button = ctk.CTkButton(master=leftFrame, width=130, height=36, font=("Prompt", 15), fg_color="#e1a23b", hover_color="#f9b74c", text="Add Game", text_color="#000000", command=add_game)
save_button = ctk.CTkButton(master=leftFrame, width=130, height=36, font=("Prompt", 15), fg_color="#3e91ec", hover_color="#3EBEEC", text="Save", text_color="#000000", command=save_data)

# upFrame

current_ui = "Game List"

upFrame = ctk.CTkFrame(master=window, width=546, height=50, corner_radius=0, fg_color="#cd9c8e")
upFrame.grid_propagate(False)

Topic_Label = ctk.CTkLabel(master=upFrame, font=("Prompt", 21), text_color="#2c415b", text=current_ui)

# midFrame

midFrame = ctk.CTkFrame(master=window, width=546, height=450, corner_radius=0, fg_color="#cd9c8e")
midFrame.grid_propagate(False)

scrollbox = ctk.CTkScrollableFrame(master=midFrame, width=546, height=450, corner_radius=0, fg_color="#cd9c8e")

# add game pop up
pop_up = ctk.CTkFrame(master=window, width=380, height=260, corner_radius=16, fg_color="#1b1b1c", border_width=1, border_color="#2d2e2e")
pop_up.columnconfigure(0, weight=1)
pop_up.columnconfigure(1, weight=1)
pop_up.columnconfigure(2, weight=1)
pop_up.grid_propagate(False)

game_name_label = ctk.CTkLabel(master=pop_up, font=("Prompt", 16), text_color="#f6f2ec", text="Game Name")
game_entry = ctk.CTkEntry(master=pop_up, width=220, height=38, fg_color="#2d2e2e", text_color="#f6f2ec", border_color="#3e3f40", border_width=1, corner_radius=8)

confirm_button = ctk.CTkButton(master=pop_up, width=120, height=32, font=("Prompt", 14), fg_color="#e1a23b", hover_color="#f9b74c", text="Confirm", text_color="#000000", corner_radius=8, command=confirm_add_game)

# แสดงกรอบหัวข้อ leftFrame
leftFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")

Menu_label.grid(row=0, column=1, pady=10)
game_list_button.grid(row=1, column=1,pady=10)

add_button.place(relx=0.5, y=383, anchor="center")
save_button.place(relx=0.5, y=431, anchor="center")

# แสดงกรอบหัวข้อ upFrame
upFrame.grid(row=0, column=1, sticky="ne")

Topic_Label.grid(row=0, column=0, padx=10, pady=10)

# แสดงกรอบหัวข้อ midFrame
midFrame.grid(row=1, column=1, sticky="se")

scrollbox.grid()

rowi = 0
columni = 0

for game in data:
    if columni == 3:
        rowi += 1
        columni = 0
    
    create_box_game(game, rowi, columni)
    columni += 1

window.resizable(False, False)
window.mainloop()