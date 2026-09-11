function VendorCard({
    vendor,
    onClose
}) {

    if (!vendor) {
        return null;
    }


    return (

        <div className="vendor-detail">

            <div className="vendor-detail-header">

                <div>

                    <h2>
                        {vendor.vendor_name}
                    </h2>

                    <p>
                        {vendor.location || "Location unknown"}
                        {" "}
                        {vendor.country
                            ? `• ${vendor.country}`
                            : ""
                        }
                    </p>

                </div>

                <div>
                    <span>Decision Status</span>
                    <strong>{vendor.recommendation_status || "needs_verification"}</strong>
                </div>


                <button
                    className="close-button"
                    onClick={onClose}
                >
                    ×
                </button>

            </div>


            <div className="vendor-summary">

                <div className="score-box">

                    <span>
                        Total Score
                    </span>

                    <strong>
                        {vendor.total_score}
                    </strong>

                </div>


                <div>

                    <span>
                        Match
                    </span>

                    <strong>
                        {vendor.match_type}
                    </strong>

                </div>


                <div>

                    <span>
                        Confidence
                    </span>

                    <strong>
                        {vendor.confidence}
                    </strong>

                </div>

            </div>


            <section>

                <h3>
                    Evidence
                </h3>

                {vendor.key_evidence?.length ? (

                    <ul>

                        {vendor.key_evidence.map(
                            (item, index) => (

                                <li key={index}>
                                    ✓ {item}
                                </li>

                            )
                        )}

                    </ul>

                ) : (

                    <p>
                        No key evidence available.
                    </p>

                )}

            </section>


            <section>

                <h3>
                    Unresolved Issues
                </h3>

                {vendor.unresolved_issues?.length ? (

                    <ul>

                        {vendor.unresolved_issues.map(
                            (item, index) => (

                                <li key={index}>
                                    ⚠ {item}
                                </li>

                            )
                        )}

                    </ul>

                ) : (

                    <p>
                        No unresolved issues reported.
                    </p>

                )}

            </section>


            <section>

                <h3>
                    Recommended Next Step
                </h3>

                <p>
                    {vendor.recommended_next_step}
                </p>

            </section>


            <section>

                <h3>
                    Sources
                </h3>

                {vendor.source_urls?.length ? (

                    <ul className="sources">

                        {vendor.source_urls.map(
                            (url, index) => (

                                <li key={index}>

                                    <a
                                        href={url}
                                        target="_blank"
                                        rel="noreferrer"
                                    >
                                        Source {index + 1}
                                    </a>

                                </li>

                            )
                        )}

                    </ul>

                ) : (

                    <p>
                        No source URLs available.
                    </p>

                )}

            </section>

            {(vendor.website || vendor.contact_details?.length) && (
                <section>
                    <h3>Contact</h3>
                    {vendor.website && (
                        <p><a href={vendor.website} target="_blank" rel="noreferrer">Vendor website</a></p>
                    )}
                    {vendor.contact_details?.map((detail, index) => <p key={index}>{detail}</p>)}
                </section>
            )}

        </div>
    );
}


export default VendorCard;
