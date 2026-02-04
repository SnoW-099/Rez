import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import LoadingScreen from './LoadingScreen';
import ParticlesBackground from './ParticlesBackground';
import CustomCursor from './CustomCursor';
import './Layout.css';

const Layout = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fake loading for 3 seconds on initial mount
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="layout-container">
      <CustomCursor />
      {isLoading && <LoadingScreen />}

      {!isLoading && (
        <>
          <ParticlesBackground />
          <div className="animate-fade-in" style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', zIndex: 1 }}>
            <header className="layout-header">
              <Navbar />
            </header>

            <main className="layout-content">
              <div className="content-wrapper">
                {children}
              </div>
            </main>
          </div>
        </>
      )}
    </div>
  );
};

export default Layout;
