import { useState } from "react";

const DEMOS = [
    {
        id: "M-01",
        name: "M-01: ERW Pipe DN 50",
        material: "ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239",
        quantity: 1000,
        unit: "",
        city: "Ahmedabad",
        state: "Gujarat",
        country: "India",
        desc: "Strict spec with nominal diameter, dimensions & standard"
    },
    {
        id: "M-02",
        name: "M-02: 50mm MS ERW Class B",
        material: "50 mm MS ERW, Class B pipe",
        quantity: 500,
        unit: "",
        city: "Ahmedabad",
        state: "Gujarat",
        country: "India",
        desc: "Class-based specification test"
    },
    {
        id: "M-03",
        name: "M-03: ERW Pipe DN 80",
        material: "ERW pipe, DN 80, 88.9 x 5.5 mm, IS 1239",
        quantity: 1000,
        unit: "",
        city: "Ahmedabad",
        state: "Gujarat",
        country: "India",
        desc: "Larger outer diameter (88.9 mm) standard test"
    },
];

function RequirementForm({ onAnalyze, loading }) {
    const [material, setMaterial] = useState("ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239");
    const [quantity, setQuantity] = useState(1000);
    const [quantityUnit, setQuantityUnit] = useState("meters");
    const [city, setCity] = useState("Ahmedabad");
    const [state, setState] = useState("Gujarat");
    const [country, setCountry] = useState("India");
    const [selectedDemoId, setSelectedDemoId] = useState("M-01");

    function loadDemo(demo) {
        setSelectedDemoId(demo.id);
        setMaterial(demo.material);
        setQuantity(demo.quantity);
        setQuantityUnit(demo.unit || "");
        setCity(demo.city || "Ahmedabad");
        setState(demo.state || "Gujarat");
        setCountry(demo.country || "India");
    }

    function runDemoDirectly(demo) {
        loadDemo(demo);
        const request = {
            id: demo.id,
            material: demo.material,
            quantity: Number(demo.quantity),
            quantity_unit: demo.unit || null,
            location: {
                city: demo.city || "Ahmedabad",
                state: demo.state || "Gujarat",
                country: demo.country || "India"
            }
        };
        onAnalyze(request);
    }

    function handleSubmit(event) {
        event.preventDefault();
        const request = {
            id: selectedDemoId || "REQ-CUSTOM",
            material,
            quantity: Number(quantity),
            quantity_unit: quantityUnit || null,
            location: {
                city,
                state,
                country
            }
        };
        onAnalyze(request);
    }

    return (
        <form onSubmit={handleSubmit} className="requirement-form">
            {/* Quick Demo Selector */}
            <div className="demo-section">
                <div className="demo-header-label">
                    <span>⚡ Quick Assessment Demos (One-Click Run & Analyze):</span>
                </div>
                <div className="demo-cards-row">
                    {DEMOS.map((demo) => {
                        const isSelected = selectedDemoId === demo.id;
                        return (
                            <div
                                key={demo.id}
                                className={`demo-card ${isSelected ? "selected" : ""}`}
                            >
                                <div className="demo-card-top">
                                    <strong className="demo-badge">{demo.id}</strong>
                                    <span className="demo-qty">{demo.quantity} {demo.unit}</span>
                                </div>
                                <p className="demo-mat-text">{demo.material}</p>
                                <div className="demo-card-actions">
                                    <button
                                        type="button"
                                        className="btn-demo-load"
                                        onClick={() => loadDemo(demo)}
                                        disabled={loading}
                                        title="Load into form to inspect/edit"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        type="button"
                                        className="btn-demo-run"
                                        onClick={() => runDemoDirectly(demo)}
                                        disabled={loading}
                                        title="Load and immediately execute agentic pipeline"
                                    >
                                        ⚡ Run Demo
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Main Form Fields */}
            <div className="form-group">
                <label className="form-label">
                    Industrial Material / Specification Requirement <span className="req-star">*</span>
                </label>
                <textarea
                    value={material}
                    onChange={(e) => setMaterial(e.target.value)}
                    rows="3"
                    className="form-textarea"
                    placeholder="e.g. ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239"
                    required
                    disabled={loading}
                />
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label className="form-label">
                        Quantity <span className="req-star">*</span>
                    </label>
                    <input
                        type="number"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        min="1"
                        className="form-input"
                        required
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Quantity Unit</label>
                    <select
                        value={quantityUnit}
                        onChange={(e) => setQuantityUnit(e.target.value)}
                        className="form-select"
                        disabled={loading}
                    >
                        <option value="">Not specified</option>
                        <option value="meters">Meters</option>
                        <option value="pieces">Pieces</option>
                        <option value="tonnes">Tonnes</option>
                        <option value="feet">Feet</option>
                    </select>
                </div>
            </div>

            <div className="form-subtitle">
                <span>📍 Target Procurement Delivery Location</span>
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label className="form-label">City <span className="req-star">*</span></label>
                    <input
                        value={city}
                        onChange={(e) => setCity(e.target.value)}
                        className="form-input"
                        required
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">State <span className="req-star">*</span></label>
                    <input
                        value={state}
                        onChange={(e) => setState(e.target.value)}
                        className="form-input"
                        required
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Country <span className="req-star">*</span></label>
                    <input
                        value={country}
                        onChange={(e) => setCountry(e.target.value)}
                        className="form-input"
                        required
                        disabled={loading}
                    />
                </div>
            </div>

            <div className="form-submit-row">
                <button
                    type="submit"
                    className="btn-submit-primary"
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <span className="btn-spinner"></span>
                            <span>Analyzing Vendors Across Geography Tiers...</span>
                        </>
                    ) : (
                        <>
                            <span>🚀 Analyze Vendors & Generate Report</span>
                        </>
                    )}
                </button>
            </div>
        </form>
    );
}

export default RequirementForm;
