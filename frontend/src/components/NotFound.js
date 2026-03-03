import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div style={{
            height: '70vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            fontFamily: '"MSGothic", "Courier New", monospace',
            color: '#ededed',
            padding: '20px'
        }}>
            <div className="glass-card" style={{
                background: 'rgba(0,0,0,0.8)',
                border: '1px solid #27272a',
                padding: '40px',
                width: '100%',
                maxWidth: '500px',
                textAlign: 'left',
                boxShadow: '0 0 40px rgba(0,0,0,0.5)'
            }}>
                <div style={{ marginBottom: '20px', borderBottom: '1px solid #27272a', paddingBottom: '10px', color: '#5865F2', fontWeight: 'bold' }}>
                    [ SYSTEM_ERROR: 404 ]
                </div>
                <div style={{ marginBottom: '10px', color: '#71717a' }}>
                    &gt; REZ_CORE_v1.0.4: RESOURCE_NOT_FOUND
                </div>
                <div style={{ marginBottom: '10px', color: '#71717a' }}>
                    &gt; STACK_TRACE: 0xRE7_Z0_B0T_X99
                </div>
                <div style={{ marginBottom: '30px', opacity: 0.8, lineHeight: '1.6' }}>
                    The entry you are attempting to access does not exist in the current data cluster. It may have been relocated or purged.
                </div>

                <Link to="/" className="secondary-btn" style={{
                    textDecoration: 'none',
                    textAlign: 'center'
                }}>
                    [ REBOOT_SYSTEM ]
                </Link>
            </div>
            <div style={{ marginTop: '24px', fontSize: '0.75rem', color: '#3f3f46' }}>
                SESSION_ID: {Math.random().toString(36).substring(7).toUpperCase()}
            </div>
        </div>
    );
};

export default NotFound;
