# 🎮 Retro Game Randomizer (Mobile APK)

A lightweight, privacy-focused Android application designed to help retro gamers pick their next adventure. No more "analysis paralysis"—just upload your library, roll the dice, and start playing.

![Version](https://img.shields.io/badge/version-2.2-blue)
![Platform](https://img.shields.io/badge/platform-Android-green)
![Build](https://img.shields.io/github/actions/workflow/status/sheikhshahnawaz41299/Retro-Game-Randomizer/android_build.yml?branch=main)

## 🚀 Features

- **Zero-Latency Offline Mode:** No internet connection required. Your game lists stay on your device.
- **Multi-Console Support:** Separate memory slots for **PSP, PS1, PS2, and PS3**.
- **Smart Progress Tracking:** The app remembers which games you've already rolled so you never see the same game twice until you've finished the list.
- **Favorites System:** "Star" the games you're excited about and manage them in a dedicated favorites menu.
- **Privacy First:** No tracking, no data collection, and no "CORS" browser blocking issues.
- **Auto-Build on Every Commit:** The APK is automatically built and published whenever a change is pushed to the repository, so you always have the latest version available.

---

## 📲 Installation

1. Go to the **[Releases](https://github.com/sheikhshahnawaz41299/Retro-Game-Randomizer/releases)** section of this repository.
2. Download the latest `RetroRandomizer.apk`.
3. Open the file on your Android device.
4. If prompted, allow "Install from Unknown Sources" (since this is your own private build!).
5. Launch and play!

---

## 🛠 How to Use

### 1. Prepare your List
Create a simple `.txt` file for your games. Put **one game title per line**.
Example (`ps2_games.txt`):
```text
God Hand
Shadow of the Colossus
Metal Gear Solid 3
Final Fantasy X
```

### 2. Load your List into the App
- Open the app and select your console (PSP, PS1, PS2, or PS3).
- Tap **Import List** and select your `.txt` file.
- Your games will appear in the library for that console.

### 3. Roll the Dice
- Tap the **Randomize** button to get a random game suggestion.
- The app tracks what you've already been shown, so you won't see repeats until every game has been rolled.
- Tap **Mark as Played** to remove a game from the active pool.

### 4. Manage Favorites
- Tap the ⭐ icon next to any game to add it to your Favorites.
- Access your Favorites list from the main menu to roll only within games you're excited about.

---

## 🔄 CI/CD — Automatic Builds

This project uses **GitHub Actions** to build a fresh APK on every commit pushed to the repository. No manual builds needed.

- Workflow file: `.github/workflows/android_build.yml`
- Trigger: every `push` to any branch
- Output: `RetroRandomizer.apk` attached to the corresponding GitHub Release

If you fork this repo, the workflow will run automatically as long as GitHub Actions is enabled on your fork.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| UI | HTML / CSS / JavaScript |
| Mobile Wrapper | Capacitor |
| Android Build | Gradle |
| CI/CD | GitHub Actions |
| Runtime | Android (Java 21, Node.js 22) |

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request.

Every push will automatically trigger a build so you can verify your changes produce a working APK before merging.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
