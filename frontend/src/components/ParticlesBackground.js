import React, { useEffect, useRef } from 'react';

const ParticlesBackground = () => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationFrameId;
        const mouse = { x: null, y: null, radius: 100 }; // Smaller radius for subtlety

        // Configuration
        const particleCount = 150; // More stars
        const particles = [];

        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        const handleMouseMove = (event) => {
            mouse.x = event.clientX;
            mouse.y = event.clientY;
        };

        window.addEventListener('resize', resizeCanvas);
        window.addEventListener('mousemove', handleMouseMove);
        resizeCanvas();

        // Particle Class - Now "Stars"
        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 1.7 + 0.8; // Slightly larger stars
                this.baseX = this.x;
                this.baseY = this.y;
                this.vx = (Math.random() - 0.5) * 0.2; // Very slow drift
                this.vy = (Math.random() - 0.5) * 0.2;
                this.density = (Math.random() * 30) + 1;
            }

            draw() {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'; // Brighter stars
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
            }

            update() {
                // Background Drift
                this.baseX += this.vx;
                this.baseY += this.vy;

                // Wrap around screen with seamless position adjustment
                if (this.baseX < 0) {
                    this.baseX = canvas.width;
                    this.x += canvas.width;
                }
                if (this.baseX > canvas.width) {
                    this.baseX = 0;
                    this.x -= canvas.width;
                }
                if (this.baseY < 0) {
                    this.baseY = canvas.height;
                    this.y += canvas.height;
                }
                if (this.baseY > canvas.height) {
                    this.baseY = 0;
                    this.y -= canvas.height;
                }

                // Magnetic Attraction Logic
                if (mouse.x != null && mouse.y != null) {
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    let maxDistance = mouse.radius;
                    let force = (maxDistance - distance) / maxDistance;
                    let directionX = forceDirectionX * force * this.density;
                    let directionY = forceDirectionY * force * this.density;

                    if (distance < mouse.radius) {
                        this.x += directionX * 0.05; // Even more subtle attraction
                        this.y += directionY * 0.05;
                    } else {
                        // Return to base position drift
                        if (this.x !== this.baseX) {
                            let dx = this.x - this.baseX;
                            this.x -= dx / 20;
                        }
                        if (this.y !== this.baseY) {
                            let dy = this.y - this.baseY;
                            this.y -= dy / 20;
                        }
                    }
                } else {
                    this.x = this.baseX;
                    this.y = this.baseY;
                }
            }
        }

        const init = () => {
            for (let i = 0; i < particleCount; i++) {
                particles.push(new Particle());
            }
        };

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });
            animationFrameId = requestAnimationFrame(animate);
        };

        init();
        animate();

        return () => {
            window.removeEventListener('resize', resizeCanvas);
            window.removeEventListener('mousemove', handleMouseMove);
            cancelAnimationFrame(animationFrameId);
        };
    }, []);

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                zIndex: 0,
                pointerEvents: 'none',
                background: 'transparent'
            }}
        />
    );
};

export default ParticlesBackground;
