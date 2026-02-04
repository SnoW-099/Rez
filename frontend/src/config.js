// config.js - Configuración del frontend

export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  BOT_CLIENT_ID: process.env.REACT_APP_BOT_CLIENT_ID || ''
};

export const APP_CONFIG = {
  NAME: 'Rez Bot Dashboard',
  VERSION: '1.0.0',
  THEME: 'apple-style'
};