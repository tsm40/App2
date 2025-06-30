from email.mime.text import MIMEText
import smtplib
import os

def send_summary_email(info: dict):
    def format_field(key, value):
        return f"{key.title():<20}: {value if value else 'N/A'}"

    # Organize fields into logical sections 
    patient_section = [
        "name", "dob", "phone number", "email", "address"
    ]
    insurance_section = [
        "insurance provider", "payer name", "payer id"
    ]
    referral_section = [
        "referral source", "referral doctor"
    ]
    appointment_section = [
        "chief complaint", "appointment doctor", "appointment time"
    ]

    # Build formatted body with section titles
    body_lines = []

    body_lines.append("=== Patient Information ===")
    for field in patient_section:
        body_lines.append(format_field(field, info.get(field)))

    body_lines.append("\n=== Insurance Information ===")
    for field in insurance_section:
        body_lines.append(format_field(field, info.get(field)))

    body_lines.append("\n=== Referral Information ===")
    for field in referral_section:
        body_lines.append(format_field(field, info.get(field)))

    body_lines.append("\n=== Appointment Details ===")
    for field in appointment_section:
        body_lines.append(format_field(field, info.get(field)))

    body = "\n".join(body_lines)

    # get sender and recipient(s)
    sender = os.getenv("EMAIL_SENDER", "noreply@example.com")
    recipients_str = os.getenv("EMAIL_RECIPIENT", "admin@example.com")
    recipients = [email.strip() for email in recipients_str.split(",")]

    # create email
    msg = MIMEText(body)
    msg["Subject"] = "New Appointment Booking for " + info.get("name", "Unknown Patient")
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, os.getenv("EMAIL_PASSWORD")) 
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
