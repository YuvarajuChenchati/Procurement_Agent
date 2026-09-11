import { useState, useRef } from "react";

import RequirementForm from "./components/RequirementForm";
import AnalysisDashboard from "./components/AnalysisDashboard";
import AnalysisModal from "./components/AnalysisModal";
import VendorTable from "./components/VendorTable";
import VendorModal from "./components/VendorModal";
import LoadingProgress from "./components/LoadingProgress";

import { analyzeProcurement, downloadReport } from "./api";
import "./index.css";

function App() {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [selectedVendor, setSelectedVendor] = useState(null);
    const [showAnalysisModal, setShowAnalysisModal] = useState(false);

    const resultsRef = useRef(null);

    async function handleAnalyze(request) {
        setLoading(true);
        setError(null);
        setReport(null);

        // Smoothly scroll directly to the Analysis/Loading section
        setTimeout(() => {
            if (resultsRef.current) {
                resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }, 120);

        try {
            const result = await analyzeProcurement(request);
            setReport(result.report);

            // Re-ensure focus on analysis results once loaded
            setTimeout(() => {
                if (resultsRef.current) {
                    resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }, 150);
        } catch (err) {
            setError(err.message || "An unexpected error occurred during vendor analysis.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="app-layout">
            {/* Top Navigation / Brand Header */}
            <header className="app-header">
                <div className="header-container">
                    <div className="brand-group">
                        <div className="brand-icon">⚡</div>
                        <div>
                            <h1 className="brand-title">Agentic Procurement Intelligence</h1>
                            <p className="brand-subtitle">
                                Autonomous Multi-Agent Industrial Vendor Discovery, Verification & Multi-Tier Scoring
                            </p>
                        </div>
                    </div>
                    <div className="system-pill">
                        <span className="live-indicator"></span>
                        <span>Multi-Agent LangGraph Pipeline Ready</span>
                    </div>
                </div>
            </header>

            <main className="main-content">
                {/* Input Card */}
                <section className="card card-input">
                    <div className="card-header">
                        <div>
                            <h2 className="card-title">1. Procurement Requirement Configuration</h2>
                            <p className="card-subtitle">
                                Select an assessment demo preset or define custom industrial material specifications and target delivery geography.
                            </p>
                        </div>
                    </div>

                    <RequirementForm
                        onAnalyze={handleAnalyze}
                        loading={loading}
                    />
                </section>

                {/* Target Anchor for Direct Navigation */}
                <div ref={resultsRef} id="analysis-section" className="results-anchor">
                    {/* Loading State with Real-Time Percentage & Pipeline Stepper */}
                    {loading && (
                        <LoadingProgress isCompleted={false} />
                    )}

                    {/* Error Banner */}
                    {error && (
                        <section className="error-banner">
                            <div className="error-icon">⚠️</div>
                            <div className="error-body">
                                <strong>Pipeline Execution Error</strong>
                                <p>{error}</p>
                            </div>
                            <button
                                className="btn-retry"
                                onClick={() => {
                                    setError(null);
                                    window.scrollTo({ top: 0, behavior: "smooth" });
                                }}
                            >
                                Back to Form
                            </button>
                        </section>
                    )}

                    {/* Results & Analysis Section */}
                    {report && (
                        <>
                            {/* Executive Analysis Dashboard */}
                            <AnalysisDashboard
                                report={report}
                                onOpenAnalysisModal={() => setShowAnalysisModal(true)}
                                onDownload={(format) => downloadReport(report, format)}
                            />

                            {/* Geographic Category Tables */}
                            <VendorTable
                                id="ahmedabad-vendors"
                                title="Tier 1: Ahmedabad Local Suppliers (Direct Proximity)"
                                vendors={report.ahmedabad_vendors}
                                onSelectVendor={setSelectedVendor}
                            />

                            <VendorTable
                                id="india-vendors"
                                title="Tier 2: India Domestic Suppliers (Outside Ahmedabad)"
                                vendors={report.india_vendors}
                                onSelectVendor={setSelectedVendor}
                            />

                            <VendorTable
                                id="global-vendors"
                                title="Tier 3: Global International Manufacturers & Exporters"
                                vendors={report.global_vendors}
                                onSelectVendor={setSelectedVendor}
                            />

                            <VendorTable
                                id="excluded-vendors"
                                title="Screened / Excluded / Unverified Entities"
                                vendors={report.excluded_or_unverified}
                                onSelectVendor={setSelectedVendor}
                            />
                        </>
                    )}
                </div>
            </main>

            {/* Vendor Details Popup Modal */}
            {selectedVendor && (
                <VendorModal
                    vendor={selectedVendor}
                    onClose={() => setSelectedVendor(null)}
                />
            )}

            {/* Analysis Details Popup Modal */}
            {showAnalysisModal && (
                <AnalysisModal
                    report={report}
                    onClose={() => setShowAnalysisModal(false)}
                />
            )}
        </div>
    );
}

export default App;
