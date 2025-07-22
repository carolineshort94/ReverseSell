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


            </main>

        </>
    )
}
