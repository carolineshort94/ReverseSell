//@ts-check
import { createContext, useContext } from "react";

/**
 * @typedef {{user: null | {username:string}, logout: () => Promise , login: () => Promise, signup: () => Promise, refreshUser: () => Promise<void>}} AuthContextType
 */

/**@type {import('react').Context<AuthContextType>} */
export const AuthContext = createContext(
    /** @type {AuthContextType} */({
        user: null,
        login: async () => { },
        signup: async () => { },
        logout: async => { },
        refreshUser: async () => { },
    })
);

/**
 * Custom hook to access auth context.
 * @returns {AuthContextType}
 */
export function userAuth() {
    return useContext(AuthContext);
}
