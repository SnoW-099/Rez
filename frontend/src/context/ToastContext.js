import React, { createContext, useContext, useState, useCallback } from 'react';

const ToastContext = createContext();

export const useToast = () => useContext(ToastContext);

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    const addToast = useCallback((message, type = 'info') => {
        const id = Math.random().toString(36).substring(7);
        setToasts((prev) => [...prev, { id, message, type, show: false }]);

        // Trigger animation
        setTimeout(() => {
            setToasts((prev) =>
                prev.map(t => t.id === id ? { ...t, show: true } : t)
            );
        }, 10);

        // Auto remove
        setTimeout(() => {
            setToasts((prev) =>
                prev.map(t => t.id === id ? { ...t, show: false } : t)
            );
            setTimeout(() => {
                setToasts((prev) => prev.filter(t => t.id !== id));
            }, 400);
        }, 3000);
    }, []);

    return (
        <ToastContext.Provider value={{ addToast }}>
            {children}
            <div className="toast-container">
                {toasts.map((toast) => (
                    <div
                        key={toast.id}
                        className={`liquid-toast ${toast.show ? 'show' : ''}`}
                    >
                        <span className="toast-icon">✨</span>
                        {toast.message}
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
};
