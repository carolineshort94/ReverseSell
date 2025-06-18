//@ts-check
import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";

const API_BASE = "http://localhost:8000";

/**
 * AuthProvider component to manage user auth state and provide context
 * @param {{children: import('react').ReactNode}} props
 * @returns {import('react').ReactElement}
 */
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const navigate = useNavigate;

    const refreshUser = useCallback(async () => {
        const res = await fetch(`${API_BASE}/api/me`, {
            credentials: "include"
        });
        if (res.ok) {
            setUser(await res.json());
        } else {
            setUser(null);
        }
    }, [])

    const logout = async () => {
        await fetch(`${API_BASE}/api/logout`, {
            method: "GET",
            credentials: "include",
        });
        setUser(null);
        navigate("/");
    };

    return (
        <AuthContext.Provider value={{ user, refreshUser }} >
            {children}
        </AuthContext.Provider>
    )
}
