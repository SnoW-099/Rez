import React, { useState, useEffect } from 'react';

const ProgressiveImage = ({ src, placeholder, alt, className, style }) => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [currentSrc, setCurrentSrc] = useState(null);

    useEffect(() => {
        const img = new Image();
        img.src = src;
        img.onload = () => {
            setCurrentSrc(src);
            setIsLoaded(true);
        };
    }, [src]);

    return (
        <div style={{
            ...style,
            backgroundColor: isLoaded ? 'transparent' : (placeholder || 'rgba(255,255,255,0.05)'),
            overflow: 'hidden',
            position: 'relative'
        }} className={className}>
            {currentSrc && (
                <img
                    src={currentSrc}
                    alt={alt}
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                        filter: isLoaded ? 'none' : 'blur(10px)',
                        transition: 'filter 0.5s ease-out, opacity 0.5s ease-out',
                        opacity: isLoaded ? 1 : 0
                    }}
                />
            )}
        </div>
    );
};

export default ProgressiveImage;
