// api.js - Funciones de API para comunicarse con el backend

import axios from 'axios';
import { API_CONFIG } from './config';

// Configurar instancia de axios con la URL base
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 5000,
});

// Obtener el estado del bot
export const getBotStatus = async () => {
  try {
    const response = await api.get('/status');
    return response.data;
  } catch (error) {
    console.error('Error al obtener el estado del bot:', error);
    throw error;
  }
};

// Obtener estadísticas del bot
export const getBotStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error al obtener las estadísticas del bot:', error);
    throw error;
  }
};

// Obtener lista de comandos desde la API
export const getCommands = async () => {
  try {
    const response = await api.get('/commands');
    return response.data;
  } catch (error) {
    console.error('Error al obtener comandos:', error);
    // Fallback en caso de que la API no esté disponible
    return [
      { name: '!help', description: 'Muestra todos los comandos', category: 'Utilidad' },
      { name: '!ping', description: 'Verifica la latencia del bot', category: 'Utilidad' },
      { name: '!profile', description: 'Tu perfil completo', category: 'Economía' },
      { name: '!balance', description: 'Consulta tu saldo', category: 'Economía' },
      { name: '!work', description: 'Trabaja y gana dinero (3min cd)', category: 'Economía' },
      { name: '!daily', description: 'Recompensa diaria (24h cd)', category: 'Economía' },
      { name: '!shop', description: 'Tienda de items', category: 'Economía' },
      { name: '!buy [item]', description: 'Compra un item', category: 'Economía' },
      { name: '!transfer @user $', description: 'Transferir dinero', category: 'Economía' },
      { name: '!rob @user', description: 'Intenta robar (50%)', category: 'Economía' },
      { name: '!ranking', description: 'Top 5 más ricos', category: 'Economía' },
      { name: '!level', description: 'Ver nivel y XP', category: 'Niveles' },
      { name: '!leaderboard', description: 'Top 10 por XP', category: 'Niveles' },
      { name: '!warn @user', description: 'Advertir usuario', category: 'Moderación' },
      { name: '!mute @user [tiempo]', description: 'Silenciar usuario', category: 'Moderación' },
      { name: '!kick @user', description: 'Expulsar del servidor', category: 'Moderación' },
      { name: '!ban @user', description: 'Banear permanente', category: 'Moderación' },
      { name: '!clear [1-100]', description: 'Elimina mensajes', category: 'Moderación' },
      { name: '!slowmode [seg]', description: 'Modo lento del canal', category: 'Moderación' },
    ];
  }
};

const apiMethods = {
  getBotStatus,
  getBotStats,
  getCommands
};

// Exportar todas las funciones como un objeto
export default apiMethods;