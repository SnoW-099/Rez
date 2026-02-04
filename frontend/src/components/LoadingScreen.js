import React from 'react';
import './LoadingScreen.css';

const LoadingScreen = () => {
    return (
        <div className="loading-screen">
            <div className="loading-content">
                <div className="icon-wrapper">
                    <div className="ripple"></div>
                    <div className="ripple delay"></div>
                    <img src="/images/bot_icon.jpg" alt="Loading..." className="loading-icon" />
                </div>
            </div>
        </div>
    );
};

export default LoadingScreen;
