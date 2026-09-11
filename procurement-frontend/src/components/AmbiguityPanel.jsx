function AmbiguityPanel({ ambiguities }) {

    if (!ambiguities || ambiguities.length === 0) {
        return null;
    }


    return (

        <section className="ambiguity-panel">

            <h2>
                ⚠ Ambiguities
            </h2>


            {ambiguities.map(
                (ambiguity, index) => (

                    <div
                        key={index}
                        className="ambiguity"
                    >

                        <strong>
                            {ambiguity.field}
                        </strong>

                        <p>
                            {ambiguity.issue}
                        </p>

                        <span>
                            Severity: {ambiguity.severity}
                        </span>

                    </div>

                )
            )}

        </section>
    );
}


export default AmbiguityPanel;