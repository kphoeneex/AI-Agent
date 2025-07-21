import time
import pandas as pd
from typing import Dict, Iterator

def ticket_stream(csv_path: str, delay: float = 2.0) -> Iterator[Dict]:
    """
    Yield one support message at a time, simulating real‑time arrival.
    CSV must have columns: timestamp,text,channel
    """
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    for _, row in df.iterrows():
        yield {
            "timestamp": row["timestamp"],
            "text":      row["text"],
            "channel":   row.get("channel", "ticket"),
        }
        time.sleep(delay)            # comment this out for instant replay
