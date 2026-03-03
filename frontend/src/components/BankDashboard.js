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
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchBankData = async () => {
      try {
        setError(false);
        const data = await api.getBankData();
        setBankData(data);
      } catch (err) {
        console.error('Error loading bank data:', err);
        setError(true);
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
    return (
      <div className="animate-fade-in">
        <div className="glass-card shimmer-sweep skeleton-card" style={{ height: '120px', marginBottom: '24px' }} />
        <div className="bento-grid">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="glass-card skeleton-card shimmer-sweep" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="animate-fade-in">
        <div className="glass-card" style={{ textAlign: 'center', padding: '60px 24px' }}>
          <div style={{ fontSize: '3rem', marginBottom: '16px' }}>⚠️</div>
          <h2 style={{ color: 'var(--text-primary)', marginBottom: '8px' }}>Bot Offline</h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            Could not connect to the API. Make sure the bot is running.
          </p>
        </div>
      </div>
    );
  }

  const medals = ['🥇', '🥈', '🥉'];

  return (
    <div className="animate-fade-in">
      <div className="glass-card" style={{ marginBottom: '24px', textAlign: 'center' }}>
        <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '8px' }}>Global Economy</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Real-time banking statistics from all servers.</p>
      </div>

      <div className="bento-grid">
        <div className="glass-card">
          <div style={{ fontSize: '2rem', marginBottom: '8px' }}>💰</div>
          <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)' }}>
            {bankData.totalCoins.toLocaleString()}
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '4px' }}>
            Total Circulating Coins
          </div>
        </div>

        <div className="glass-card">
          <div style={{ fontSize: '2rem', marginBottom: '8px' }}>📊</div>
          <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)' }}>
            {Math.round(bankData.averageBalance).toLocaleString()}
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '4px' }}>
            Average Balance
          </div>
        </div>

        <div className="glass-card">
          <div style={{ fontSize: '2rem', marginBottom: '8px' }}>👥</div>
          <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)' }}>
            {bankData.totalUsers.toLocaleString()}
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '4px' }}>
            Active Accounts
          </div>
        </div>

        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: 'var(--text-primary)' }}>
            🏆 Richest Users
          </h2>
          {bankData.topUsers.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '20px 0' }}>
              No data available yet.
            </p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {bankData.topUsers.map((user, index) => (
                <div key={user.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  borderRadius: '12px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '1.3rem' }}>
                      {medals[index] || `#${index + 1}`}
                    </span>
                    <span style={{ fontWeight: '600', color: 'var(--text-primary)', fontSize: '0.9rem' }}>
                      User {user.id.toString().substring(0, 8)}...
                    </span>
                  </div>
                  <span style={{
                    fontWeight: '700',
                    color: '#10b981',
                    fontSize: '0.95rem'
                  }}>
                    ${user.balance.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BankDashboard;