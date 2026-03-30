import random
import json
import os
import urllib.request
import urllib.error
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Dictionary of consoles and their master list URLs 
CONSOLES = {
    "PS1": "https://raw.githubusercontent.com/namuol/titlegen/master/titles/games/ps1.txt",
    "PS2": "https://raw.githubusercontent.com/namuol/titlegen/master/titles/games/ps2.txt",
    "PS3": "https://raw.githubusercontent.com/namuol/titlegen/master/titles/games/ps3.txt",
    "PSP": "https://raw.githubusercontent.com/namuol/titlegen/master/titles/games/psp.txt"
}

class RandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Game Randomizer V2.0")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)

        self.current_console = tk.StringVar(value="PS2")
        self.files = {}
        self.all_games = []
        self.remaining_games = []

        self.setup_ui()
        self.change_console() # Load initial console data

    def get_files(self):
        prefix = self.current_console.get().lower()
        self.files = {
            'master': f'{prefix}_games.txt',
            'state': f'{prefix}_remaining.json',
            'history': f'{prefix}_history.txt',
            'favorites': f'{prefix}_favorites.txt'
        }

    def setup_ui(self):
        # --- Top Section: Console Selection & Stats ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=(0, 20))

        tk.Label(top_frame, text="Select Console:", font=("Arial", 14, "bold")).pack(side="left", padx=(0, 10))
        
        console_dropdown = ttk.Combobox(top_frame, textvariable=self.current_console, values=list(CONSOLES.keys()), state="readonly", width=10, font=("Arial", 12))
        console_dropdown.pack(side="left")
        console_dropdown.bind("<<ComboboxSelected>>", lambda e: self.change_console())

        self.stats_label = tk.Label(top_frame, text="Stats: Loading...", font=("Arial", 12), fg="blue")
        self.stats_label.pack(side="right")

        # --- Middle Section: The 10 Games Display ---
        self.games_frame = tk.LabelFrame(self.root, text=" Your 10 Random Games ", font=("Arial", 12, "bold"), padx=10, pady=10)
        self.games_frame.pack(fill="both", expand=True, pady=(0, 20))

        self.game_rows = [] # Will hold the UI elements for the 10 games

        # --- Bottom Section: Action Buttons ---
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x")

        tk.Button(bottom_frame, text="🎲 Roll 10 Games", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=self.roll_games, padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="⭐ Manage Favorites", font=("Arial", 12), command=self.manage_favorites, padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="⚠️ Factory Reset", font=("Arial", 12), fg="red", command=self.factory_reset, padx=10, pady=5).pack(side="right", padx=5)

    def change_console(self):
        self.get_files()
        console_name = self.current_console.get()
        url = CONSOLES[console_name]

        # Download if missing
        if not os.path.exists(self.files['master']):
            self.stats_label.config(text="Downloading database... Please wait.", fg="orange")
            self.root.update() # Force UI to update before downloading
            try:
                urllib.request.urlretrieve(url, self.files['master'])
            except Exception:
                messagebox.showerror("Download Error", f"Failed to download {console_name} list. Check internet.")
                return

        self.load_pools()
        self.update_stats()
        
        # Clear the display when switching consoles
        for widget in self.games_frame.winfo_children():
            widget.destroy()

    def load_pools(self):
        with open(self.files['master'], 'r', encoding='utf-8') as f:
            self.all_games = [line.strip() for line in f if line.strip()]
            
        if os.path.exists(self.files['state']):
            with open(self.files['state'], 'r', encoding='utf-8') as f:
                self.remaining_games = json.load(f)
        else:
            self.remaining_games = self.all_games.copy()

    def update_stats(self):
        total = len(self.all_games)
        remaining = len(self.remaining_games)
        rolled = total - remaining
        if total > 0:
            percentage = (rolled / total) * 100
            self.stats_label.config(text=f"Library Progress: {rolled}/{total} games ({percentage:.1f}%)", fg="blue")
        else:
            self.stats_label.config(text="Library Progress: 0/0 (0%)")

    def roll_games(self):
        if len(self.remaining_games) == 0:
            messagebox.showinfo("All Done!", "You've rolled every game for this console! Hit Factory Reset to start over.")
            return

        games_to_pick = min(10, len(self.remaining_games))
        selected_games = random.sample(self.remaining_games, games_to_pick)

        for game in selected_games:
            self.remaining_games.remove(game)

        # Save state
        with open(self.files['state'], 'w', encoding='utf-8') as f:
            json.dump(self.remaining_games, f, indent=4)

        # Save history
        with open(self.files['history'], 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"--- Roll on {timestamp} ---\n")
            for index, game in enumerate(selected_games, 1):
                f.write(f"{index}. {game}\n")
            f.write("\n")

        self.update_stats()
        self.display_games(selected_games)

    def display_games(self, games):
        # Clear the previous games
        for widget in self.games_frame.winfo_children():
            widget.destroy()

        for index, game in enumerate(games, 1):
            row = tk.Frame(self.games_frame)
            row.pack(fill="x", pady=5)

            # Game Title
            tk.Label(row, text=f"{index}. {game}", font=("Arial", 12), anchor="w").pack(side="left", fill="x", expand=True)

            # Copy Button
            tk.Button(row, text="📋 Copy", width=8, command=lambda g=game: self.copy_to_clipboard(g)).pack(side="right", padx=5)
            
            # Favorite Button
            tk.Button(row, text="⭐ Fav", width=8, command=lambda g=game: self.save_favorite(g)).pack(side="right", padx=5)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update() # Keep clipboard active after closing
        messagebox.showinfo("Copied", f"Copied to clipboard:\n{text}")

    def save_favorite(self, game):
        # Check if already in favorites to avoid duplicates
        if os.path.exists(self.files['favorites']):
            with open(self.files['favorites'], 'r', encoding='utf-8') as f:
                if game in f.read():
                    messagebox.showinfo("Favorites", "This game is already in your favorites!")
                    return

        with open(self.files['favorites'], 'a', encoding='utf-8') as f:
            f.write(f"{game}\n")
        messagebox.showinfo("Favorites", f"Saved '{game}' to favorites!")

    def manage_favorites(self):
        if not os.path.exists(self.files['favorites']):
            messagebox.showinfo("Favorites", "Your favorites list is empty!")
            return

        with open(self.files['favorites'], 'r', encoding='utf-8') as f:
            favorites = [line.strip() for line in f if line.strip()]

        if not favorites:
            messagebox.showinfo("Favorites", "Your favorites list is empty!")
            return

        # Create a new popup window for favorites
        fav_window = tk.Toplevel(self.root)
        fav_window.title(f"{self.current_console.get()} Favorites")
        fav_window.geometry("500x400")

        listbox = tk.Listbox(fav_window, font=("Arial", 12), selectmode=tk.EXTENDED)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for game in favorites:
            listbox.insert(tk.END, game)

        def delete_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                return
            
            # Remove from listbox and list backwards to not mess up index order
            for i in reversed(selected_indices):
                listbox.delete(i)
                favorites.pop(i)

            # Save updated list
            with open(self.files['favorites'], 'w', encoding='utf-8') as f:
                for game in favorites:
                    f.write(f"{game}\n")

        tk.Button(fav_window, text="🗑️ Remove Selected", bg="red", fg="white", font=("Arial", 12), command=delete_selected).pack(pady=10)

    def factory_reset(self):
        confirm = messagebox.askyesno("Factory Reset", f"Are you sure you want to delete all history, stats, and favorites for {self.current_console.get()}? This cannot be undone.")
        if confirm:
            for key in ['state', 'history', 'favorites']:
                if os.path.exists(self.files[key]):
                    os.remove(self.files[key])
            self.change_console() # Reload everything fresh
            messagebox.showinfo("Reset Complete", "The console pool has been completely reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomizerApp(root)
    root.mainloop()
