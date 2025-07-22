import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../context/AuthProvider";
import Header from "./Header"
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
            <main className="home-page">
                <aside className="sidebar">
                    <h2>What do you need?</h2>
                    <p>Tell us what product or service you're
                        looking for!
                    </p>
                    <Link to='/new-request' className='button green'>
                        Post a New Request</Link>

                    <h3>Are you a Seller?</h3>
                    <p>Find matching requests and submit your offers.</p>
                    <Link to='/requests' className='button purple'>
                        View Open Requests</Link>
                </aside>

                <section className="requests-section">
                    <h2>Latest Open Requests</h2>
                    {requests.map((req) => (
                        <div key={req.id} className="request-card">
                            <h3>{req.title}</h3>
                            <p>{req.description}</p>
                            <div className="expires">Expires: {formatDate(req.expiry_date)}</div>
                            <Link to={`/requests/${req.id}`} className="view-link">
                                View Details & Offers →
                            </Link>
                        </div>
                    ))}

                    <button className="load-more">Load More Requests</button>
                </section>


            </main>

        </>
    )
}
