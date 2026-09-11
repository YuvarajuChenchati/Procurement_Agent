import { useEffect } from "react";

function AnalysisModal({ report, onClose }) {
    if (!report) return null;

    useEffect(() => {
        function handleKeyDown(e) {
            if (e.key === "Escape") {
                onClose();
            }
        }
        window.addEventListener("keydown", handleKeyDown);
        const prevOverflow = document.body.style.overflow;
        document.body.style.overflow = "hidden";

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            document.body.style.overflow = prevOverflow;
        };
    }, [onClose]);

    const req = report.original_requirement || {};
    const loc = req.location || {};
    const ambiguities = report.ambiguities || [];
    const assumptions = report.assumptions || [];
    const searchIssues = report.search_issues || [];

    const getSeverityBadge = (severity) => {
        const s = (severity || "").toLowerCase();
        if (s === "high") return "badge-red";
        if (s === "medium") return "badge-amber";
        return "badge-blue";
    };

    return (
        <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
            <div className="modal-card modal-lg" onClick={(e) => e.stopPropagation()}>
                {/* Modal Header */}
                <div className="modal-header">
                    <div className="modal-header-info">
                        <h2 className="modal-title">Procurement Requirement & AI Analysis Details</h2>
                        <p className="modal-location">
                            Request ID: <strong>{report.request_id || req.id || "N/A"}</strong> • Multi-Tier Vendor Evaluation Dossier
                        </p>
                    </div>
                    <button className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
                        ✕
                    </button>
                </div>

                {/* Modal Body */}
                <div className="modal-body">
                    {/* Normalized Requirement Section */}
                    <section className="modal-section">
                        <h3 className="section-title">
                            <span className="icon">📦</span> Material & Delivery Requirements
                        </h3>
                        <div className="analysis-grid">
                            <div className="info-cell">
                                <span className="cell-label">Material / Item</span>
                                <strong className="cell-value">{req.material || "Not specified"}</strong>
                            </div>
                            <div className="info-cell">
                                <span className="cell-label">Quantity</span>
                                <strong className="cell-value">
                                    {req.quantity ? `${req.quantity} ${req.quantity_unit || "(unit not specified)"}` : "Not specified"}
                                </strong>
                            </div>
                            <div className="info-cell">
                                <span className="cell-label">Target Delivery Location</span>
                                <strong className="cell-value">
                                    {loc.city ? `${loc.city}, ${loc.state ? `${loc.state}, ` : ""}${loc.country}` : "Not specified"}
                                </strong>
                            </div>
                            <div className="info-cell">
                                <span className="cell-label">Vendor Tiers Discovered</span>
                                <strong className="cell-value">
                                    {(report.ahmedabad_vendors?.length || 0) + (report.india_vendors?.length || 0) + (report.global_vendors?.length || 0)} Shortlisted
                                </strong>
                            </div>
                        </div>
                    </section>

                    {/* Ambiguities Section */}
                    <section className="modal-section">
                        <h3 className="section-title warning">
                            <span className="icon">⚠️</span> Detected Ambiguities & Missing Data ({ambiguities.length})
                        </h3>
                        {ambiguities.length > 0 ? (
                            <div className="ambiguity-cards-grid">
                                {ambiguities.map((item, idx) => (
                                    <div key={idx} className="ambiguity-item-card">
                                        <div className="ambiguity-item-header">
                                            <strong className="ambiguity-field">{item.field}</strong>
                                            <span className={`badge ${getSeverityBadge(item.severity)}`}>
                                                {item.severity ? `${item.severity.toUpperCase()} SEVERITY` : "FLAGGED"}
                                            </span>
                                        </div>
                                        <p className="ambiguity-issue">{item.issue}</p>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="empty-text positive">✓ No critical technical ambiguities found in the procurement input.</p>
                        )}
                    </section>

                    {/* Assumptions Section */}
                    <section className="modal-section">
                        <h3 className="section-title">
                            <span className="icon">🧠</span> Engineering & Procurement Assumptions ({assumptions.length})
                        </h3>
                        {assumptions.length > 0 ? (
                            <ul className="evidence-list">
                                {assumptions.map((item, idx) => (
                                    <li key={idx}>
                                        <span className="check-bullet">ℹ</span>
                                        <span>{item}</span>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="empty-text">No implicit assumptions were made; standard engineering defaults applied.</p>
                        )}
                    </section>

                    {/* Search & Audit Issues */}
                    {searchIssues.length > 0 && (
                        <section className="modal-section">
                            <h3 className="section-title">
                                <span className="icon">🌐</span> Search & Web Discovery Notes ({searchIssues.length})
                            </h3>
                            <ul className="issues-list">
                                {searchIssues.map((issue, idx) => (
                                    <li key={idx}>
                                        <span className="warn-bullet">•</span>
                                        <span>{issue}</span>
                                    </li>
                                ))}
                            </ul>
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

export default AnalysisModal;
