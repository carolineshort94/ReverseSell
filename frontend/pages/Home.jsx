import React, { useEffect, useState, useContext } from "react";
import Header from "../components/Header"
import Footer from "../components/Footer"
import RequestCard from "../components/RequestCard";
import { AuthContext } from "../context/AuthContext";
import "../style/Home.css"


export default function HomePage() {
    const { user } = useContext(AuthContext);
    const [requests, setRequests] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/requests", {
            credentials: "include",
        })
            .then((res) => res.json())
            .then((data) => {
                setRequests(data);
            })
            .catch((error) => {
                console.error("Error fetching requests:", error);
            });
    }, []);

    const handleOfferClick = (request) => {
        if (!user) {
            window.location.href = "/login";
        } else {
            window.location.href = `/offer/${request.id}`;
        }

    };
    return (
        <>
            <Header />
            <main className="main-content">
                <aside className="sidebar">
                    <h2>What do you need?</h2>
                    <p>Tell us what product or service you're looking for!</p>
                    <button className="primary-btn" onClick={() => {
                        if (!user) return window.location.href = "/login";
                        window.location.href = "/create-request";
                    }}></button>

                    <h2>Are you a Seller?</h2>
                    <p>Find matching requests and submit your offers.</p>
                    <button className="secondary-btn" onClick={() => {
                        window.scrollTo({ top: 0, behavior: 'smooth' })
                    }}>View Open Requests</button>
                </aside>

                <section className="requests">
                    <h2>Latest Open Requests</h2>
                    {requests.map((request) => (
                        <RequestCard
                            key={request.id}
                            request={request}
                            isLoggedIn={!!user}
                            onOfferClick={handleOfferClick}
                        />
                    ))}
                    <button className="load-btn">Load More Requests</button>
                </section>
            </main>
            <Footer />

        </>
    )
}
