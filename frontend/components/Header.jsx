import { userAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../style/Header.css";
import React from "react"

export default function Header() {
    const { user, logout } = userAuth();
    const navigate = useNavigate();

    return (
        <header className="header">
            <h1 className="logo" onClick={() => navigate("/")}>Reverse Sell</h1>
            <nav className="nav-links">
                <a onClick={() => navigate("/")}>Home</a>
                <a onClick={() => navigate("/my-requests")}>My Requests</a>
                <a onClick={() => navigate("/my-offers")}>My Offers</a>
                {user ? (
                    <a className="white-btn" onClick={() => navigate("/logout")}>Logout</a>
                ) : (
                    <>
                        <a className="white-btn" onClick={() => navigate("/login")}>Login/Register</a>

                    </>
                )}
            </nav>
        </header>
    )
}
