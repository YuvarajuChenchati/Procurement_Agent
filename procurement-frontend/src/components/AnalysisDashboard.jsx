function AnalysisDashboard({ report, onOpenAnalysisModal, onDownload }) {
    if (!report) return null;

    const ahmCount = report.ahmedabad_vendors?.length || 0;
    const indCount = report.india_vendors?.length || 0;
    const gloCount = report.global_vendors?.length || 0;
    const excCount = report.excluded_or_unverified?.length || 0;
    const totalShortlist = ahmCount + indCount + gloCount;
    const ambiguitiesCount = report.ambiguities?.length || 0;

    const req = report.original_requirement || {};
    const loc = req.location || {};

    const scrollToSection = (id) => {
        const el = document.getElementById(id);
        if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    };

    return (
        <section className="analysis-dashboard-card">
            {/* Top Header */}
            <div className="dashboard-header">
                <div>
                    <span className="dashboard-eyebrow">Executive Summary</span>
                    <h2 className="dashboard-title">Procurement Intelligence & Analysis</h2>
                    <p className="dashboard-sub">
                        Target: <strong>{req.material || "Industrial Material"}</strong> • Benchmark:{" "}
                        <strong>{loc.city ? `${loc.city}, ${loc.country}` : "Ahmedabad, India"}</strong>
                    </p>
                </div>
                <div className="dashboard-top-actions">
                    <button
                        className="btn-primary"
                        onClick={onOpenAnalysisModal}
                    >
                        🔍 View Full Analysis Details
                    </button>
                    <div className="export-btn-group">
                        <button className="btn-outline" onClick={() => onDownload("json")}>
                            📥 JSON
                        </button>
                        <button className="btn-outline" onClick={() => onDownload("csv")}>
                            📥 CSV
                        </button>
                    </div>
                </div>
            </div>

            {/* Ambiguity Alert Banner if any */}
            {ambiguitiesCount > 0 && (
                <div className="ambiguity-alert-bar" onClick={onOpenAnalysisModal}>
                    <span className="alert-icon">⚠️</span>
                    <div className="alert-text">
                        <strong>{ambiguitiesCount} Technical {ambiguitiesCount === 1 ? "Ambiguity" : "Ambiguities"} Detected:</strong>{" "}
                        Missing dimensions, standard specs, or quantity units require clarification.
                    </div>
                    <button className="alert-action-link" type="button">
                        Review Ambiguities ↗
                    </button>
                </div>
            )}

            {/* KPI Stat Cards */}
            <div className="kpi-grid">
                <div className="kpi-card highlight" onClick={() => scrollToSection("ahmedabad-vendors")}>
                    <span className="kpi-label">Local Shortlist</span>
                    <div className="kpi-val-row">
                        <strong className="kpi-number">{ahmCount}</strong>
                        <span className="kpi-badge badge-green">Ahmedabad</span>
                    </div>
                    <span className="kpi-desc">Zero import duty & fastest lead time</span>
                </div>

                <div className="kpi-card" onClick={() => scrollToSection("india-vendors")}>
                    <span className="kpi-label">Domestic Shortlist</span>
                    <div className="kpi-val-row">
                        <strong className="kpi-number">{indCount}</strong>
                        <span className="kpi-badge badge-blue">India-wide</span>
                    </div>
                    <span className="kpi-desc">Established national manufacturers</span>
                </div>

                <div className="kpi-card" onClick={() => scrollToSection("global-vendors")}>
                    <span className="kpi-label">Global Suppliers</span>
                    <div className="kpi-val-row">
                        <strong className="kpi-number">{gloCount}</strong>
                        <span className="kpi-badge badge-purple">International</span>
                    </div>
                    <span className="kpi-desc">High capacity export capabilities</span>
                </div>

                <div className="kpi-card" onClick={() => scrollToSection("excluded-vendors")}>
                    <span className="kpi-label">Screened / Excluded</span>
                    <div className="kpi-val-row">
                        <strong className="kpi-number">{excCount}</strong>
                        <span className="kpi-badge badge-gray">Unverified</span>
                    </div>
                    <span className="kpi-desc">Failed spec match or lacks evidence</span>
                </div>
            </div>

            {/* Quick Navigation Jump Bar */}
            <div className="jump-nav-bar">
                <span className="jump-label">Jump to:</span>
                <button type="button" className="jump-chip" onClick={() => scrollToSection("ahmedabad-vendors")}>
                    📍 Ahmedabad ({ahmCount})
                </button>
                <button type="button" className="jump-chip" onClick={() => scrollToSection("india-vendors")}>
                    🇮🇳 India ({indCount})
                </button>
                <button type="button" className="jump-chip" onClick={() => scrollToSection("global-vendors")}>
                    🌐 Global ({gloCount})
                </button>
                <button type="button" className="jump-chip" onClick={() => scrollToSection("excluded-vendors")}>
                    Screened Out ({excCount})
                </button>
            </div>
        </section>
    );
}

export default AnalysisDashboard;
