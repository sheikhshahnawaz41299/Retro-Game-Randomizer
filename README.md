# 🎮 Retro Game Randomizer V2.0

A lightweight, GUI-based Python application that helps you discover games from massive retro console libraries (PS1, PS2, PS3, PSP) without ever rolling the same game twice. 

Whether you are looking for your next emulation playthrough or just want to explore the deepest, weirdest cuts of the PlayStation era, this app tracks your progress, logs your history, and lets you save your favorites.

---

## ✨ Features

* 🖥️ **Interactive GUI:** Built with Python's native Tkinter for a clean, windowed user experience—no more staring at a command line.
* 🕹️ **Multi-Console Support:** Swap between PS1, PS2, PS3, and PSP databases seamlessly. The app manages separate tracking files for each console.
* 🎲 **Smart Randomizer:** Pulls 10 random games at a time and removes them from the active pool so you never see duplicates.
* 📊 **Progress Tracking:** A live dashboard shows exactly how many games you've rolled and your total library completion percentage.
* 📋 **Quick Copy:** A one-click button next to every roll copies the game title straight to your clipboard for easy Google/YouTube searching.
* ⭐ **Favorites Manager:** Save the bangers to a dedicated list and manage/delete them using a clean pop-up UI.
* 💾 **Local Saving:** Automatically creates text logs of your roll history and JSON files of your remaining game pools so you never lose your progress.

---

## 🛠️ Requirements

This application is built with standard Python libraries. **No external dependencies or `pip installs` are required!**

* **Python 3.x** or higher
* An active internet connection (only required for the **very first run** of a new console to download the master database list).

---

## 🚀 How to Run

1. Clone or download this repository to your local machine.
2. Open your terminal or command prompt.
3. Navigate to the folder containing the script.
4. Run the application using:
   ```bash
   python randomizer.py
