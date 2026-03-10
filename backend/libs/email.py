from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from libs.env import ENVS


def send_email(to_emails: List[str], subject: str, body: str):
    """Send email to multiple recipients."""
    msg = MIMEMultipart()
    msg['From'] = ENVS.EMAIL_FROM  # Assume added to env
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(ENVS.SMTP_SERVER, ENVS.SMTP_PORT)
    server.starttls()
    server.login(ENVS.SMTP_USER, ENVS.SMTP_PASSWORD)
    text = msg.as_string()
    server.sendmail(ENVS.EMAIL_FROM, to_emails, text)
    server.quit()


def send_booking_notification(event_type: str, event_data: dict):
    """Send notification email for booking events."""
    subject_map = {
        "BOOKING_CREATED": "Nova Reserva Criada",
        "BOOKING_UPDATED": "Reserva Atualizada",
        "BOOKING_CANCELED": "Reserva Cancelada",
    }
    subject = subject_map.get(event_type, "Notificação de Reserva")

    body = f"""
    Título: {event_data['title']}
    Sala: {event_data['room_id']}
    Horário: {event_data['start_at']} - {event_data['end_at']}
    Tipo de evento: {event_type}
    """

    participants = event_data.get('participants', [])
    if participants:
        send_email(participants, subject, body)