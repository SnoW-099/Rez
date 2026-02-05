// api.js - Funciones de API para comunicarse con el backend

import axios from 'axios';
import { API_CONFIG } from './config';

// Configurar instancia de axios con la URL base
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
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

// Obtener lista de comandos
export const getCommands = async () => {
  // Official command list from commands.py
  return [
    { name: "!profile", description: "Muestra tu perfil de usuario" },
    { name: "!ranking", description: "Muestra el top 5 de usuarios más ricos" },
    { name: "!work", description: "Trabaja para ganar dinero (cooldown: 3 minutos)" },
    { name: "!balance", description: "Consulta tu saldo" },
    { name: "!transfer", description: "Transfiere dinero a otro usuario (@usuario cantidad)" },
    { name: "!rob", description: "Intenta robarle dinero a otro usuario (@usuario)" },
    { name: "!ping", description: "Verifica la latencia del bot" },
    { name: "!warn", description: "Advierte a un usuario (solo admins/mods)" },
    { name: "!clear", description: "Elimina mensajes (solo admins/mods)" }
  ];
};

const apiMethods = {
  getBotStatus,
  getBotStats,
  getCommands
};

// Exportar todas las funciones como un objeto
export default apiMethods;