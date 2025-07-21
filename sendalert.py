from datetime import datetime, timedelta
import requests

# Settings
NEGATIVE_THRESHOLD = 10
NEGATIVE_COOLDOWN = timedelta(minutes=30)
QUESTION_COOLDOWN = timedelta(minutes=30)

# Alert timestamps
last_negative_alert = None
last_question_alert = None

# Send alert to Slack
def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/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"
    payload = {"text": message}  # FIXED: was "test", should be "text"
    requests.post(webhook_url, json=payload)

# Check and alert for negative sentiment
def check_negative_alert(count_negative):
    global last_negative_alert
    now = datetime.utcnow()

    if count_negative >= NEGATIVE_THRESHOLD:
        if not last_negative_alert or (now - last_negative_alert) > NEGATIVE_COOLDOWN:
            alert_msg = f"🚨 Urgent: {count_negative} negative messages received in the last 30 minutes."
            send_slack_alert(alert_msg)
            last_negative_alert = now

# Check and alert for unresolved questions
def check_questions_alert(questions):
    global last_question_alert
    now = datetime.utcnow()

    if questions:
        if not last_question_alert or (now - last_question_alert) > QUESTION_COOLDOWN:
            question_texts = "\n".join(f"• {q}" for q in questions[:5])  # Show first 5
            alert_msg = f"❓ To Be Resolved: {len(questions)} questions received in the last 30 minutes:\n{question_texts}"
            send_slack_alert(alert_msg)
            last_question_alert = now

# Handle full batch stats
def handle_stats(count_positive, count_negative, questions):
    check_negative_alert(count_negative)
    check_questions_alert(questions)


if __name__ == "__main__":
    # Dummy test data
    dummy_count_positive = 6
    dummy_count_negative = 20  # > threshold → should trigger alert
    dummy_questions = [
        "Why was my package returned to sender?",
        "When will my refund be processed?",
        "Nobody has replied to my query!",
        "Why was I charged twice?",
        "I’m getting an error code 403"
    ]  # → should also trigger question alert

    handle_stats(dummy_count_positive, dummy_count_negative, dummy_questions)
