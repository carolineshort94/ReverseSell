import React, { use, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../style/MyRequests.css";
const API_BASE = "http://localhost:8000";


export default function MyRequests() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [filter, setFilter] = useState("all");
    const navigate = useNavigate();


    useEffect(() => {
        let alive = true;
        setLoading(true);
        setError("");

        (async () => {
            try {
                const meRes = await fetch(`${API_BASE}/api/me`, { credentials: "include" });
                if (!meRes.ok) {
                    navigate("/login");
                    return;
                }
                const me = await meRes.json();
                const userId = me?.id ?? me?.user_id ?? me?.account_id;
                if (!userId) {
                    throw new Error("User ID not found");
                }
                const reqRes = await fetch(`${API_BASE}/api/requests?user_id=${userId}`, { credentials: "include" });
                if (!reqRes.ok) {
                    const txt = await reqRes.text();
                    throw new Error(`Failed to fetch requests: ${txt}`);
                }
                const reqData = await reqRes.json();

                const list = Array.isArray(reqData) ? reqData : [];

                const normalized = list.map((d) => ({
                    const expires_at = d.expires_at ?? d.expiration_date ?? null;
                    const offersArr = Array.isArray(d.offers) ? d.offers : null;
                    const offers_count = d.offers_count ?? (offersArr ? offersArr.length : 0);
                    const accepted_offer_account = d.accepted_offer_account ?? (offersArr ? offersArr.filter((o) =>
                        o.status === "accepted").length : 0);
                    const category_name = d.category_name ?? d.category?.name ?? null;
                    const days_to_expiry = d.days_to_expiry ?? (expires_at ? Math.max(0, Math.floor((new Date(expires_at).getTime() - Date.now()) / 86400000)) : null);

                    return {
                        id: d.id,
                        title: d.title ?? d.request_title ?? "No Title",
                        description: d.description ?? d.request_description ?? "",
                        status: d.status ?? "unknown",
                        offers_count: offers_count,
                        accepted_offer_account: accepted_offer_account,
                        category_name: category_name,
                        expires_at: expires_at,
                        days_to_expiry: days_to_expiry,
                    };
                });

                if (!alive) return;
                setItems(normalized);
            } catch (err) {
                console.error("Error fetching requests:", err);
                if (!alive) return;
                setError("Failed to load your requests. Please try again later.");
            } finally {
                if (alive)
                    setLoading(false);

            }
        })();

        return () => { alive = false; };
    }, []);

    const visible = items.filter((r) => {
        if (filter === "all") return true;
        const ui = computerUiSatus(r.status, r.expires_at);
        return filter === "open" ? ui !== "Closed" : ui === "Closed";
    });


    return (
        <>
            <Header />
            <div className="my-re {

        </>
