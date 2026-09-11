import { useEffect } from "react";

function VendorModal({ vendor, onClose }) {
    if (!vendor) return null;

    // Handle ESC key to close modal
    useEffect(() => {
        function handleKeyDown(e) {
            if (e.key === "Escape") {
                onClose();
            }
        }
        window.addEventListener("keydown", handleKeyDown);
        // Lock body scrolling
        const prevOverflow = document.body.style.overflow;
        document.body.style.overflow = "hidden";

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            document.body.style.overflow = prevOverflow;
        };
    }, [onClose]);

    const formatStatus = (status) => {
        if (!status) return "Needs Verification";
        return status
            .split("_")
            .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
            .join(" ");
    };

    const getStatusClass = (status) => {
        if (status === "shortlist_candidate") return "badge-green";
        if (status === "needs_verification") return "badge-amber";
        return "badge-gray";
    };

    const getMatchClass = (match) => {
        if (match === "exact_match") return "badge-green";
        if (match === "near_match") return "badge-blue";
        if (match === "category_lead") return "badge-purple";
        return "badge-gray";
    };

    const getConfidenceClass = (conf) => {
        if (conf === "high") return "badge-green";
        if (conf === "medium") return "badge-blue";
        return "badge-amber";
    };

    return (
        <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
            <div className="modal-card" onClick={(e) => e.stopPropagation()}>
                {/* Modal Header */}
                <div className="modal-header">
                    <div className="modal-header-info">
                        <div className="modal-title-row">
                            <h2 className="modal-title">{vendor.vendor_name}</h2>
                            <span className={`status-pill ${getStatusClass(vendor.recommendation_status)}`}>
                                {formatStatus(vendor.recommendation_status)}
                            </span>
                        </div>
                        <p className="modal-location">
                            📍 {vendor.location || "Location not specified"}
                            {vendor.country ? ` • ${vendor.country}` : ""}
                            {vendor.geographic_category ? ` (${vendor.geographic_category.toUpperCase()})` : ""}
                        </p>
                    </div>
                    <button className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
                        ✕
                    </button>
                </div>

                {/* KPI Metrics Bar */}
                <div className="modal-metrics-bar">
                    <div className="metric-box highlight">
                        <span className="metric-label">Composite Score</span>
                        <strong className="metric-value">{vendor.total_score ?? "N/A"}</strong>
                        <span className="metric-sub">out of 100</span>
                    </div>
                    <div className="metric-box">
                        <span className="metric-label">Match Type</span>
                        <span className={`badge ${getMatchClass(vendor.match_type)}`}>
                            {formatStatus(vendor.match_type)}
                        </span>
                    </div>
                    <div className="metric-box">
                        <span className="metric-label">Evidence Confidence</span>
                        <span className={`badge ${getConfidenceClass(vendor.confidence)}`}>
                            {(vendor.confidence || "Unknown").toUpperCase()}
                        </span>
                    </div>
                    <div className="metric-box">
                        <span className="metric-label">Geography Tier</span>
                        <strong className="metric-text-val">
                            {vendor.geographic_category ? vendor.geographic_category.toUpperCase() : "N/A"}
                        </strong>
                    </div>
                </div>

                {/* Modal Scrollable Body */}
                <div className="modal-body">
                    {/* Key Evidence */}
                    <section className="modal-section">
                        <h3 className="section-title">
                            <span className="icon">✓</span> Key Verified Evidence
                        </h3>
                        {vendor.key_evidence?.length ? (
                            <ul className="evidence-list">
                                {vendor.key_evidence.map((item, idx) => (
                                    <li key={idx}>
                                        <span className="check-bullet">✓</span>
                                        <span>{item}</span>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="empty-text">No verified evidence points captured for this vendor.</p>
                        )}
                    </section>

                    {/* Unresolved Issues & Risks */}
                    <section className="modal-section">
                        <h3 className="section-title warning">
                            <span className="icon">⚠️</span> Unresolved Issues & Risks
                        </h3>
                        {vendor.unresolved_issues?.length ? (
                            <ul className="issues-list">
                                {vendor.unresolved_issues.map((item, idx) => (
                                    <li key={idx}>
                                        <span className="warn-bullet">⚠</span>
                                        <span>{item}</span>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="empty-text positive">✓ No unresolved issues or technical risks reported.</p>
                        )}
                    </section>

                    {/* Recommended Next Step */}
                    <section className="modal-section">
                        <h3 className="section-title">
                            <span className="icon">🎯</span> Recommended Next Action
                        </h3>
                        <div className="callout-box">
                            <p>{vendor.recommended_next_step || "Proceed with standard RFQ and technical specification validation."}</p>
                        </div>
                    </section>

                    {/* Sources & Citations */}
                    <section className="modal-section">
                        <h3 className="section-title">
                            <span className="icon">🔗</span> Cited Evidence Sources ({vendor.source_urls?.length || 0})
                        </h3>
                        {vendor.source_urls?.length ? (
                            <div className="sources-chips">
                                {vendor.source_urls.map((url, idx) => {
                                    let domain = "";
                                    try {
                                        domain = new URL(url).hostname.replace("www.", "");
                                    } catch {
                                        domain = `Source ${idx + 1}`;
                                    }
                                    return (
                                        <a
                                            key={idx}
                                            href={url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="source-chip"
                                        >
                                            <span className="link-icon">↗</span>
                                            <span className="link-text">{domain}</span>
                                        </a>
                                    );
                                })}
                            </div>
                        ) : (
                            <p className="empty-text">No direct web source URLs recorded.</p>
                        )}
                    </section>

                    {/* Contact Information */}
                    {(vendor.website || (vendor.contact_details && vendor.contact_details.length > 0)) && (
                        <section className="modal-section">
                            <h3 className="section-title">
                                <span className="icon">📞</span> Contact & Website
                            </h3>
                            <div className="contact-details-box">
                                {vendor.website && (
                                    <p>
                                        🌐 <strong>Official Website:</strong>{" "}
                                        <a href={vendor.website} target="_blank" rel="noopener noreferrer">
                                            {vendor.website}
                                        </a>
                                    </p>
                                )}
                                {vendor.contact_details?.map((detail, idx) => (
                                    <p key={idx}>✉ / 📱 {detail}</p>
                                ))}
                            </div>
                        </section>
                    )}
                </div>

                {/* Modal Footer */}
                <div className="modal-footer">
                    <button className="btn-secondary" onClick={onClose}>
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
}

export default VendorModal;
