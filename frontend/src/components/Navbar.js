import React, { useState, useEffect, useRef } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
  const location = useLocation();
  const [indicatorStyle, setIndicatorStyle] = useState({ left: 0, width: 0, opacity: 0 });
  const navLinksRef = useRef(null);

  useEffect(() => {
    const updateIndicator = () => {
      if (navLinksRef.current) {
        const activeLink = navLinksRef.current.querySelector('.nav-item.active');
        if (activeLink) {
          const { offsetLeft, offsetWidth } = activeLink;
          setIndicatorStyle({
            left: offsetLeft,
            width: offsetWidth,
            opacity: 1
          });
        } else {
          setIndicatorStyle(prev => ({ ...prev, opacity: 0 }));
        }
      }
    };

    // Small timeout to ensure NavLink has updated its active class
    const timer = setTimeout(updateIndicator, 50);
    window.addEventListener('resize', updateIndicator);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', updateIndicator);
    };
  }, [location.pathname]);

  return (
    <nav className="glass-navbar">
      <div className="nav-container">
        <NavLink to="/" className="nav-logo">
          Rez<span className="logo-dot">.</span>
        </NavLink>

        <div className="nav-links" ref={navLinksRef}>
          {/* The Sliding Indicator */}
          <div
            className="nav-sliding-indicator"
            style={{
              left: `${indicatorStyle.left}px`,
              width: `${indicatorStyle.width}px`,
              opacity: indicatorStyle.opacity
            }}
          />

          <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            Start
          </NavLink>
          <NavLink to="/updates" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            Updates
          </NavLink>
        </div>

        <div className="nav-actions" style={{ display: 'flex', gap: '15px', alignItems: 'center', marginLeft: 'auto' }}>
          <a href="https://github.com/SnoW-099/Rezz" target="_blank" rel="noopener noreferrer" className="nav-icon-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
            </svg>
          </a>
          <button className="invite-btn" onClick={() => window.open('https://discord.com/api/oauth2/authorize?client_id=1465120268996444375&permissions=8&scope=bot', '_blank')}>
            Add to Server
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;