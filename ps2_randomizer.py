import random
import json
import os
import urllib.request
import urllib.error
import ssl
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# 1. Bypass SSL errors globally
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# 2. Disguise Python as a normal browser
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(opener)

# NEW FIX: Pointing strictly to the compiled GitHub "Releases" links to avoid 404s!
CONSOLES = {
    "PS1": "https://github.com/niemasd/GameDB-PSX/releases/latest/download/PSX.titles.json",
    "PS2": "https://github.com/niemasd/GameDB-PS2/releases/latest/download/PS2.titles.json",
    "PS3": "https://github.com/niemasd/GameDB-PS3/releases/latest/download/PS3.titles.json",
    "PSP": "https://github.com/niemasd/GameDB-PSP/releases/latest/download/PSP.titles.json"
}

class RandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Game Randomizer V2.0")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)

        self.current_console = tk.StringVar(value="PSP") # Defaulted to PSP for you to test!
        self.files = {}
        self.all_games = []
        self.remaining_games = []

        self.setup_ui()
        self.change_console() 

    def get_files(self):
        prefix = self.current_console.get().lower()
        self.files = {
            'master': f'{prefix}_games.txt',
            'state': f'{prefix}_remaining.json',
            'history': f'{prefix}_history.txt',
            'favorites': f'{prefix}_favorites.txt'
        }

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=(0, 20))

        tk.Label(top_frame, text="Select Console:", font=("Arial", 14, "bold")).pack(side="left", padx=(0, 10))
        
        console_dropdown = ttk.Combobox(top_frame, textvariable=self.current_console, values=list(CONSOLES.keys()), state="readonly", width=10, font=("Arial", 12))
        console_dropdown.pack(side="left")
        console_dropdown.bind("<<ComboboxSelected>>", lambda e: self.change_console())

        self.stats_label = tk.Label(top_frame, text="Stats: Loading...", font=("Arial", 12), fg="blue")
        self.stats_label.pack(side="right")

        self.games_frame = tk.LabelFrame(self.root, text=" Your 10 Random Games ", font=("Arial", 12, "bold"), padx=10, pady=10)
        self.games_frame.pack(fill="both", expand=True, pady=(0, 20))

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x")

        tk.Button(bottom_frame, text="🎲 Roll 10 Games", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=self.roll_games, padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="⭐ Manage Favorites", font=("Arial", 12), command=self.manage_favorites, padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="⚠️ Factory Reset", font=("Arial", 12), fg="red", command=self.factory_reset, padx=10, pady=5).pack(side="right", padx=5)

    def change_console(self):
        self.get_files()
        console_name = self.current_console.get()
        url = CONSOLES[console_name]

        # AUTO-CLEAN: Delete corrupted 404 text files automatically
        if os.path.exists(self.files['master']):
            try:
                with open(self.files['master'], 'r', encoding='utf-8', errors='ignore') as f:
                    preview = f.read(1000).lower()
                if "<html" in preview or "404" in preview or "not found" in preview or os.path.getsize(self.files['master']) < 100:
                    os.remove(self.files['master'])
            except:
                pass

        # Download if missing
        if not os.path.exists(self.files['master']):
            self.stats_label.config(text="Downloading database... Please wait.", fg="orange")
            self.root.update() 
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    data = response.read().decode('utf-8')

                # Parse the JSON databases into our clean text format
                json_data = json.loads(data)
                titles = sorted(list(set(json_data.values())))
                with open(self.files['master'], 'w', encoding='utf-8') as f:
                    for title in titles:
                        if title.strip():
                            f.write(f"{title.strip()}\n")
                        
            except Exception as e:
                messagebox.showerror("Download Error", f"Failed to download {console_name} list.\n\nError: {str(e)}")
                self.stats_label.config(text="Download Failed", fg="red")
                return

        self.load_pools()
        self.update_stats()
        
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

        with open(self.files['state'], 'w', encoding='utf-8') as f:
            json.dump(self.remaining_games, f, indent=4)

        with open(self.files['history'], 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"--- Roll on {timestamp} ---\n")
            for index, game in enumerate(selected_games, 1):
                f.write(f"{index}. {game}\n")
            f.write("\n")

        self.update_stats()
        self.display_games(selected_games)

    def display_games(self, games):
        for widget in self.games_frame.winfo_children():
            widget.destroy()

        for index, game in enumerate(games, 1):
            row = tk.Frame(self.games_frame)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=f"{index}. {game}", font=("Arial", 12), anchor="w").pack(side="left", fill="x", expand=True)
            tk.Button(row, text="📋 Copy", width=8, command=lambda g=game: self.copy_to_clipboard(g)).pack(side="right", padx=5)
            tk.Button(row, text="⭐ Fav", width=8, command=lambda g=game: self.save_favorite(g)).pack(side="right", padx=5)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("Copied", f"Copied to clipboard:\n{text}")

    def save_favorite(self, game):
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
            
            for i in reversed(selected_indices):
                listbox.delete(i)
                favorites.pop(i)

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
            self.change_console() 
            messagebox.showinfo("Reset Complete", "The console pool has been completely reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomizerApp(root)
    root.mainloop()
