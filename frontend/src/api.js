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
    // Fallback con todos los comandos actuales
    return [
      // Utilidad
      { name: '!help', description: 'Muestra todos los comandos', category: 'Utilidad' },
      { name: '!ping', description: 'Verifica la latencia del bot', category: 'Utilidad' },

      // Economía
      { name: '!profile', description: 'Tu perfil completo', category: 'Economía' },
      { name: '!balance', description: 'Consulta tu saldo', category: 'Economía' },
      { name: '!work', description: 'Trabaja y gana $50-200 (3min cd)', category: 'Economía' },
      { name: '!daily', description: 'Recompensa diaria $200-500', category: 'Economía' },
      { name: '!transfer @user $', description: 'Transferir dinero', category: 'Economía' },
      { name: '!rob @user', description: 'Robar (50% éxito)', category: 'Economía' },
      { name: '!ranking', description: 'Top 5 más ricos', category: 'Economía' },
      { name: '!shop', description: 'Tienda de items', category: 'Economía' },
      { name: '!buy [item]', description: 'Compra un item', category: 'Economía' },

      // Niveles
      { name: '!level', description: 'Ver nivel y XP', category: 'Niveles' },
      { name: '!leaderboard', description: 'Top 10 por XP', category: 'Niveles' },

      // Casino
      { name: '!coinflip $ cara/cruz', description: 'Apuesta cara o cruz', category: 'Casino' },
      { name: '!slots $', description: 'Máquina tragamonedas', category: 'Casino' },
      { name: '!blackjack $', description: 'Juega al 21', category: 'Casino' },
      { name: '!roulette $ color/num', description: 'Ruleta de casino', category: 'Casino' },

      // Sorteos
      { name: '!giveaway [tiempo] [premio]', description: 'Crear sorteo', category: 'Sorteos' },
      { name: '!gend', description: 'Terminar sorteo', category: 'Sorteos' },
      { name: '!greroll [id]', description: 'Re-sortear ganador', category: 'Sorteos' },

      // Tickets
      { name: '!ticket [razón]', description: 'Crear ticket de soporte', category: 'Tickets' },
      { name: '!close', description: 'Cerrar ticket actual', category: 'Tickets' },

      // Moderación
      { name: '!warn @user', description: 'Advertir (3 = kick)', category: 'Moderación' },
      { name: '!mute @user [tiempo]', description: 'Silenciar usuario', category: 'Moderación' },
      { name: '!kick @user', description: 'Expulsar del servidor', category: 'Moderación' },
      { name: '!ban @user', description: 'Banear permanente', category: 'Moderación' },
      { name: '!clear [1-100]', description: 'Elimina mensajes', category: 'Moderación' },
      { name: '!slowmode [seg]', description: 'Modo lento', category: 'Moderación' },
    ];
  }
};

const apiMethods = {
  getBotStatus,
  getBotStats,
  getCommands
};

export default apiMethods;