# Rez Bot - Frontend Dashboard

This is the frontend component of the Rez Bot, a React-based web application providing a premium "Liquid Black" dashboard for monitoring Discord bot status.

## Installation

1. Ensure Node.js is installed on your system.
2. Install dependencies:
```bash
npm install
```

## Running the App

To start the application in development mode:
```bash
npm start
```

The app will automatically open in your browser at `http://localhost:3000`.

## Configuration

Environment variables can be configured in a `.env` file:

- `REACT_APP_API_URL`: Bot API URL (default: http://localhost:3001/api)
- `REACT_APP_BOT_CLIENT_ID`: Discord Bot Client ID

## Features

- **Liquid Black Aesthetic**: Premium dark mode design with immersive animations.
- **Live Status**: Real-time monitoring of bot online status.
- **Animation System**: 
  - Ripple Loading Screen
  - Sand Dissolve Text
  - 3D Tilt Cards
  - Custom Minimalist Cursor
- **Responsive Design**: Optimized for all devices.