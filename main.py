import argparse
import pandas as pd
from data_stream import ticket_stream
from classifier import classify
from spike_detector import SpikeDetector
from slack_alert import send_slack_alert

def run(csv_path: str, slack_url: str):
    detector = SpikeDetector(
        callback=lambda alert: send_slack_alert(slack_url, alert)
    )
    rows = []

    for ticket in ticket_stream(csv_path):
        labels = classify(ticket["text"])
        ticket.update(labels)

        detector.add(ticket)
        rows.append(ticket)

        print(
            f"[{ticket['timestamp']:%H:%M}] "
            f"{ticket['emotion']}/{ticket['urgency']}/{ticket['type']} → "
            f"{ticket['text'][:60]}…"
        )

    # Save classified data for dashboard
    pd.DataFrame(rows).to_csv("classified_output.csv", index=False)
    print("✓ Saved classified_output.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run BrandPulse Watchdog")
    ap.add_argument("--csv", required=True, help="Support-ticket CSV file")
    ap.add_argument("--slack_url", required=True, help="Slack Incoming‑Webhook URL")
    args = ap.parse_args()
    run(args.csv, args.slack_url)
