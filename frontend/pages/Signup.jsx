import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userAuth } from "../context/AuthContext";

const API_BASE = "http://localhost:8000";

export default function Signup() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");

    const { refreshUser } = userAuth();
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Password do not match!")
            return
        }

        const res = await fetch(`${API_BASE}/api/signup`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        })

        if (res.ok) {
            await refreshUser();
            navigate("/");
        } else {
            const data = await res.json();
            setError(data.detail || "Signup failed")
        }
    };

    return (
        <div>
            <h1>Signup</h1>
            <form onSubmit={handleSignup}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Confirm Password:</label>
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Singup</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <p>Already have an account? <a href="/login">Login</a></p>
        </div>
    )
}
