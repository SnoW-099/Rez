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
  try {
    const response = await api.get('/commands');
    return response.data;
  } catch (error) {
    console.error('Error al obtener los comandos:', error);
    throw error;
  }
};

// Exportar todas las funciones como un objeto
export default {
  getBotStatus,
  getBotStats,
  getCommands
};