## BrandPulse Watchdog

An AI-powered CX monitor that classifies incoming support messages and alerts your team when negative/high-urgency traffic spikes. It:
- Classifies each message by sentiment, emotion, type, and urgency
- Detects spikes in high‑urgency negative messages over a rolling window
- Sends Slack alerts via Incoming Webhooks
- Saves a `classified_output.csv` for analysis and a simple Streamlit dashboard

### Requirements
- Python 3.10+
- Internet access (first run downloads Hugging Face models)

Install dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Quick Start (with sample data)
1) Create a Slack Incoming Webhook URL (see Slack docs) and copy it.
2) Run the classifier + spike detector on the sample CSV:
```bash
python main.py --csv sample_tickets.csv --slack_url "<YOUR_SLACK_WEBHOOK_URL>"
```
This will print live classifications and create `classified_output.csv` in the project root. On first run, model weights will download (can take a minute).

### Dashboard
Visualize the results with Streamlit:
```bash
streamlit run dashboard.py
```
- In the app, upload the generated `classified_output.csv` to see recent messages and basic charts.

### What’s Inside
- `main.py` – Orchestrates the stream → classification → spike detection → Slack alerts; saves CSV.
- `classifier.py` – Uses Hugging Face pipelines for sentiment and emotion; simple rules + zero‑shot for type; heuristic urgency.
- `data_stream.py` – Simulates real‑time ticket arrival from a CSV (`timestamp,text,channel`).
- `spike_detector.py` – Rolling window; triggers callback when negative/high‑urgency fraction crosses a threshold.
- `slack_alert.py` – Sends formatted alerts to Slack via webhook.
- `dashboard.py` – Streamlit UI to inspect `classified_output.csv`.
- `sample_tickets.csv` – Example input data to try the system.
- `requirements.txt` – Python dependencies.

### Configuration
- **Spike sensitivity**: tweak `window_minutes` and `thresh_neg_percent` in `SpikeDetector` (see `spike_detector.py`).
- **Classification hints/keywords**: edit sets in `classifier.py` (`NEGATIVE_HINTS`, `PRAISE_HINTS`, `HIGH_URGENCY_WORDS`).
- **Replay speed**: adjust `delay` in `ticket_stream` (see `data_stream.py`). Set to `0` to replay instantly.

### Troubleshooting
- **Transformers download slow/blocked**: ensure internet access or pre‑download models by running once on a network with access.
- **CUDA/GPU optional**: library falls back to CPU; first run may be slower.
- **Slack errors (400/404)**: verify the Incoming Webhook URL. If your Slack blocks webhooks, use an approved endpoint.

### Example: Run your own CSV
Ensure your CSV has columns `timestamp,text,channel` (channel optional). Then:
```bash
python main.py --csv path\to\your.csv --slack_url "<YOUR_SLACK_WEBHOOK_URL>"
```

### Notes
- For Windows, the commands above assume PowerShell in the project directory.
- The app writes `classified_output.csv` next to the scripts by default.
