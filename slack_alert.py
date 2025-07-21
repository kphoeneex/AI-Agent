import json
import requests

def send_slack_alert(webhook_url: str, alert: dict):
    text = (
        "🚨 *Spike in Negative Sentiment*\n"
        f"{alert['neg_high']} high‑urgency angry/confused messages "
        f"in the last 30 min ({alert['fraction']} % of {alert['total']})."
    )
    requests.post(webhook_url, data=json.dumps({"text": text}))
