import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userAuth } from "../context/AuthContext";
import "../style/Login.css";
import Header from "../components/Header";
import Footer from "../components/Footer";


import { auth, provider } from "../context/firebaseConfig";
import { signInWithPopup } from "firebase/auth";


const API_BASE = "http://localhost:8000";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [remember, setRemember] = useState(false);

    const { refreshUser } = userAuth();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        console.log({ email, password, remember });
        setError("");

        try {
            const res = await fetch(`${API_BASE}/api/login`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
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

    const handleGoogleLogin = async () => {
        try {
            const result = await signInWithPopup(auth, provider);
            const token = await result.user.getIdToken();

            const res = await fetch(`${API_BASE}/api/firebase-login`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ token }),
            });

            if (res.ok) {
                await refreshUser();
                navigate("/");
            } else {
                const data = await res.json();
                setError(data.detail || "Google login failed");
            }
        } catch (err) {
            console.error("Google login error:", err);
            setError("Something went wrong with Google login. Please try again.");
        }
    }




    return (
        <>
            <Header />
            <div className="login-container">
                <form className="login-form" onSubmit={handleLogin}>
                    <h1>Welcome Back!</h1>
                    <p className="subtitle">Please enter your details</p>



                    <label>Email address:</label>
                    <input
                        type="email"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />


                    <label>Password:</label>
                    <input
                        type="password"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    <button className="signin-btn" type="submit">Login</button>


                    <div className="options">
                        <label className="remember">
                            <input
                                type="checkbox"
                                checked={remember}
                                onChange={(e) => setRemember(e.target.checked)}
                            />
                            Remember me
                        </label>
                        <a href="/forgot" className="forgot">
                            Forgot password?
                        </a>
                    </div>



                    <button type="button" className="google-btn">
                        <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google logo" className="google-logo" />
                        Sign in with Google
                    </button>

                    <p className="footer-text">
                        Don't have an account? <a href="/register">Sign up</a>
                    </p>

                    {error && <p className="error-message">{error}</p>}
                </form>
            </div>

            <Footer />
        </>
    )
}
