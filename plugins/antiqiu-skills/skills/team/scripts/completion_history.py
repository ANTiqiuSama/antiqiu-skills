"""Collect serial completion-file metadata; never open payloads or execute jobs."""
import math
import re
from pathlib import Path


def completed_file_samples(directory, *, job_id, phase, total, completed, execution_id,
                           started_at, observed_at, name_pattern, position_offset=1, limit=32):
    """Return current consecutive completion samples, or None when unavailable.

    The adapter must first verify that the named position is a serial work unit,
    written only after completion, and that files were not copied or touched.
    name_pattern must contain a named integer group 'position'.
    """
    if not isinstance(execution_id, str) or not execution_id.strip():
        raise ValueError("verified execution_id is required for completion metadata")
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in (started_at, observed_at)):
        raise ValueError("finite process start and observation times are required")
    if started_at > observed_at or not 3 <= limit <= 64:
        raise ValueError("invalid observation window or sample limit")
    if type(completed) is not int or type(total) is not int or not 0 <= completed <= total:
        raise ValueError("file positions require integer completed and total counts")
    pattern = re.compile(name_pattern)
    if "position" not in pattern.groupindex:
        raise ValueError("name_pattern requires a named position group")
    points = []
    try:
        for path in Path(directory).iterdir():
            match = pattern.fullmatch(path.name)
            if not match:
                continue
            count = int(match.group("position")) + position_offset
            if not 1 <= count <= completed:
                continue
            try:
                if not path.is_file():
                    continue
                modified = path.stat().st_mtime
            except OSError:
                continue  # A raced/missing file cannot become a completed sample.
            if started_at <= modified <= observed_at:
                points.append({"at": modified, "completed": count})
    except OSError:
        return None  # Optional throughput history being absent is not job failure.
    points = sorted(points, key=lambda point: point["completed"])[-limit:]
    if len(points) < 3 or points[-1]["completed"] != completed:
        return None
    if any(b["completed"] != a["completed"] + 1 or b["at"] <= a["at"]
           for a, b in zip(points, points[1:])):
        return None
    return {"job_id": job_id, "phase": phase, "total": total, "execution_id": execution_id,
            "source": "completed_event_file_mtime", "points": points}
