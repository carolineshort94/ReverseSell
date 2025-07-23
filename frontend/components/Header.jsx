import { userAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../style/Header.css"; // Assuming you have a CSS file for styling
import React from "react"

export default function Header() {
    const { user, logout } = userAuth();
    const navigate = useNavigate();

    return (
        <header className="header">
            <h1 className="logo" onClick={() => navigate("/")}>Reverse Sell</h1>
            <nav className="nav">
                <button onClick={() => navigate("/")}>Home</button>
                <button onClick={() => navigate("/my-requests")}>My Requests</button>
                <button onClick={() => navigate("/my-offers")}>My Offers</button>
                {user ? (
                    <button onClick={() => navigate("/logout")}>Logout</button>
                ) : (
                    <>
                        <button onClick={() => navigate("/login")}>Login</button>
                        <button onClick={() => navigate("signup")}>Reverse</button>
                    </>
                )}
            </nav>
        </header>
    )
}
