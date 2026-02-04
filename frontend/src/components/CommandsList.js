import React, { useState, useEffect } from 'react';
import api from '../api';

const CommandsList = () => {
    const [commands, setCommands] = useState([]);
    // Removed specific loading state UI for faster perceived load
    // const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchCommands = async () => {
            try {
                const data = await api.getCommands();
                setCommands(data);
            } catch (error) {
                console.error("Failed to fetch commands", error);
            }
        };

        fetchCommands();
    }, []);

    const filteredCommands = commands.filter(cmd =>
        cmd.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cmd.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="animate-fade-in">
            <div className="glass-card" style={{ marginBottom: '24px' }}>
                <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Commands</h1>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
                    Browse all available commands for Rez Bot.
                </p>
                <input
                    type="text"
                    placeholder="Search commands..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{
                        width: '100%',
                        padding: '16px',
                        borderRadius: '16px',
                        border: '1px solid rgba(0,0,0,0.1)',
                        background: 'rgba(255,255,255,0.05)', /* Darker input */
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
                {filteredCommands.map((cmd, index) => (
                    <div key={index} className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                        <code style={{
                            background: 'rgba(88, 101, 242, 0.2)', /* Blurple tint */
                            color: '#5865F2',
                            padding: '6px 12px',
                            borderRadius: '8px',
                            alignSelf: 'flex-start',
                            fontWeight: 'bold',
                            marginBottom: '10px',
                            border: '1px solid rgba(88, 101, 242, 0.3)'
                        }}>
                            {cmd.name}
                        </code>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                            {cmd.description}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CommandsList;
