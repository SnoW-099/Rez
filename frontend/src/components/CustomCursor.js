import React, { useEffect, useState } from 'react';

const CustomCursor = () => {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isHidden, setIsHidden] = useState(false);
    const [isClicking, setIsClicking] = useState(false);
    const [isVisible, setIsVisible] = useState(false); // Only show after first move to avoid 0,0 jump

    useEffect(() => {
        const updatePosition = (e) => {
            setPosition({ x: e.clientX, y: e.clientY });
            if (!isVisible) setIsVisible(true);
        };

        const handleMouseDown = () => setIsClicking(true);
        const handleMouseUp = () => setIsClicking(false);

        const handleMouseEnter = () => setIsHidden(false);
        const handleMouseLeave = () => setIsHidden(true);

        window.addEventListener('mousemove', updatePosition);
        window.addEventListener('mousedown', handleMouseDown);
        window.addEventListener('mouseup', handleMouseUp);
        document.body.addEventListener('mouseenter', handleMouseEnter);
        document.body.addEventListener('mouseleave', handleMouseLeave);

        return () => {
            window.removeEventListener('mousemove', updatePosition);
            window.removeEventListener('mousedown', handleMouseDown);
            window.removeEventListener('mouseup', handleMouseUp);
            document.body.removeEventListener('mouseenter', handleMouseEnter);
            document.body.removeEventListener('mouseleave', handleMouseLeave);
        };
    }, [isVisible]); // depend on isVisible to re-bind if needed (not strictly necessary but safe)

    if (!isVisible) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '10px', /* Slightly larger for visibility */
            height: '10px',
            background: 'white',
            borderRadius: '50%',
            pointerEvents: 'none',
            zIndex: 9999,
            /* Centering logic: translate moves the element to mouse pos, -50% centers the 10px div on that pos */
            transform: `translate3d(${position.x}px, ${position.y}px, 0) translate(-50%, -50%) scale(${isClicking ? 0.8 : 1})`,
            opacity: isHidden ? 0 : 1,
            transition: 'transform 0.05s linear, opacity 0.2s', /* Faster follow, linear for smoothness */
            mixBlendMode: 'difference',
            willChange: 'transform'
        }} />
    );
};

export default CustomCursor;
