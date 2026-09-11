# Agentic Procurement Tool

An evidence-first procurement research tool for industrial materials. It turns a material requirement, quantity, and procurement location into a ranked shortlist of Ahmedabad, India-wide, global, and unverified vendors.

## What it does

- Preserves the original input and identifies missing or ambiguous specifications.
- Searches Ahmedabad, India-wide, and global markets separately.
- Uses two targeted searches and caps deep source research at two candidates per geography (six maximum), keeping the live demo responsive while preserving geographic coverage.
- Extracts and deduplicates candidate vendors, then verifies their technical, geography, quantity, delivery, and standards evidence.
- Scores vendors using transparent weights: technical fit 35%, geography 20%, quantity feasibility 20%, evidence quality 15%, delivery capability 10%.
- Keeps unsupported facts as unresolved issues rather than presenting them as facts.
- Exports the finished report as JSON or CSV from the browser. The API also exposes `POST /procurement/export/json` and `/csv`.

## Architecture

`Requirement analysis → query planning → web search → vendor extraction → deduplication → geography classification → source research → evidence verification → evaluation → ranking → report`

LLM stages use structured Pydantic output. Deterministic code handles scoring, duplicate merging, geography grouping, and workflow orchestration. Search, extraction, verification, and evaluation failures are retained as evidence-trail issues so a single failed vendor does not end the run.

## Run locally

Prerequisites: Python 3.11+ and Node 20+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_key_here
```

Start the API from the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd procurement-frontend
npm install
npm run dev
```

Open the Vite URL (normally `http://localhost:5173`). The health check is `http://localhost:8000/health`.

## Assessment demonstration

The UI has M-01, M-02, and M-03 quick-fill buttons for the supplied Ahmedabad scenario. Run each material separately and download its JSON or CSV report. Quantities intentionally have no unit: the report must keep that as an ambiguity and should not claim stock, capacity, price, lead time, certification, or delivery unless a source explicitly supports it.

## Confidence and ranking

`exact_match` requires strong direct evidence. `near_match` has relevant but incomplete or differing evidence. `category_lead` is only material-category evidence. `unverified` is retained separately. Confidence reflects source reliability and completeness; it is not a claim that a vendor can fulfill an order. Procurement should use the report to choose who receives an RFQ and a technical-document request.

Source reliability is high for official vendor sites and manufacturer documentation, medium for established industry directories, and low for marketplaces or search-result-only evidence. A high-reliability source only confirms the facts it actually states: omitted stock, capacity, MOQ, or delivery data remains `not_found`. Scores are decision-support signals, never supplier approval. `shortlist_candidate` means ready for RFQ follow-up, `needs_verification` means material facts remain unresolved, and `unverified` means evidence was insufficient or processing failed.

## Limitations and next steps

- Live web results change and must be revalidated before purchasing.
- Delivery, export, MOQ, capacity, and stock are commonly unavailable publicly; the system marks these as unresolved unless sourced.
- Vendor names are deduplicated conservatively by normalised legal name; future work could add domain/address matching and human review.
- Long analyses are synchronous. A production deployment should use background jobs, persisted evidence, retry policies, and progress streaming.
- Public contact details are shown only when present in sourced data.

Never commit `.env` or other credentials.
