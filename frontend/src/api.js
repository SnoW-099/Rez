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
    // Fallback con todos los comandos
    return [
      // ========== UTILIDAD ==========
      { name: '!help', description: 'Muestra todos los comandos', category: 'Utilidad', role: 'usuario' },
      { name: '!ping', description: 'Verifica la latencia del bot', category: 'Utilidad', role: 'usuario' },

      // ========== ECONOMÍA ==========
      { name: '!profile [@user]', description: 'Tu perfil completo con stats', category: 'Economía', role: 'usuario' },
      { name: '!balance [@user]', description: 'Consulta tu saldo', category: 'Economía', role: 'usuario' },
      { name: '!work', description: 'Trabaja y gana $50-200 (3min cd)', category: 'Economía', role: 'usuario' },
      { name: '!daily', description: 'Recompensa diaria $200-500 (24h cd)', category: 'Economía', role: 'usuario' },
      { name: '!transfer @user $', description: 'Transferir dinero a otro usuario', category: 'Economía', role: 'usuario' },
      { name: '!rob @user', description: 'Intenta robar (50% éxito)', category: 'Economía', role: 'usuario' },
      { name: '!ranking', description: 'Top 5 usuarios más ricos', category: 'Economía', role: 'usuario' },
      { name: '!shop', description: 'Ver tienda de items', category: 'Economía', role: 'usuario' },
      { name: '!buy [item]', description: 'Compra un item de la tienda', category: 'Economía', role: 'usuario' },

      // ========== NIVELES ==========
      { name: '!level [@user]', description: 'Ver nivel y XP actual', category: 'Niveles', role: 'usuario' },
      { name: '!leaderboard', description: 'Top 10 por XP', category: 'Niveles', role: 'usuario' },

      // ========== CASINO ==========
      { name: '!coinflip $ cara/cruz', description: 'Apuesta cara o cruz (x2)', category: 'Casino', role: 'usuario' },
      { name: '!slots $', description: 'Máquina tragamonedas', category: 'Casino', role: 'usuario' },
      { name: '!blackjack $', description: 'Juega al 21 (!hit/!stand)', category: 'Casino', role: 'usuario' },
      { name: '!roulette $ color/num', description: 'Ruleta (red/black/green/0-36)', category: 'Casino', role: 'usuario' },
      { name: '!hit', description: 'Pide carta en Blackjack', category: 'Casino', role: 'usuario' },
      { name: '!stand', description: 'Plantarte en Blackjack', category: 'Casino', role: 'usuario' },

      // ========== SORTEOS ==========
      { name: '!giveaway [tiempo] [premio]', description: 'Crear sorteo (ej: 1h iPhone)', category: 'Sorteos', role: 'admin' },
      { name: '!gend [id]', description: 'Terminar sorteo manualmente', category: 'Sorteos', role: 'admin' },
      { name: '!greroll [id]', description: 'Volver a sortear ganador', category: 'Sorteos', role: 'admin' },

      // ========== TICKETS ==========
      { name: '!ticket [razón]', description: 'Crear ticket de soporte', category: 'Tickets', role: 'usuario' },
      { name: '!close', description: 'Cerrar ticket actual', category: 'Tickets', role: 'usuario' },
      { name: '!adduser @user', description: 'Añadir usuario al ticket', category: 'Tickets', role: 'admin' },
      { name: '!removeuser @user', description: 'Quitar usuario del ticket', category: 'Tickets', role: 'admin' },

      // ========== MODERACIÓN ==========
      { name: '!warn @user [razón]', description: 'Advertir usuario (3 warns = kick)', category: 'Moderación', role: 'admin' },
      { name: '!mute @user [tiempo]', description: 'Silenciar (ej: 10m, 1h, 1d)', category: 'Moderación', role: 'admin' },
      { name: '!unmute @user', description: 'Quitar silencio a usuario', category: 'Moderación', role: 'admin' },
      { name: '!kick @user [razón]', description: 'Expulsar del servidor', category: 'Moderación', role: 'admin' },
      { name: '!ban @user [razón]', description: 'Banear permanentemente', category: 'Moderación', role: 'admin' },
      { name: '!unban [id]', description: 'Desbanear por ID de usuario', category: 'Moderación', role: 'admin' },
      { name: '!clear [1-100]', description: 'Elimina mensajes del canal', category: 'Moderación', role: 'admin' },
      { name: '!slowmode [segundos]', description: 'Modo lento del canal (0 = off)', category: 'Moderación', role: 'admin' },
      { name: '!reset_warnings @user', description: 'Reiniciar warns de usuario', category: 'Moderación', role: 'admin' },

      // ========== OWNER ==========
      { name: '!addmoney @user $', description: 'Dar dinero a usuario', category: 'Owner', role: 'owner' },
      { name: '!removemoney @user $', description: 'Quitar dinero a usuario', category: 'Owner', role: 'owner' },
      { name: '!setbalance @user $', description: 'Establecer balance exacto', category: 'Owner', role: 'owner' },
      { name: '!setlevel @user nivel', description: 'Establecer nivel de usuario', category: 'Owner', role: 'owner' },
      { name: '!resetuser @user', description: 'Reiniciar todos los datos', category: 'Owner', role: 'owner' },
      { name: '!botstat', description: 'Estadísticas detalladas del bot', category: 'Owner', role: 'owner' },

      // ========== MÚSICA ==========
      { name: '!play [canción]', description: 'Reproduce música', category: 'Música', role: 'usuario' },
      { name: '!join', description: 'Entra al canal de voz', category: 'Música', role: 'usuario' },
      { name: '!leave', description: 'Sale del canal de voz', category: 'Música', role: 'usuario' },
    ];
  }
};

const apiMethods = {
  getBotStatus,
  getBotStats,
  getCommands
};

export default apiMethods;