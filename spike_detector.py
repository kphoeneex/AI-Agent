from collections import deque
from datetime import datetime, timedelta
from typing import Callable, Deque, Dict

class SpikeDetector:
    """
    Maintains a rolling window of messages.
    Calls `callback(alert_dict)` when the share of
    high‑urgency negative messages crosses `thresh_neg_percent`.
    """
    def __init__(
        self,
        window_minutes: int = 30,
        thresh_neg_percent: float = 0.20,
        callback: Callable[[Dict], None] | None = None
    ):
        self.window: Deque[Dict] = deque()
        self.window_minutes      = window_minutes
        self.thresh_neg_percent  = thresh_neg_percent
        self.callback            = callback

    def add(self, ticket: Dict):
        """Add a new classified ticket and evaluate spike conditions."""
        now = ticket["timestamp"]
        self.window.append(ticket)

        # Drop old messages
        cutoff = now - timedelta(minutes=self.window_minutes)
        while self.window and self.window[0]["timestamp"] < cutoff:
            self.window.popleft()

        self._check_spike()

    def _check_spike(self):
        total = len(self.window)
        if total == 0:  # guard
            return

        neg_high = sum(
            1 for t in self.window
            if t["emotion"] in {"anger", "sadness"} and t["urgency"] == "high"
        )
        frac = neg_high / total

        if frac >= self.thresh_neg_percent and self.callback:
            self.callback({
                "ts":        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "total":     total,
                "neg_high":  neg_high,
                "fraction":  round(frac * 100, 1)
            })
