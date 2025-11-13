from flask import Flask, request
import requests
import os

app = Flask(__name__)


PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route('/')
def home():
    return "Messenger Bot is running successfully!"


@app.route('/webhook', methods=['GET'])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data.get('object') == 'page':
        for entry in data.get('entry', []):
            for event in entry.get('messaging', []):
                if 'message' in event:
                    sender_id = event['sender']['id']
                    message_text = event['message'].get('text', '')
                    handle_message(sender_id, message_text)
    return "OK", 200


def handle_message(sender_id, message_text):
    """Simple text reply logic"""
    if message_text:
        response = f"Hello 👋, you said: {message_text}"
        send_message(sender_id, response)


def send_message(recipient_id, message_text):
    """Send message to user"""
    url = "https://graph.facebook.com/v19.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

