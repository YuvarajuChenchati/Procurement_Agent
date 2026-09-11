import { useState } from "react";


function RequirementForm({ onAnalyze, loading }) {

    const [material, setMaterial] = useState(
        "ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239"
    );

    const [quantity, setQuantity] = useState(1000);

    const [quantityUnit, setQuantityUnit] = useState("");

    const [city, setCity] = useState("Ahmedabad");

    const [state, setState] = useState("Gujarat");

    const [country, setCountry] = useState("India");

    const demos = [
        ["M-01", "ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239", 1000],
        ["M-02", "50 mm MS ERW, Class B pipe", 500],
        ["M-03", "ERW pipe, DN 80, 88.9 x 5.5 mm, IS 1239", 1000],
    ];
    const [requestId, setRequestId] = useState("M-01");

    function loadDemo([id, demoMaterial, demoQuantity]) {
        setRequestId(id);
        setMaterial(demoMaterial);
        setQuantity(demoQuantity);
        setQuantityUnit("");
    }


    function handleSubmit(event) {

        event.preventDefault();


        const request = {

            id: requestId,

            material,

            quantity: Number(quantity),

            quantity_unit:
                quantityUnit || null,

            location: {
                city,
                state,
                country
            }
        };


        onAnalyze(request);
    }


    return (

        <form
            onSubmit={handleSubmit}
            className="requirement-form"
        >
            <div className="demo-actions">
                <span>Assessment demos:</span>
                {demos.map((demo) => <button type="button" key={demo[0]} onClick={() => loadDemo(demo)} disabled={loading}>{demo[0]}</button>)}
            </div>

            <div className="form-group">

                <label>
                    Material Requirement
                </label>

                <textarea
                    value={material}
                    onChange={(e) =>
                        setMaterial(e.target.value)
                    }
                    rows="4"
                    required
                />

            </div>


            <div className="form-row">

                <div className="form-group">

                    <label>
                        Quantity
                    </label>

                    <input
                        type="number"
                        value={quantity}
                        onChange={(e) =>
                            setQuantity(e.target.value)
                        }
                        min="0"
                        required
                    />

                </div>


                <div className="form-group">

                    <label>
                        Quantity Unit
                    </label>

                    <select
                        value={quantityUnit}
                        onChange={(e) =>
                            setQuantityUnit(e.target.value)
                        }
                    >

                        <option value="">
                            Not specified
                        </option>

                        <option value="pieces">
                            Pieces
                        </option>

                        <option value="meters">
                            Meters
                        </option>

                        <option value="tonnes">
                            Tonnes
                        </option>

                    </select>

                </div>

            </div>


            <h3>
                Procurement Location
            </h3>


            <div className="form-row">

                <div className="form-group">

                    <label>
                        City
                    </label>

                    <input
                        value={city}
                        onChange={(e) =>
                            setCity(e.target.value)
                        }
                        required
                    />

                </div>


                <div className="form-group">

                    <label>
                        State
                    </label>

                    <input
                        value={state}
                        onChange={(e) =>
                            setState(e.target.value)
                        }
                        required
                    />

                </div>


                <div className="form-group">

                    <label>
                        Country
                    </label>

                    <input
                        value={country}
                        onChange={(e) =>
                            setCountry(e.target.value)
                        }
                        required
                    />

                </div>

            </div>


            <button
                type="submit"
                disabled={loading}
            >

                {loading
                    ? "Analyzing..."
                    : "Analyze Vendors"
                }

            </button>

        </form>
    );
}


export default RequirementForm;
