import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings

def send_email(to: str, subject: str, body: str) -> bool:
    if not settings.SMTP_USER:
        return False
    
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP(settings.SMTP_HOST, 587) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_welcome_email(email: str, name: str) -> bool:
    subject = "Welcome to Find My Tutor!"
    body = f"""
    <h1>Welcome, {name}!</h1>
    <p>Thank you for joining Find My Tutor. Start exploring tutors today!</p>
    <p><a href="{settings.FRONTEND_URL}">Visit Find My Tutor</a></p>
    """
    return send_email(email, subject, body)

def send_booking_confirmation(email: str, details: dict) -> bool:
    subject = "Booking Confirmation - Find My Tutor"
    body = f"""
    <h1>Booking Confirmed!</h1>
    <p>Your tutoring session has been booked.</p>
    <p><strong>Subject:</strong> {details.get('subject')}</p>
    <p><strong>Date:</strong> {details.get('date')}</p>
    <p><strong>Amount:</strong> ₹{details.get('amount')}</p>
    """
    return send_email(email, subject, body)