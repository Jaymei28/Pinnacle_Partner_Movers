import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';

const LoaderContext = createContext(null);

export const useLoader = () => useContext(LoaderContext);

/**
 * Wraps the app and provides:
 *  - startLoading() / stopLoading() for manual control
 *  - A thin animated top-bar progress line that auto-completes
 */
export const PageLoaderProvider = ({ children }) => {
    const [active, setActive] = useState(false);
    const [width, setWidth] = useState(0);
    const timerRef = useRef(null);
    const completeRef = useRef(null);

    const startLoading = useCallback(() => {
        // Reset, then animate width to ~85% quickly
        setWidth(0);
        setActive(true);
        let w = 0;
        clearInterval(timerRef.current);
        timerRef.current = setInterval(() => {
            w += Math.random() * 12 + 4;
            if (w >= 85) { w = 85; clearInterval(timerRef.current); }
            setWidth(w);
        }, 80);
    }, []);

    const stopLoading = useCallback(() => {
        clearInterval(timerRef.current);
        setWidth(100);
        completeRef.current = setTimeout(() => {
            setActive(false);
            setWidth(0);
        }, 400);
    }, []);

    useEffect(() => () => {
        clearInterval(timerRef.current);
        clearTimeout(completeRef.current);
    }, []);

    return (
        <LoaderContext.Provider value={{ startLoading, stopLoading }}>
            {active && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        height: '3px',
                        width: `${width}%`,
                        background: 'linear-gradient(90deg, #f97316, #fb923c)',
                        zIndex: 9999,
                        transition: width === 100 ? 'width 0.25s ease' : 'width 0.12s ease',
                        borderRadius: '0 2px 2px 0',
                        boxShadow: '0 0 8px rgba(249, 115, 22, 0.6)',
                    }}
                />
            )}
            {children}
        </LoaderContext.Provider>
    );
};
