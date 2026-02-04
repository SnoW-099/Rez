# Rez 🤖 | Security & Economy System

Rez is a high-performance Discord bot designed to balance community management with a competitive economic framework. Built for **reliability, efficiency, and security**.

> 🛡️ **Project Status**: Active Beta. Rez now features full data persistence and independent administrative modules.

## 🛠️ Project Architecture

The bot utilizes a modular structure to ensure stability and maintainability:

* `main.py`: Core execution and module orchestrator.
* `config.py`: Intents management and API configuration (Prefix: `!`).
* `moderation.py`: Security system, filters, and user control.
* `commands.py`: Economic logic and server utilities.
* `bank_system.py`: JSON database engine and data persistence.

## ✨ Core Features

### 🛡️ Security Module
* **Warning System**: Persistent tracking of user infractions with automatic kick-action after 3 warnings.
* **Invite Anti-Spam**: Intelligent filter that blocks external server links (Administrator bypass included).
* **Log Maintenance**: High-speed commands for channel cleanup and moderation.

### 💰 Economic System
* **Full Persistence**: Balances and records are saved in real-time to prevent data loss.
* **Social Interaction**: Transfer commands (donate), risk-reward mechanics (work/rob), and social engagement.
* **Global Ranking**: High-fidelity Embeds displaying the most influential users in the server.

## 📜 Command List

| Command | Category | Description |
| :--- | :--- | :--- |
| `!profile` | Utility | Displays user technical file, balance, and security history. |
| `!ranking` | Economy | Displays Top 5 users with the highest liquidity. |
| `!warn` | Security | Issues a formal warning to a user (Admin only). |
| `!clear` | Moderation | Bulk message deletion for channel maintenance. |
| `!work` | Economy | Generates random income (3-minute cooldown). |

## 🌐 Deployment & Testing

1. Clone the repository.
2. Create a `.env` file containing your `DISCORD_TOKEN`.
3. Install dependencies: `pip install discord.py python-dotenv`.
4. Run `main.py` to initialize the system.

---
Developed with 💻 by **Snow099** ⭐
