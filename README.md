# Rez Bot - Liquid Black Edition 🖤

Rez is a next-generation Discord bot featuring a premium "God Tier" web interface with a 'Liquid Black' aesthetic. Built for performance, style, and seamless user experience.

![Rez Bot](frontend/public/images/bot_icon.jpg)

## ✨ Features

### 🎨 Web Interface (Frontend)
- **Liquid Black Aesthetic**: Pure black design with deep grey accents (`#09090b`) and `blurple` highlights.
- **Immersive Animations**:
  - **Ripple Loading**: Cinematic 3s intro.
  - **Sand Dissolve**: Physics-based text revelation.
  - **3D Tilt Cards**: Interactive depth effects on mouse hover.
  - **Starfield Background**: Subtle particle system.
  - **Liquid Navbar**: Sliding indicator with gooey animation.
- **Tech Stack**: React 18, React Router v6, CSS animations.

### ⚙️ Backend (API & Bot)
- **Live Status Monitoring**: Real-time bot status and stats.
- **REST API**: Built with Flask (Python).
- **MongoDB Integration**: Persistent data storage in the cloud.
- **Modular Architecture**: Cogs for commands, moderation, levels, and music.

### 💰 Economy System
| Command | Description |
|---------|-------------|
| `!profile` | View your complete profile |
| `!balance` | Check your balance |
| `!work` | Work to earn money (3 min cooldown) |
| `!daily` | Collect daily reward (24h cooldown) |
| `!transfer @user amount` | Transfer money |
| `!rob @user` | Attempt robbery (50% success) |
| `!ranking` | Top 5 richest users |

### ⭐ Level System
| Command | Description |
|---------|-------------|
| `!level` | View your level and XP |
| `!leaderboard` | Top 10 by XP |

- Earn 15-25 XP per message (60s cooldown)
- Level up bonus: Level × $50

### 🛡️ Moderation
| Command | Description |
|---------|-------------|
| `!warn @user` | Warn user (3 warns = kick) |
| `!mute @user [time]` | Timeout (e.g., `10m`, `1h`) |
| `!unmute @user` | Remove timeout |
| `!kick @user` | Kick from server |
| `!ban @user` | Ban from server |
| `!unban [user_id]` | Unban by ID |
| `!clear [amount]` | Delete messages (1-100) |
| `!slowmode [seconds]` | Set channel slowmode |

---

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB Atlas account (free tier)

### 1. Clone the Repository
```bash
git clone https://github.com/SnoW-099/Rez.git
cd Rez
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file with:
```env
DISCORD_TOKEN=your_discord_bot_token
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/
PREFIX=!
WEB_SERVER_PORT=3001
```

Start the bot:
```bash
python main.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Quick Start (Windows)
Double-click `start_app.bat` to launch both backend and frontend.

---

## 🌍 Deployment

### Deploy Frontend to Netlify
1. New Site → Import from Git
2. **Build Command**: `npm run build`
3. **Publish Directory**: `frontend/build`
4. **Base Directory**: `frontend`

### Deploy Backend
For production, consider:
- **Railway** or **Render** for the Python bot
- **MongoDB Atlas** for database (already configured)

---

## 📁 Project Structure
```
Rez/
├── backend/
│   ├── main.py           # Bot entry point
│   ├── api_server.py     # Flask API
│   ├── database.py       # MongoDB connection
│   ├── bank_system.py    # Economy & XP logic
│   ├── commands.py       # Economy commands
│   ├── moderation.py     # Mod commands
│   ├── levels.py         # XP system
│   └── music.py          # Voice commands
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── context/      # Toast notifications
│   │   └── App.js        # Main app
│   └── public/
└── start_app.bat         # Windows launcher
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, CSS3, React Router |
| Backend | Python 3.8+, discord.py 2.x |
| API | Flask, Flask-CORS |
| Database | MongoDB Atlas |
| Deployment | Netlify (frontend), Railway (backend) |

---

## 🤝 Contributing
Built by **SnoW-099**. All rights reserved.

---

## 📜 License
This project is proprietary. Contact the author for licensing inquiries.