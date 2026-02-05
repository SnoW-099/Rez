import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import ProgressiveImage from './ProgressiveImage';
import { useToast } from '../context/ToastContext';
import updates from '../data/UpdatesData';
import TiltCard from './TiltCard';

const DashboardHome = () => {
    const [stats, setStats] = useState(null);
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const { addToast } = useToast();

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                // Add slight delay for premium feel / shimmer visibility
                await new Promise(resolve => setTimeout(resolve, 800));
                const [statsData, statusData] = await Promise.all([
                    api.getBotStats(),
                    api.getBotStatus()
                ]);
                setStats(statsData);
                setStatus(statusData);
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
                addToast('Failed to load dashboard data.', 'error');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [addToast]);

    return (
        <div className="animate-fade-in">
            {/* Header / Profile Section - Tilt Effect */}
            <div className={`glass-card ${loading ? 'shimmer-sweep' : ''}`} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '20px',
                marginBottom: '16px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <ProgressiveImage
                    src="/images/bot_icon.jpg"
                    placeholder="rgba(255,255,255,0.05)"
                    alt="Rez Bot avatar"
                    style={{
                        width: '100px',
                        height: '100px',
                        borderRadius: '20px',
                        backgroundColor: '#18181b'
                    }}
                />
                <div>
                    <h1 className="sand-text" style={{ fontSize: '2rem', display: 'flex', alignItems: 'center', gap: '10px', margin: 0, fontWeight: '700' }}>
                        Rez
                        <span style={{
                            background: 'var(--accent-color)',
                            fontSize: '0.7rem',
                            fontWeight: 'bold',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            color: 'white',
                            textTransform: 'uppercase'
                        }}>APP</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0', fontSize: '1rem', fontWeight: '500' }}>Rez#1996</p>
                </div>
            </div>

            {/* Actions */}
            <div style={{ marginBottom: '24px' }}>
                <Link to="/commands" className="secondary-btn">
                    View Commands
                </Link>
            </div>

            <div className="bento-grid">
                {/* Status/Stats - Tilt Effect */}
                <TiltCard className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div>
                            <h3 style={{ marginBottom: '5px', fontSize: '0.9rem', color: 'var(--text-primary)' }}>Status</h3>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                <div className="status-dot-pulse" style={{
                                    width: '8px',
                                    height: '8px',
                                    borderRadius: '50%',
                                    background: status?.status === 'online' ? '#23a559' : '#ed4245'
                                }}></div>
                                {status?.status === 'online' ? 'Operational' : 'Maintenance'}
                            </div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                            <h3 style={{ marginBottom: '5px', fontSize: '0.9rem', color: 'var(--text-primary)' }}>Servers</h3>
                            <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                {loading ? '...' : (stats?.servers || 0)}
                            </div>
                        </div>
                    </div>
                </TiltCard>

                {/* News Feed - Tilt Effect */}
                <TiltCard className="glass-card">
                    <h3 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>Latest Updates</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                        {updates.slice(0, 3).map(update => (
                            <div key={update.id} style={{
                                borderLeft: '2px solid #27272a',
                                paddingLeft: '16px'
                            }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>{update.date}</div>
                                <div style={{ fontWeight: '600', marginBottom: '4px', color: 'var(--text-primary)' }}>{update.title}</div>
                                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>{update.description}</div>
                            </div>
                        ))}
                    </div>
                </TiltCard>
            </div>
        </div>
    );
};

export default DashboardHome;
