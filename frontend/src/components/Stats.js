import React, { useState, useEffect } from 'react';
import { getBotStats } from '../api';
import { useNotifications } from '../context/Notifications';
import './Stats.css';

const StatsComponent = () => {
  const [stats, setStats] = useState({
    servers: 0,
    users: 0,
    commandsUsed: 0,
    uptime: '0d 0h 0m'
  });
  const { addNotification } = useNotifications();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const statsData = await getBotStats();
        if (!statsData.error) {
          setStats(statsData);
        } else {
          console.error('Error al obtener estadísticas:', statsData.error);
          addNotification('Error al cargar estadísticas', 'error');
        }
      } catch (error) {
        console.error('Error al obtener estadísticas:', error);
        addNotification('Error al cargar estadísticas', 'error');
      }
    };

    // Cargar estadísticas iniciales
    fetchStats();

    // Actualizar estadísticas periódicamente
    const interval = setInterval(fetchStats, 30000); // Cada 30 segundos

    return () => clearInterval(interval);
  }, [addNotification]);

  return (
    <div className="stats-container">
      <h3>Estadísticas del Bot</h3>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.servers}</div>
          <div className="stat-label">Servidores</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.users?.toLocaleString()}</div>
          <div className="stat-label">Usuarios</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.commandsUsed?.toLocaleString()}</div>
          <div className="stat-label">Comandos Usados</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.uptime}</div>
          <div className="stat-label">Tiempo Activo</div>
        </div>
      </div>
    </div>
  );
};

export default StatsComponent;