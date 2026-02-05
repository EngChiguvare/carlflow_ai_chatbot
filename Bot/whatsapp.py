from datetime import datetime
from .models import Lead, Appointment
from .lead_scoring import score_lead
from .ai_engine import get_ai_reply
from .email_alerts import send_hot_lead

BOOKING_WORDS = ['book', 'appointment', 'schedule', 'meeting', 'call']


def parse_datetime(text):
    try:
        return datetime.strptime(text.strip(), '%Y-%m-%d %H:%M')
    except Exception:
        return None


def process_message(phone, message):
    score, status = score_lead(message)

    lead = Lead.objects.create(
        phone=phone,
        message=message,
        score=score,
        status=status
    )

    if any(word in message.lower() for word in BOOKING_WORDS):
        Appointment.objects.create(
            lead=lead,
            requested_text=message
        )
        return (
            "📅 Appointment request received.\n"
            "Please send your preferred date & time in this format:\n"
            "YYYY-MM-DD HH:MM"
        )

    dt = parse_datetime(message)
    if dt:
        appt = Appointment.objects.filter(lead__phone=phone, scheduled_for__isnull=True).last()
        if appt:
            appt.scheduled_for = dt
            appt.confirmed = True
            appt.save()
            return f"✅ Appointment confirmed for {dt}" 

    if status == 'HOT':
        send_hot_lead(phone, message)

    return get_ai_reply(message)