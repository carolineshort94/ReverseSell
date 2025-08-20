import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../style/MyRequest.css";


export default function MyRequests() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [filter, setFilter] = useState("all"); // all | open | closed
    const navigate = useNavigate();

    useEffect(() => {
        let alive = true;
        setLoading(true);
        setError("");

        (async () => {
            try {
                // 1) Who am I?
                const meRes = await fetch(`/api/me`, { credentials: "include" });
                if (!meRes.ok) {
                    const txt = await meRes.text();
                    throw new Error(txt || "Not authenticated");
                }
                const me = await meRes.json();
                const userId = me?.id ?? me?.user_id ?? me?.account_id;
                if (!userId) throw new Error("Missing user id from /me response");

                // 2) My requests
                const reqRes = await fetch(`/api/requests/user/${userId}`, { credentials: "include" });
                if (!reqRes.ok) {
                    // If backend returns 200 with HTTPException(detail=...), this won't run.
                    // This branch is for real non-200 errors.
                    const txt = await reqRes.text();
                    throw new Error(txt || "Failed to load requests");
                }
                const raw = await reqRes.json();

                // If your backend sends {detail: "No requests..."} with 200, treat as empty.
                const list = Array.isArray(raw) ? raw : [];

                // Normalize to the shape the cards expect
                const normalized = list.map((d) => {
                    const expires_at = d.expires_at ?? d.expiry_date ?? null;
                    const offersArr = Array.isArray(d.offers) ? d.offers : null;
                    const offers_count = d.offers_count ?? (offersArr ? offersArr.length : 0);
                    const accepted_offers_count = d.accepted_offers_count ?? (offersArr ? offersArr.filter((o) => o.status === "accepted").length : 0);
                    const category_name = d.category_name ?? d.category?.name ?? null;
                    const days_to_expiry = d.days_to_expiry ?? (expires_at ? Math.max(0, Math.floor((new Date(expires_at).getTime() - Date.now()) / 86400000)) : null);

                    return {
                        id: d.id,
                        title: d.title,
                        description: d.description,
                        status: d.status ?? "open",
                        post_date: d.post_date ?? d.created_at ?? null,
                        expires_at,
                        days_to_expiry,
                        category_name,
                        tags: Array.isArray(d.tags) ? d.tags : (category_name ? [category_name] : []),
                        offers_count,
                        accepted_offers_count,
                    };
                });

                if (!alive) return;
                setItems(normalized);
            } catch (err) {
                console.error("Load MyRequests error:", err);
                if (!alive) return;
                setError("Could not load your requests. Please log in and try again.");
            } finally {
                if (alive) setLoading(false);
            }
        })();

        return () => { alive = false; };
    }, []);

    const visible = items.filter((r) => {
        if (filter === "all") return true;
        const ui = computeUiStatus(r.status, r.expires_at);
        return filter === "open" ? ui !== "Closed" : ui === "Closed";
    });

    return (
        <>
            <Header />
            <div className="myreq-page">
                <div className="myreq-container">
                    <h2 className="myreq-title">My Posted Requests</h2>
                    <p className="myreq-subtitle">Here you can view and manage all the requests you have posted.</p>

                    {/* Filters */}
                    <div className="myreq-filters">
                        <FilterBtn active={filter === "all"} onClick={() => setFilter("all")}>All</FilterBtn>
                        <FilterBtn active={filter === "open"} onClick={() => setFilter("open")}>Open</FilterBtn>
                        <FilterBtn active={filter === "closed"} onClick={() => setFilter("closed")}>Closed</FilterBtn>
                    </div>

                    {/* States */}
                    {loading && <SkeletonList />}
                    {!loading && error && <div className="myreq-error">{error}</div>}
                    {!loading && !error && visible.length === 0 && <EmptyState />}

                    {/* Cards */}
                    {!loading && !error && (
                        <div className="myreq-list">
                            {visible.map((r) => (
                                <RequestCard key={r.id} r={r} onNavigate={navigate} />
                            ))}
                        </div>
                    )}
                </div>
            </div>
            <Footer />
        </>
    );
}

// ---------- Small helpers ----------
function computeUiStatus(status, expiresAt) {
    if (status === "closed") return "Closed";
    if (!expiresAt) return "Active";
    const exp = new Date(expiresAt);
    return exp.getTime() < Date.now() ? "Closed" : "Active";
}

