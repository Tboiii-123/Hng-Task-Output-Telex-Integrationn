import re
import smtplib
from flask import Flask, request, jsonify,json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)


# Get current date and time
now = datetime.now()

# Format it as a string
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current Date and Time:", formatted_time)

admin_mail ='lawalhussein775@gmail.com'
# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "joshhearns37@gmail.com"
EMAIL_PASSWORD = "roue egvy bumj wkez"  # Use App Password if 2FA is enabled

def send_email(to_email, mention):
    """Send a dummy email notification"""
    subject = f"Notification: You were mentioned!"
    body = f"Hello {mention},\n\nYou were mentioned in a message!\n\nBest,\nYour App"
    body=f"Hello Admin. {mention} was mentioned in the channel by {formatted_time} time"
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
        return f"Email sent to {to_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"



@app.route("/api", methods=["POST"])
def detect_mentions():
    """Detect @mentions in a message"""
    data = request.json
    content = data.get("content")

    

    if not content:
        return jsonify({"error": "Message content required"}), 400

    # Use regex to find words starting with @
    mentions = re.findall(r"@(\w+)", content)
     # Find mentions using regex
    

    email_status = send_email(admin_mail, mentions)



    return jsonify({
        "message": "Mentions detected",
        "content": content,
        "mentions": mentions
    }), 200






def load_json():
    with open("integration.json", "r") as file:
        data = json.load(file)
    return data

@app.route("/integration.json",methods=['GET'])
def jsonsetting():
    return jsonify(load_json())










if __name__ == '__main__':
    app.run(debug=True)



