📦 Minecraft Auto-Backuper

<p align="center"> <img src="./assets/MinecraftIcon.png" width="120px" alt="Minecraft Auto-Backuper Icon"/> </p>

<p align="center"> <em> A robust, autonomous Python solution for compressing Minecraft worlds, uploading them to Google Drive, and receiving detailed status reports via email. </em> </p>

<p align="center"> <img src="https://img.shields.io/badge/License-MIT-E92063?style=flat-square&logo=opensourceinitiative&logoColor=white"/> <img src="https://img.shields.io/badge/Python-3.x-E92063?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/🛠_Status-Operational-E92063?style=flat-square"/> </p>

<p align="center"><em>Built with:</em></p> <p align="center"> <img src="https://img.shields.io/badge/Compression-WinRAR-E92063?style=flat-square&logo=winrar&logoColor=white"/> <img src="https://img.shields.io/badge/Cloud-Google_Drive-E92063?style=flat-square&logo=googledrive&logoColor=white"/> <img src="https://img.shields.io/badge/Logging-Python_Logging-E92063?style=flat-square&logo=python&logoColor=white"/> </p>

<details><summary><b>📋 Table of Contents</b></summary>

    🧭 Overview

        Why "Minecraft Auto-Backuper"?

    ⚙️ Features

    📁 Project Structure

    🧩 Get Started

        🛠️ Local Installation

    🧠 Usage

    👤 Author

    📜 License

</details>

<a id="overview"></a>
🧭 Overview

Minecraft Auto-Backuper is a meta-language scripted tool designed to protect your large-scale Minecraft projects. It automates the entire cycle of data safety: identifying world folders, compressing them using solid WinRAR algorithms, mirroring the data to the cloud, and informing the user via email.

<a id="why-project"></a>
ㅤ---

<details><summary><b>Why "Minecraft Auto-Backuper"?</b></summary>

For technical players, losing a world is losing months of work. This project exists to:

    Minimize Storage Impact: Uses WinRAR solid compression (-s) to reduce file size.

    Automate Cloud Redundancy: Integrates with Google Drive API v3 to replace old backups with fresh ones.

    Provide Peace of Mind: You don't need to check if it worked; the script sends the log directly to your email inbox.

    Local Hygiene: Automatically cleans up temporary .zip files and old logs to save disk space.

</details>

<a id="features"></a>
⚙️ Features
	Category	Description
🗜️	Solid Compression	Uses WinRAR CLI for high-ratio, background-mode compression.
☁️	Cloud Integration	OAuth2 authentication with Google Drive for secure file replacement.
📧	Email Reporting	Automatic SMTP delivery of the execution log after completion.
📝	Smart Logging	Dual-handler logging (Terminal + UTF-8 File) with automatic cleanup.
🧹	Self-Cleaning	Deletes local temporary backups after successful cloud upload.

<a id="project-structure"></a>
📁 Project Structure
Bash

Minecraft-Backuper/
├── logs/                # Stores generated UTF-8 execution logs
├── Backups/        # Temporary directory for .zip creation (cleaned after upload)
├── backuper.py          # Core orchestrator and main logic
├── Backuper_cloud.py    # Google Drive API v3 integration
├── Email_sender.py      # SMTP configuration and email delivery logic
├── .env                 # Environment variables (Credentials & Paths)
└── requirements.txt     # Python dependencies

<a id="get-started"></a>
🧩 Get Started

<a id="installation"></a>
🛠️ Local Installation

    Clone the repository
    Bash

    git clone https://github.com/SEU_USER/minecraft-backuper.git
    cd minecraft-backuper

    Install Dependencies
    Bash

    pip install -r requirements.txt

    Configure Environment (.env) Create a .env file and fill in your details:
    Code Snippet

    CAMINHO_SAVES_MINECRAFT=C:/Users/YourUser/AppData/Roaming/.minecraft/saves
    WINRAR_PATH=C:/Program Files/WinRAR/WinRAR.exe
    CAMINHO_DESTINO_BACKUP=./temp_backups
    EMAIL_REMETENTE=your-email@gmail.com
    EMAIL_DESTINATARIO=target-email@gmail.com
    EMAIL_SENHA=your-app-password
    CAMINHO_CREDENTIALS=credentials.json

<a id="usage"></a>
🧠 Usage

Simply run the main script. The process is fully autonomous:
Bash

python backuper.py

    Step 1: The script authenticates with Drive and locates your Minecraft saves.

    Step 2: Each world is compressed into a .zip in background mode.

    Step 3: Files are uploaded to the "Backups_Minecraft_Vanilla" folder on Drive.

    Step 4: Local temporary backups are deleted.

    Step 5: The most recent log is sent via email and old logs are purged.

<a id="author"></a>
👤 Author

Developed with ❤️ by Artur (Turzimm). If this project helped you protect your worlds, consider giving it a ⭐!

 * **Artur** - *Lead Developer* 📎 [GitHub Profile](https://github.com/TurzimmGit) | [LinkedIn](https://linkedin.com/in/artur-ferreira-sales-26a927370/)

<a id="license"></a>
📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

<p align="left"> <a href="#top"> <img src="https://img.shields.io/badge/Back_to_Top_⭱-E92063?style=flat&logoColor=white" /> </a> </p>
