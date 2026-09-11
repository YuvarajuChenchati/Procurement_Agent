function VendorTable({
    title,
    vendors,
    onSelectVendor
}) {

    return (

        <section className="vendor-section">

            <h2>{title}</h2>

            {!vendors || vendors.length === 0 ? (

                <p className="empty">
                    No sufficiently verified vendors found.
                </p>

            ) : (

                <div className="table-container">

                    <table>

                        <thead>

                            <tr>

                                <th>Vendor</th>
                                <th>Location</th>
                                <th>Match</th>
                                <th>Score</th>
                                <th>Confidence</th>
                                <th>Decision status</th>
                                <th></th>

                            </tr>

                        </thead>


                        <tbody>

                            {vendors.map(
                                (vendor, index) => (

                                    <tr key={index}>

                                        <td>
                                            <strong>
                                                {vendor.vendor_name}
                                            </strong>
                                        </td>

                                        <td>
                                            {vendor.recommendation_status || "needs_verification"}
                                        </td>

                                        <td>
                                            {vendor.location || "Unknown"}
                                        </td>

                                        <td>
                                            <span
                                                className={`match-badge ${vendor.match_type}`}
                                            >
                                                {vendor.match_type}
                                            </span>
                                        </td>

                                        <td>
                                            <strong>
                                                {vendor.total_score}
                                            </strong>
                                        </td>

                                        <td>
                                            <span
                                                className={`confidence-badge ${vendor.confidence}`}
                                            >
                                                {vendor.confidence}
                                            </span>
                                        </td>

                                        <td>

                                            <button
                                                className="view-button"
                                                onClick={() =>
                                                    onSelectVendor(vendor)
                                                }
                                            >
                                                View Details
                                            </button>

                                        </td>

                                    </tr>

                                )
                            )}

                        </tbody>

                    </table>

                </div>

            )}

        </section>
    );
}


export default VendorTable;
