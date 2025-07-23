import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom"
import Header from "./Header"
import Footer from "./Footer"
import "./style/Home.css"


export default function HomePage() {
    const [requests, setRequests] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/requests?user_id=1")
            .then((res) => res.json())
            .then((data) => setRequests(data))
            .catch((err) => console.error("Failed to fetch requests", err))
    }, [])

    return (
        <>
            <Header />
            <main className="main-content">
                <aside className="sidebar">
                    <h2>What do you need?</h2>
                    <p>Tell us what product or service you're looking for!</p>
                    <button className="primary-btn">Post a New Request</button>

                    <h2>Are you a Seller?</h2>
                    <p>Find matching requests and submit your offers.</p>
                    <button className="secondary-btn">View Open Requests</button>
                </aside>

                <section className="requests">
                    <h2>Latest Open Requests</h2>
                    <div className="request-card">
                        <h3>Looking for a custom-built PC</h3>
                        <p>Need a high-performance gaming PC...</p>
                        <div className="tags">
                            <span className="tag blue">Electronics</span>
                            <span className="tag green">Gaming</span>
                            <span className="tag pink">Custom Build</span>
                        </div>
                        <p className="expires">Expires in: 3 days</p>
                    </div>
                    <button className="load-btn">Load More Requests</button>
                </section>
            </main>
            <Footer />

        </>
    )
}
