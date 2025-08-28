import { useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import { userAuth } from "../context/AuthContext";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { FcGoogle } from "react-icons/fc";
import "../style/Signup.css";


const BASE = "http://127.0.0.1:8000";

export default function Signup() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [contactPhone, setContactPhone] = useState("");
    const [error, setError] = useState("");

    const { refreshUser, googleSignIn } = userAuth();
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Password do not match!")
            return
        }

        try {
            const res = await fetch(`${BASE}/signup`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName, contact_phone: contactPhone }),
            })

            if (res.ok) {
                await refreshUser();
                navigate("/");
            } else {
                const data = await res.json();
                setError(data.detail || "Signup failed")
            }
        } catch (err) {
            console.error("Signup error:", err);
            setError("An error occurred during signup. Please try again.");
        }


    };

    const handleGoogleSignup = async () => {
        try {
            await googleSignIn();
            navigate("/");
        } catch (err) {
            console.error("Google signup error:", err);
            setError("An error occurred during Google signup. Please try again.");
        }
    };

    return (
        <>
            <Header />
            <div className="signup-page">
                <div className="signup-card">
                    <h2>Sign up now</h2>
                    <p className="subtitle">Create a free account</p>

                    <button className="google-btn" onClick={handleGoogleSignup}>
                        <FcGoogle size={20} />
                        <span>Sign up with Google</span>
                    </button>


                    <div className="divider">
                        <span>or</span>
                    </div>

                    <form onSubmit={handleSignup}>
                        <label>First Name</label>
                        <input
                            type="text"
                            value={firstName}
                            onChange={(e) => setFirstName(e.target.value)}
                            placeholder="First Name"
                            required
                        />
                        <label>Last Name</label>
                        <input
                            type="text"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                            placeholder="Last Name"
                            required
                        />
                        <label>Contact Phone</label>
                        <input
                            type="tel"
                            value={contactPhone}
                            onChange={(e) => setContactPhone(e.target.value)}
                            placeholder="Contact Phone"
                            required
                        />
                        <label>Email address</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com"
                            required
                        />
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                        <label>Confirm Password</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Confirm your password"
                            required
                        />
                        {error && <p className="error-message">{error}</p>}
                        <button type="submit" className="primary-btn">Sign Up</button>
                    </form>

                    <p className="login-link">
                        Already have an account? <a href="/login">Login</a>
                    </p>
                </div>
            </div>
            <Footer />
        </>
    )
}
