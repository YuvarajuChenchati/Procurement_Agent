import { useState, useEffect } from "react";

const PIPELINE_STAGES = [
    { threshold: 12, label: "Analyzing Requirements", icon: "📋", desc: "Parsing technical specs, dimensions, standards & detecting ambiguities" },
    { threshold: 28, label: "Formulating Search Strategy", icon: "🔍", desc: "Generating targeted supplier queries for Ahmedabad, India & Global tiers" },
    { threshold: 48, label: "Live Web Research", icon: "🌐", desc: "Querying live industrial supplier directories & web sources" },
    { threshold: 64, label: "Extracting & Screening Vendors", icon: "🏭", desc: "Parsing vendor profiles, capabilities & removing duplicates" },
    { threshold: 78, label: "Geographic Benchmarking", icon: "📍", desc: "Classifying proximity to delivery location & shortlisting candidates" },
    { threshold: 88, label: "Deep Evidence Verification", icon: "🛡️", desc: "Investigating supplier documentation, standards & technical proof" },
    { threshold: 96, label: "Scoring & Ranking", icon: "📊", desc: "Computing weighted composite score (technical, geographic, delivery)" },
    { threshold: 100, label: "Generating Final Report", icon: "📑", desc: "Compiling executive dossier with evidence-backed shortlists" },
];

function LoadingProgress({ isCompleted = false }) {
    const [progress, setProgress] = useState(4);
    const [secondsElapsed, setSecondsElapsed] = useState(0);

    // Elapsed timer
    useEffect(() => {
        const timer = setInterval(() => {
            setSecondsElapsed((prev) => prev + 1);
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    // Progress percentage incrementer
    useEffect(() => {
        if (isCompleted) {
            setProgress(100);
            return;
        }

        const interval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 95) {
                    // Slow down near 95% while waiting for final report synthesis
                    return Math.min(97, prev + 0.2);
                }
                if (prev >= 80) {
                    return prev + 0.8;
                }
                if (prev >= 50) {
                    return prev + 1.2;
                }
                return prev + 2.0;
            });
        }, 500);

        return () => clearInterval(interval);
    }, [isCompleted]);

    const displayPercent = Math.min(100, Math.round(progress));

    // Determine current active stage
    const currentStage = PIPELINE_STAGES.find((s) => progress <= s.threshold) || PIPELINE_STAGES[PIPELINE_STAGES.length - 1];
    const currentStageIndex = PIPELINE_STAGES.findIndex((s) => s.label === currentStage.label);

    const formatTime = (secs) => {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return `${m > 0 ? `${m}m ` : ""}${s}s`;
    };

    return (
        <section className="loading-container">
            <div className="loading-header">
                <div className="loading-badge">
                    <span className="pulse-dot"></span>
                    Live Multi-Agent Pipeline
                </div>
                <div className="loading-timer">
                    ⏱ Elapsed: <strong>{formatTime(secondsElapsed)}</strong>
                </div>
            </div>

            {/* Percentage Display */}
            <div className="loading-percentage-row">
                <div className="percentage-circle">
                    <span className="percentage-number">{displayPercent}</span>
                    <span className="percentage-symbol">%</span>
                </div>
                <div className="current-stage-info">
                    <div className="stage-title">
                        <span className="stage-icon">{currentStage.icon}</span>
                        <h3>{currentStage.label}</h3>
                    </div>
                    <p className="stage-desc">{currentStage.desc}</p>
                </div>
            </div>

            {/* Progress Bar */}
            <div className="progress-bar-wrapper">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${displayPercent}%` }}
                >
                    <div className="progress-bar-glow"></div>
                </div>
            </div>

            {/* Stepper Pipeline Indicators */}
            <div className="stepper-pipeline">
                {PIPELINE_STAGES.map((stage, idx) => {
                    const isPassed = progress > stage.threshold || isCompleted;
                    const isActive = idx === currentStageIndex && !isCompleted;
                    return (
                        <div
                            key={idx}
                            className={`step-chip ${isPassed ? "completed" : ""} ${isActive ? "active" : ""}`}
                            title={stage.desc}
                        >
                            <span className="step-icon">
                                {isPassed ? "✓" : isActive ? "●" : `${idx + 1}`}
                            </span>
                            <span className="step-text">{stage.label}</span>
                        </div>
                    );
                })}
            </div>

            <p className="loading-footnote">
                Our agentic system is querying live search tools, evaluating manufacturer evidence, and cross-referencing technical compliance in real time.
            </p>
        </section>
    );
}

export default LoadingProgress;
