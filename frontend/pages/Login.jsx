import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userAuth } from "../context/AuthContext";
import "../style/Login.css";
import Header from "../components/Header";
import Footer from "../components/Footer";


const API_BASE = "http://localhost:8000";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const { refreshUser } = userAuth();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch(`${API_BASE}/api/login`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            })

            if (res.ok) {
                await refreshUser();
                navigate("/");
            } else {
                const data = await res.json();
                setError(data.detail || "Login failed")
            }

        } catch (err) {
            console.error("Login error:", err);
            setError("Something went wrong. Please try again.")
        }
    }




    return (
        <>
            <Header />
            <div className="login-wrapper">
                <form className="login-form" onSubmit={handleLogin}>
                    <h2 >Login</h2>
                    <div className="form-group">
                        <label>Username:</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password:</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Login</button>
                </form>
                {error && <p className="error-message">{error}</p>}
            </div>
            <Footer />
        </>
    )
}
