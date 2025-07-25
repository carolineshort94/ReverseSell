import React from "react";
import { Link } from "react-router-dom";
import "../style/Footer.css";

function Footer() {
    return (
        <footer className="footer">
            <p>© 2025 Reserve Sell. All rights reserved.</p>
            <div className="footer-links">
                <Link to="/privacy">Privacy Policy</Link>
                <Link to="/terms">Terms of Service</Link>
                <Link to="/contact">Contact Us</Link>
            </div>
        </footer>
    );
}

export default Footer;
