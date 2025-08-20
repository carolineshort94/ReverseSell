//@ts-check
import React, { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";


/**
 * AuthProvider component to manage user auth state and provide context
 * @param {{children: import('react').ReactNode}} props
 * @returns {import('react').ReactElement}
 */
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const refreshUser = useCallback(async () => {
        try {
            const res = await fetch(`/api/me`, {
                credentials: "include"
            });
            if (res.ok) {
                setUser(await res.json());
            } else {
                setUser(null);
            }
        } catch (err) {
            console.error("Failed to refresed user:", err);
            setUser(null)
        }
    }, [])

    const logout = async () => {
        try {
            await fetch(`$/api/logout`, {
                method: "POST",
                credentials: "include",
            });
        } catch (err) {
            console.error("Logout error:", err)
        }
        setUser(null);
        navigate("/");
    };

    return (
        <AuthContext.Provider value={{ user, refreshUser, logout }} >
            {children}
        </AuthContext.Provider>
    )
}
