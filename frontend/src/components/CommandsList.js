import React, { useState, useEffect } from 'react';
import api from '../api';
import { useToast } from '../context/ToastContext';

const CommandsList = () => {
    const [commands, setCommands] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterRole, setFilterRole] = useState('all');
    const { addToast } = useToast();

    useEffect(() => {
        const fetchCommands = async () => {
            try {
                await new Promise(resolve => setTimeout(resolve, 800));
                const data = await api.getCommands();
                setCommands(data);
            } catch (error) {
                console.error("Failed to fetch commands", error);
            } finally {
                setLoading(false);
            }
        };

        fetchCommands();
    }, []);

    const filteredCommands = commands.filter(cmd => {
        const matchesSearch = cmd.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            cmd.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (cmd.category && cmd.category.toLowerCase().includes(searchTerm.toLowerCase()));

        const matchesRole = filterRole === 'all' || cmd.role === filterRole;

        return matchesSearch && matchesRole;
    });

    const getRoleBadge = (role) => {
        switch (role) {
            case 'admin':
                return { text: '🛡️ Admin', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.15)' };
            case 'owner':
                return { text: '👑 Owner', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' };
            default:
                return { text: '👤 Usuario', color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' };
        }
    };

    const getCategoryColor = (category) => {
        const colors = {
            'Economy': '#10b981',
            'Casino': '#f59e0b',
            'Moderation': '#ef4444',
            'Owner': '#f59e0b',
            'Levels': '#8b5cf6',
            'Giveaways': '#ec4899',
            'Tickets': '#06b6d4',
            'Music': '#3b82f6',
            'Utility': '#6b7280'
        };
        return colors[category] || '#5865F2';
    };

    return (
        <div className="animate-fade-in">
            <div className="glass-card" style={{ marginBottom: '24px' }}>
                <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Commands</h1>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
                    {commands.length} comandos disponibles. Click para copiar.
                </p>

                {/* Filtros */}
                <div style={{ display: 'flex', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
                    {['all', 'user', 'admin', 'owner'].map((role) => (
                        <button
                            key={role}
                            onClick={() => setFilterRole(role)}
                            style={{
                                padding: '8px 16px',
                                borderRadius: '20px',
                                border: filterRole === role ? '2px solid #5865F2' : '1px solid rgba(255,255,255,0.1)',
                                background: filterRole === role ? 'rgba(88, 101, 242, 0.2)' : 'rgba(255,255,255,0.05)',
                                color: filterRole === role ? '#5865F2' : 'var(--text-secondary)',
                                fontSize: '0.85rem',
                                fontWeight: '500',
                                cursor: 'pointer',
                                transition: 'all 0.2s'
                            }}
                        >
                            {role === 'all' ? '🔍 All' :
                                role === 'user' ? '👍 User' :
                                    role === 'admin' ? '🛡️ Admin' : '👑 Owner'}
                        </button>
                    ))}
                </div>

                <input
                    type="text"
                    placeholder="Buscar comandos..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{
                        width: '100%',
                        padding: '16px',
                        borderRadius: '16px',
                        border: '1px solid rgba(255,255,255,0.1)',
                        background: 'rgba(255,255,255,0.05)',
                        color: 'white',
                        fontSize: '1rem',
                        outline: 'none',
                        transition: 'all 0.2s'
                    }}
                    onFocus={(e) => e.target.style.background = 'rgba(255,255,255,0.1)'}
                    onBlur={(e) => e.target.style.background = 'rgba(255,255,255,0.05)'}
                />
            </div>

            <div className="bento-grid">
                {loading ? (
                    [1, 2, 3, 4].map(i => (
                        <div key={i} className="glass-card skeleton-card shimmer-sweep" />
                    ))
                ) : filteredCommands.map((cmd, index) => {
                    const roleBadge = getRoleBadge(cmd.role);
                    const categoryColor = getCategoryColor(cmd.category);

                    return (
                        <div
                            key={index}
                            className="glass-card"
                            style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}
                            onClick={() => {
                                navigator.clipboard.writeText(cmd.name.split(' ')[0]);
                                addToast(`Copiado: ${cmd.name.split(' ')[0]}`);
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
                                <code style={{
                                    background: 'rgba(88, 101, 242, 0.2)',
                                    color: '#5865F2',
                                    padding: '6px 12px',
                                    borderRadius: '8px',
                                    fontWeight: 'bold',
                                    border: '1px solid rgba(88, 101, 242, 0.3)',
                                    fontSize: '0.9rem'
                                }}>
                                    {cmd.name}
                                </code>
                                <span style={{
                                    background: roleBadge.bg,
                                    color: roleBadge.color,
                                    padding: '4px 10px',
                                    borderRadius: '12px',
                                    fontSize: '0.75rem',
                                    fontWeight: '600',
                                    border: `1px solid ${roleBadge.color}30`
                                }}>
                                    {roleBadge.text}
                                </span>
                            </div>

                            <p style={{ color: 'var(--text-secondary)', lineHeight: '1.5', margin: 0 }}>
                                {cmd.description}
                            </p>

                            {cmd.category && (
                                <span style={{
                                    color: categoryColor,
                                    fontSize: '0.75rem',
                                    fontWeight: '500',
                                    opacity: 0.8
                                }}>
                                    {cmd.category}
                                </span>
                            )}
                        </div>
                    );
                })}
            </div>

            {!loading && filteredCommands.length === 0 && (
                <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
                    <p style={{ color: 'var(--text-secondary)' }}>No se encontraron comandos</p>
                </div>
            )}
        </div>
    );
};

export default CommandsList;
