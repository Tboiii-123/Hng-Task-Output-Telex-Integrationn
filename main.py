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
            "app_logo": "https://www.google.com/imgres?q=name%20notifier%20logo%20for%20api&imgurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fvector-multi-color-icon-webhook-600w-2545676463.jpg&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fnotifier-logo&docid=ZHyur4VYW14V1M&tbnid=z1ir3cEwbaHJFM&vet=12ahUKEwi6x46DqNSLAxUQWEEAHWZbLSEQM3oECBsQAA..i&w=600&h=620&hcb=2&itg=1&ved=2ahUKEwi6x46DqNSLAxUQWEEAHWZbLSEQM3oECBsQAA",
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



