import re
import smtplib
from flask import Flask, request, jsonify,json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading
from flask_cors import CORS
import asyncio

app = Flask(__name__)



CORS(app, origins=["*"], supports_credentials=True, methods=["GET", "POST", "PUT"])



@app.route("/",methods=["GET"])
def root():

    data={
        "app_name":"Email Notifier",
        "description":"It notifies the Admin when a username/user is called in a channel at a particular period of time",
        "type":"Output Integration",
        "category":"Email & Messaging"
    }



    return jsonify(data)











# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "joshhearns37@gmail.com"
EMAIL_PASSWORD = "roue egvy bumj wkez"  # Use an App Password if 2FA is enabled
ADMIN_EMAIL = "lawalhussein775@gmail.com"

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
        print(f" Failed to send email: {str(e)}")

async def process_mentions(message):
    """Process mentions and send email notifications asynchronously."""
    mentions = re.findall(r"@(\w+)", message)

    if not mentions:
        return {"status": "No mentions found"}

    # Send an email for each mention
    for mention in mentions:
        await send_email(ADMIN_EMAIL, mention)

    response_data = {
        "event_name": "Email Notifier",
        "message": message,
        "status": "success",
        "username": "Tboiii",
        
    }

    print("Processed Data:", response_data)
    return response_data

def background_task(payload):
    """Wrapper to run async function in a separate thread."""
    asyncio.run(process_mentions(payload["message"]))

@app.route("/tick", methods=["POST"])
def detect_mentions():
    """Handles incoming POST requests and triggers background processing."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"message": "Invalid or missing message"}), 400

        # Run in the background
        thread = threading.Thread(target=background_task, args=(data,))
        thread.start()

        return jsonify({"status": "Accepted", "message": "Processing in background"}), 202

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    




@app.route("/integration.json",methods=['GET'])
def jsonsetting():
    base_url =str(request.base_url).rstrip("/")


    return jsonify(
        
            {
    "data": {
        "date": {
            "created_at": "2025-02-21",
            "updated_at": "2025-02-21"
        },
        "descriptions": {
            "app_name": "Channel Name Notifier",
            "app_description": "is an integration that detects when a user's name or role is mentioned in a message and sends a notification (email or API alert) to them",
            "app_logo": "data:image/jpeg;base64,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",
            "app_url":"https://hng-task-output-telex-integrationn.onrender.com",
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
}

  
    )













if __name__ == '__main__':
    app.run(debug=True)



