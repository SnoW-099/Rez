import React from 'react';
import updates from '../data/UpdatesData';
import TiltCard from './TiltCard';

const UpdatesPage = () => {
    return (
        <div className="animate-fade-in" style={{ maxWidth: '600px', margin: '0 auto' }}>
            {/* Header wrapped in TiltCard for consistency */}
            <TiltCard
                className="glass-card"
                style={{
                    marginBottom: '24px',
                    background: 'transparent',
                    border: 'none',
                    padding: '0'
                }}
            >
                <h1 style={{ fontSize: '2rem', marginBottom: '10px', color: 'white' }}>History of Changes</h1>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Track all the latest updates and improvements to Rez Bot.
                </p>
            </TiltCard>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {updates.map(update => (
                    <TiltCard key={update.id} className="glass-card" style={{
                        background: '#0a0a0a',
                        border: '1px solid #202020',
                        position: 'relative',
                        paddingLeft: '24px'
                    }}>
                        <div style={{
                            position: 'absolute',
                            left: '0',
                            top: '24px',
                            bottom: '24px',
                            width: '4px',
                            background: update.color || '#5865F2',
                            borderTopRightRadius: '4px',
                            borderBottomRightRadius: '4px'
                        }}></div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                            <span style={{
                                background: 'rgba(255, 255, 255, 0.05)',
                                color: update.color || '#fff',
                                padding: '4px 10px',
                                borderRadius: '100px',
                                fontSize: '0.75rem',
                                fontWeight: '600',
                                border: `1px solid ${update.color}40` /* Semi-transparent border match */
                            }}>
                                {update.tag}
                            </span>
                            <span style={{ color: '#949BA4', fontSize: '0.85rem' }}>{update.date}</span>
                        </div>

                        <h3 style={{ fontSize: '1.2rem', margin: '0 0 8px 0', color: '#f2f3f5' }}>{update.title}</h3>
                        <p style={{ margin: 0, fontSize: '0.95rem', color: '#b5bac1', lineHeight: '1.5' }}>
                            {update.description}
                        </p>
                    </TiltCard>
                ))}
            </div>
        </div>
    );
};

export default UpdatesPage;
