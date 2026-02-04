import React, { useState, useEffect } from 'react';
import api from '../api';

const BankDashboard = () => {
  const [bankData, setBankData] = useState({
    totalUsers: 0,
    totalCoins: 0,
    averageBalance: 0,
    topUsers: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBankData = async () => {
      try {
        const response = await fetch('/api/bank-data');
        const data = await response.json();
        setBankData(data);
      } catch (error) {
        console.error('Error al cargar los datos bancarios:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBankData();
    // Refresh every 10 seconds for live economy updates
    const interval = setInterval(fetchBankData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading-container">Loading Bank System...</div>;
  }

  return (
    <div className="animate-fade-in">
      <div className="glass-card" style={{ marginBottom: '24px', textAlign: 'center' }}>
        <h1 className="text-gradient" style={{ fontSize: '3rem' }}>Global Economy</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Real-time banking statistics from all servers.</p>
      </div>

      <div className="bento-grid">
        <div className="glass-card">
          <span className="tech-icon">💰</span>
          <div className="stat-value">{bankData.totalCoins.toLocaleString()}</div>
          <div className="stat-label">Total Circulating Coins</div>
        </div>

        <div className="glass-card">
          <span className="tech-icon">📈</span>
          <div className="stat-value">{Math.round(bankData.averageBalance).toLocaleString()}</div>
          <div className="stat-label">Average Balance</div>
        </div>

        <div className="glass-card">
          <span className="tech-icon">💳</span>
          <div className="stat-value">{bankData.totalUsers.toLocaleString()}</div>
          <div className="stat-label">Active Accounts</div>
        </div>

        <div className="glass-card" style={{ gridColumn: 'span 2' }}>
          <h2>Richest Users 🏆</h2>
          <div className="rich-list" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {bankData.topUsers.map((user, index) => (
              <div key={user.id} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px',
                background: 'rgba(255,255,255,0.4)',
                borderRadius: '12px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                  <span style={{
                    width: '30px',
                    height: '30px',
                    background: index === 0 ? '#FFD700' : index === 1 ? '#C0C0C0' : index === 2 ? '#CD7F32' : 'var(--text-secondary)',
                    color: 'white',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 'bold'
                  }}>
                    {index + 1}
                  </span>
                  <span style={{ fontWeight: '600' }}>User {user.id.substring(0, 8)}...</span>
                </div>
                <span style={{ fontWeight: '700', color: 'var(--success-color)' }}>
                  {user.balance.toLocaleString()} 🪙
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BankDashboard;