function formatDate(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, { year: "numeric", month: "2-digit", day: "2-digit" });
}

function plural(n, s) {
    return `${n} ${n === 1 ? s : s + "s"}`;
}

// ---------- UI pieces ----------
function FilterBtn({ active, onClick, children }) {
    return (
        <button className={`myreq-chip ${active ? "is-active" : ""}`} onClick={onClick}>
            {children}
        </button>
    );
}

function StatusBadge({ status }) {
    const cls = status === "Active" ? "status-active" : status === "Closed" ? "status-closed" : "status-open";
    return <span className={`myreq-badge ${cls}`}>{status}</span>;
}

function Tag({ label }) {
    return <span className="myreq-tag">{label}</span>;
}

function PrimaryBtn({ onClick, children }) {
    return (
        <button className="btn-primary" onClick={onClick}>
            {children}
        </button>
    );
}

function SecondaryBtn({ onClick, children }) {
    return (
        <button className="btn-secondary" onClick={onClick}>
            {children}
        </button>
    );
}

function RequestCard({ r, onNavigate }) {
    const uiStatus = r.ui_status || computeUiStatus(r.status, r.expires_at);
    const isClosed = uiStatus === "Closed";
    const hasOffers = (r.offers_count || 0) > 0;

    const primaryLabel = isClosed ? "View Details" : hasOffers ? "View Offers" : "View Request";
    const primaryHref = isClosed ? `/requests/${r.id}` : hasOffers ? `/requests/${r.id}/offers` : `/requests/${r.id}`;

    const tags = (r.tags && r.tags.length) ? r.tags : (r.category_name ? [r.category_name] : []);

    return (
        <article className="myreq-card">
            <div className="myreq-card-head">
                <h3 className="myreq-card-title">{r.title}</h3>
                <StatusBadge status={uiStatus} />
            </div>

            <p className="myreq-card-desc">{r.description}</p>

            <div className="myreq-tags">
                {tags.map((t, i) => (
                    <Tag key={i} label={t} />
                ))}
            </div>

            <div className="myreq-card-foot">
                <div className="myreq-meta">
                    {isClosed ? (
                        <>
                            <span className="meta-strong">Closed on:</span> {formatDate(r.expires_at)} | {plural(r.offers_count || 0, "Offer")} {r.accepted_offers_count ? `(${r.accepted_offers_count} Accepted)` : ""}
                        </>
                    ) : (
                        <>
                            {r.days_to_expiry != null ? (
                                <>
                                    <span className="meta-strong">Expires in:</span> {r.days_to_expiry} {r.days_to_expiry === 1 ? "day" : "days"} | {r.offers_count ? <span className="text-green">{plural(r.offers_count, "Offer")} Received</span> : "No Offers Yet"}
                                </>
                            ) : (
                                <>
                                    <span className="meta-strong">No Expiry</span> | {r.offers_count ? <span className="text-green">{plural(r.offers_count, "Offer")} Received</span> : "No Offers Yet"}
                                </>
                            )}
                        </>
                    )}
                </div>
                <div className="myreq-actions">
                    <PrimaryBtn onClick={() => onNavigate(primaryHref)}>{primaryLabel}</PrimaryBtn>
                    {!isClosed && <SecondaryBtn onClick={() => onNavigate(`/requests/${r.id}/edit`)}>Edit Request</SecondaryBtn>}
                </div>
            </div>
        </article>
    );
}

function SkeletonList() {
    return (
        <div className="myreq-skeletons">
            {Array.from({ length: 3 }).map((_, i) => (
                <div className="myreq-card skeleton" key={i}>
                    <div className="sk-line w-40" />
                    <div className="sk-line w-96" />
                    <div className="sk-tags">
                        <div className="sk-pill" />
                        <div className="sk-pill" />
                        <div className="sk-pill" />
                    </div>
                    <div className="sk-foot" />
                </div>
            ))}
        </div>
    );
}

function EmptyState() {
    return (
        <div className="myreq-empty">
            <h4>No requests yet</h4>
            <p>Create your first request so sellers can start sending offers.</p>
            <a href="/requests/new" className="btn-primary">Create Request</a>
        </div>
    );
}
