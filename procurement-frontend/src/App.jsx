import { useState } from "react";

import RequirementForm from "./components/RequirementForm";
import AmbiguityPanel from "./components/AmbiguityPanel";
import VendorTable from "./components/VendorTable";
import VendorCard from "./components/VendorCard";

import { analyzeProcurement, downloadReport } from "./api";

import "./index.css";


function App() {

    const [report, setReport] = useState(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState(null);

    const [selectedVendor, setSelectedVendor] =
    useState(null);


    async function handleAnalyze(request) {

        setLoading(true);

        setError(null);

        setReport(null);


        try {

            const result =
                await analyzeProcurement(request);

            setReport(result.report);

        } catch (error) {

            setError(error.message);

        } finally {

            setLoading(false);

        }
    }


    return (

        <div className="app">

            <header>

                <h1>
                    Agentic Procurement Tool
                </h1>

                <p>
                    AI-powered industrial vendor
                    discovery and evaluation
                </p>

            </header>


            <main>

              {loading && (

    <section className="loading-card">

        <div className="spinner"></div>

        <h2>
            Analyzing Vendors...
        </h2>

        <p>
            Searching suppliers, verifying evidence,
            evaluating technical fit and ranking vendors.
        </p>

        <p className="loading-note">
            This may take a little while because
            the system performs live web research.
        </p>

    </section>

)}

                <section className="card">

                    <h2>
                        Procurement Requirement
                    </h2>

                    <RequirementForm
                        onAnalyze={handleAnalyze}
                        loading={loading}
                    />

                </section>


                {error && (

                    <section className="error">

                        <strong>
                            Error
                        </strong>

                        <p>
                            {error}
                        </p>

                    </section>

                )}


                {report && (

                    <>

                        <section className="card">

                            <h2>
                                Analysis
                            </h2>

                            <AmbiguityPanel
                                ambiguities={
                                    report.ambiguities
                                }
                            />

                            <div className="export-actions">
                                <button onClick={() => downloadReport(report, "json")}>Download JSON</button>
                                <button onClick={() => downloadReport(report, "csv")}>Download CSV</button>
                            </div>

                        </section>


                       <VendorTable
    title="Ahmedabad Vendors"
    vendors={report.ahmedabad_vendors}
    onSelectVendor={setSelectedVendor}
/>


<VendorTable
    title="India Vendors (outside Ahmedabad)"
    vendors={report.india_vendors}
    onSelectVendor={setSelectedVendor}
/>


<VendorTable
    title="Global Vendors"
    vendors={report.global_vendors}
    onSelectVendor={setSelectedVendor}
/>


<VendorTable
    title="Excluded / Unverified"
    vendors={report.excluded_or_unverified}
    onSelectVendor={setSelectedVendor}
/>

{selectedVendor && (

    <VendorCard
        vendor={selectedVendor}
        onClose={() =>
            setSelectedVendor(null)
        }
    />

)}

                    </>

                )}

            </main>

        </div>
    );
}


export default App;
