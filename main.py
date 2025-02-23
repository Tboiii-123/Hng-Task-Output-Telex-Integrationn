import re
import smtplib
import threading
import asyncio
import httpx
from datetime import datetime
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True, methods=["GET", "POST", "PUT"])

load_dotenv()

passowrd =os.getenv('PASSWORD')


# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "joshhearns37@gmail.com"
EMAIL_PASSWORD = passowrd # Use an App Password if 2FA is enabled
ADMIN_EMAIL = "lawalhussein775@gmail.com"

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "app_name": "Email Notifier",
        "description": "It notifies the Admin when a username/user is called in a channel at a particular period of time",
        "type": "Output Integration",
        "category": "Email & Messaging"
    })

async def send_email(to_email, mention):
    """Send an email notification asynchronously."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subject = "Notification: You were mentioned!"
    body = f"Hello Admin,\n\n{mention} was mentioned in the channel at {now}.\n\nBest,\nYour App"
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

async def process_mentions(message, return_url):
    """Process mentions, send email notifications, and post data back."""
    mentions = re.findall(r"@(\w+)", message)

    if not mentions:
        return {"status": "No mentions found"}

    for mention in mentions:
        await send_email(ADMIN_EMAIL, mention)

    response_data = {
        "event_name": "Email Notifier",
        "message": message,
        "status": "success",
        "username": "Tboiii",
    }

    print("Processed Data:", response_data)

    # Post data back to the provided return URL
    if return_url:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(return_url, json=response_data)
                print(f"Data posted to {return_url}: {response.status_code}")
        except Exception as e:
            print(f"Failed to post data: {str(e)}")

    return response_data

def background_task(payload):
    """Run async function in a separate thread."""
    asyncio.run(process_mentions(payload["message"], payload.get("return_url", "")))

@app.route("/tick", methods=["POST"])
def detect_mentions():
    """Handles incoming POST requests and triggers background processing."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"message": "Invalid or missing message"}), 400

        thread = threading.Thread(target=background_task, args=(data,))
        thread.start()

        return jsonify({"status": "Accepted", "message": "Processing in background"}), 202

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/integration.json", methods=['GET'])
def jsonsetting():
    return jsonify({
        "data": {
            "date": {"created_at": "2025-02-21", "updated_at": "2025-02-21"},
            "descriptions": {
                "app_name": "Channel Name Notifier",
                "app_description": "Detects when a user's name or role is mentioned in a message and sends a notification.",
                "app_logo": "https://thenounproject.com/icon/mail-681630.png",
                "app_url": "https://hng-task-output-telex-integrationn.onrender.com",
                "background_color": "#fff"
            },
            "integration_category": "Email & Messaging",
            "is_active": True,
            "integration_type": "output",
            "key_features": [
                "No Backend Required",
                "Easy Integration",
                "Email Notification",
                "Scalable and Secure"
            ],
            "author": "Lawal Hussein",
            "settings": [
                {
                    "label": "Notification Type",
                    "type": "Multi-Select",
                    "description": "Description of the multi-select setting.",
                    "default": "Email,API Alert",
                    "required": True
                }
            ],
            "tick_url": "https://hng-task-output-telex-integrationn.onrender.com/tick",
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
