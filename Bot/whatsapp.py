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
    # 1️⃣ Hard safety check
    if not message:
        return "👋 Hi! How can I help you today?"

    message = message.strip()

    # 2️⃣ Score lead safely
    try:
        score, status = score_lead(message)
    except Exception:
        score, status = 0, "COLD"

    # 3️⃣ Save lead
    lead = Lead.objects.create(
        phone=phone or "unknown",
        message=message,
        score=score,
        status=status
    )

    message_lower = message.lower()

    # 4️⃣ Booking intent
    if any(word in message_lower for word in BOOKING_WORDS):
        Appointment.objects.create(
            lead=lead,
            requested_text=message
        )
        return (
            "📅 Appointment request received.\n\n"
            "Please send your preferred date & time like this:\n"
            "2026-02-10 14:30"
        )

    # 5️⃣ Date/time confirmation
    dt = parse_datetime(message)
    if dt:
        appt = Appointment.objects.filter(
            lead__phone=phone,
            scheduled_for__isnull=True
        ).last()

        if appt:
            appt.scheduled_for = dt
            appt.confirmed = True
            appt.save()
            return f"✅ Appointment confirmed for {dt.strftime('%Y-%m-%d %H:%M')}"

        return "⚠️ I couldn’t find a pending appointment request."

    # 6️⃣ HOT lead alert
    if status == 'HOT':
        try:
            send_hot_lead(phone, message)
        except Exception:
            pass  # never crash WhatsApp flow

    # 7️⃣ AI fallback (never crash)
    try:
        reply = get_ai_reply(message)
        if reply:
            return reply
    except Exception:
        pass

    return "🤖 I’m here to help. Could you please rephrase that?"
