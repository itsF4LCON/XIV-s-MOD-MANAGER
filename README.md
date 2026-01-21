# XIV's Mod Manager

XIV's Mod Manager is a Minecraft Mod Manager that allows users to maintain and switch between multiple mod folders for different Minecraft versions. This tool simplifies managing mods without manually moving files.

---

## Description

XIV's Mod Manager helps Minecraft players organize mods per version. Each version can have its own dedicated `mods` folder, and the manager allows switching between them quickly and safely. The active version is tracked automatically to prevent conflicts.

This version is compiled as a standalone Windows executable, so Python is not required to run it.

---

## Features

- Select Minecraft folder manually or use auto-detect.
- Add and manage multiple mod versions.
- Switch between mod versions with a single click.
- Active version tracking to prevent mod conflicts.
- User-friendly interface built with CustomTkinter.
- Runs as a standalone Windows executable (`.exe`).

---

## Installation

1. Download the latest `.exe` release from the repository's **Releases** section.
2. Place the `.exe` anywhere on your computer.
3. Double-click to launch the application.

> Note: If you want to use the Python source version, Python 3.10+ is required, along with the `customtkinter` and `pillow` packages.

---

## Usage

1. Launch the executable.
2. Select your Minecraft folder or use the **Auto Scan** feature.
3. Add new mod versions using the **Add Version** button.
4. Click a version to activate its mod folder.
5. The manager updates `active_version.txt` automatically to track the currently active version.

> Note: Windows SmartScreen may warn about this executable because it is not digitally signed. This is normal for self-made applications. Click "More info" and then "Run anyway" to use the program.

---

## Folder Structure

- `mods` – The currently active mods folder.
- `mods<version>` – Individual folders for each managed Minecraft version.
- `active_version.txt` – Records the currently active version.

---

## Contributing

Contributions, bug reports, and feature requests are welcome. Please open an issue or submit a pull request.

---

## Author

**itsF4LCON** – Creator of XIV's Mod Manager

---

## License

This project is licensed under the MIT License.
