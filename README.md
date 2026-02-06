# ⚙️ Rez | Backend Engine
**The core infrastructure powering the Rez ecosystem.**

This repository contains the logic, database management, and API bridge that sustain the security and economy modules of Rez.

---

## 🏗️ System Architecture
The backend is divided into two main components:
1. **The Bot (Discord Core):** Handles events, commands, and real-time interaction using `discord.py` / `disnake`.
2. **The API Bridge (Flask):** A lightweight REST API that serves data to the Frontend dashboard.



## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Framework:** Flask (API)
* **Library:** Discord.py / Disnake (Bot)
* **Database:** Supabase / MongoDB (Persistence)
* **Process Manager:** PM2 / Docker

## 📡 API Endpoints (Flask)
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/status` | `GET` | Returns system health and latency. |
| `/api/v1/stats` | `GET` | Fetches global server and user counts. |
| `/api/v1/user/<id>`| `GET` | Returns specific economy and security data for a user. |

## 🛡️ Security & Performance
* **Asynchronous Execution:** Built with `asyncio` to handle multiple requests without blocking.
* **CORS Enabled:** Configured for secure communication with the Netlify frontend.
* **Environment Variables:** Critical tokens and DB strings are managed via `.env` files.

## 🚀 Installation & Setup
1. **Clone the backend:**
   ```bash
   git clone [https://github.com/SnoW-099/Rez-Backend](https://github.com/SnoW-099/Rez-Backend)
