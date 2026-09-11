"""Console logging utility for the Procurement Agent workflow and APIs."""

import datetime
import sys
import time

# Ensure stdout and stderr handle utf-8 safely in Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _get_timestamp() -> str:
    """Return current timestamp formatted as HH:MM:SS."""
    return datetime.datetime.now().strftime("%H:%M:%S")


def _safe_print(text: str):
    """Print to stdout safely and flush immediately."""
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), flush=True)


def log_banner(title: str, char: str = "=", width: int = 70):
    """Print a visual section banner."""
    line = char * width
    _safe_print(f"\n{line}")
    _safe_print(f"  {title}")
    _safe_print(f"{line}")


def log_api_start(endpoint: str, details: dict = None):
    """Log the arrival of an API request with incoming parameters."""
    ts = _get_timestamp()
    log_banner(f"[{ts}] API REQUEST: {endpoint}")
    if details:
        for key, value in details.items():
            _safe_print(f"   * {key}: {value}")
    _safe_print("")


def log_api_end(endpoint: str, duration_s: float, details: dict = None):
    """Log the completion of an API request."""
    ts = _get_timestamp()
    log_banner(f"[{ts}] API COMPLETED: {endpoint} (Total Time: {duration_s:.2f}s)")
    if details:
        for key, value in details.items():
            _safe_print(f"   * {key}: {value}")
    _safe_print("")


def log_api_error(endpoint: str, duration_s: float, error: str):
    """Log an API failure."""
    ts = _get_timestamp()
    log_banner(f"[{ts}] API FAILED: {endpoint} (Elapsed: {duration_s:.2f}s)", char="!")
    _safe_print(f"   [ERROR] {error}\n")


def log_step_start(step_num: int, total_steps: int, name: str, details: str = None):
    """Log the start of a workflow step."""
    ts = _get_timestamp()
    prefix = f"[{ts}] [Step {step_num}/{total_steps}]"
    if details:
        _safe_print(f"\n{prefix} ===> {name} ({details})")
    else:
        _safe_print(f"\n{prefix} ===> {name}")


def log_step_end(step_num: int, total_steps: int, name: str, duration_s: float, summary: str = None):
    """Log the completion of a workflow step."""
    ts = _get_timestamp()
    prefix = f"[{ts}] [Step {step_num}/{total_steps}]"
    if summary:
        _safe_print(f"{prefix} [OK] {name} finished in {duration_s:.2f}s | {summary}")
    else:
        _safe_print(f"{prefix} [OK] {name} finished in {duration_s:.2f}s")


def log_substep(msg: str):
    """Log an intermediate action or item within a step."""
    _safe_print(f"    * {msg}")


def log_info(msg: str):
    """Log an informative message."""
    ts = _get_timestamp()
    _safe_print(f"[{ts}] [INFO] {msg}")


def log_warning(msg: str):
    """Log a warning message."""
    ts = _get_timestamp()
    _safe_print(f"[{ts}] [WARN] {msg}")


def log_error(msg: str):
    """Log an error message."""
    ts = _get_timestamp()
    _safe_print(f"[{ts}] [ERROR] {msg}")
