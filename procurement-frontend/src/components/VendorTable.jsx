function VendorTable({
    id,
    title,
    vendors = [],
    onSelectVendor
}) {
    const formatStatus = (status) => {
        if (!status) return "Needs Verification";
        return status
            .split("_")
            .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
            .join(" ");
    };

    const getMatchBadgeClass = (match) => {
        if (match === "exact_match") return "badge-green";
        if (match === "near_match") return "badge-blue";
        if (match === "category_lead") return "badge-purple";
        return "badge-gray";
    };

    const getStatusBadgeClass = (status) => {
        if (status === "shortlist_candidate") return "badge-green";
        if (status === "needs_verification") return "badge-amber";
        return "badge-gray";
    };

    const getConfidenceBadgeClass = (conf) => {
        if (conf === "high") return "badge-green";
        if (conf === "medium") return "badge-blue";
        return "badge-amber";
    };

    return (
        <section className="vendor-section" id={id}>
            <div className="section-header-row">
                <div className="section-title-group">
                    <h2 className="section-title">{title}</h2>
                    <span className="count-pill">{vendors ? vendors.length : 0} {vendors?.length === 1 ? "vendor" : "vendors"}</span>
                </div>
            </div>

            {!vendors || vendors.length === 0 ? (
                <div className="empty-box">
                    <span className="empty-icon">📂</span>
                    <p className="empty-title">No verified vendors in this geographic category.</p>
                    <p className="empty-sub">Vendors screened during live research did not satisfy verification criteria or lacked verifiable documentation.</p>
                </div>
            ) : (
                <div className="table-container">
                    <table className="modern-table">
                        <thead>
                            <tr>
                                <th>Vendor / Supplier</th>
                                <th>Location</th>
                                <th>Match Type</th>
                                <th>Composite Score</th>
                                <th>Confidence</th>
                                <th>Decision Status</th>
                                <th style={{ textAlign: "right" }}>Action</th>
                            </tr>
                        </thead>

                        <tbody>
                            {vendors.map((vendor, index) => (
                                <tr key={index} className="table-row">
                                    <td>
                                        <div className="vendor-cell">
                                            <strong className="vendor-cell-name">{vendor.vendor_name}</strong>
                                            {vendor.vendor_type && (
                                                <span className="vendor-cell-type">{vendor.vendor_type}</span>
                                            )}
                                        </div>
                                    </td>

                                    <td>
                                        <div className="location-cell">
                                            <span>📍 {vendor.location || "Unknown"}</span>
                                            {vendor.country && <span className="country-sub">{vendor.country}</span>}
                                        </div>
                                    </td>

                                    <td>
                                        <span className={`badge ${getMatchBadgeClass(vendor.match_type)}`}>
                                            {formatStatus(vendor.match_type)}
                                        </span>
                                    </td>

                                    <td>
                                        <div className="score-cell">
                                            <strong className="score-num">{vendor.total_score ?? "0"}</strong>
                                            <span className="score-denom">/100</span>
                                        </div>
                                    </td>

                                    <td>
                                        <span className={`badge ${getConfidenceBadgeClass(vendor.confidence)}`}>
                                            {(vendor.confidence || "Unknown").toUpperCase()}
                                        </span>
                                    </td>

                                    <td>
                                        <span className={`badge ${getStatusBadgeClass(vendor.recommendation_status)}`}>
                                            {formatStatus(vendor.recommendation_status)}
                                        </span>
                                    </td>

                                    <td style={{ textAlign: "right" }}>
                                        <button
                                            type="button"
                                            className="btn-view-details"
                                            onClick={() => onSelectVendor(vendor)}
                                            title="View detailed scorecard, evidence, sources and risks in popup"
                                        >
                                            <span className="btn-icon">👁</span>
                                            <span>View Details</span>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </section>
    );
}

export default VendorTable;
