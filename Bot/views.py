from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .whatsapp import process_message
import traceback


@csrf_exempt
def whatsapp_webhook(request):
    resp = MessagingResponse()

    try:
        # 1️⃣ Handle non-POST requests safely
        if request.method != "POST":
            resp.message("🤖 Carlflow_AI WhatsApp bot is running.")
            return HttpResponse(str(resp))

        # 2️⃣ Extract Twilio fields
        phone = request.POST.get("From", "").strip()
        body = request.POST.get("Body", "").strip()

        # 3️⃣ Handle empty messages (Twilio pings, delivery receipts)
        if not phone or not body:
            resp.message("👋 Carlflow_AI is online. How can I help you today?")
            return HttpResponse(str(resp))

        # 4️⃣ Process message
        reply = process_message(phone, body)

        # 5️⃣ Fallback if AI / logic returns nothing
        if not reply:
            reply = "🤖 I’m here to help. Please tell me what you need."

        resp.message(reply)
        return HttpResponse(str(resp))

    except Exception:
        print("🔥 WHATSAPP WEBHOOK ERROR 🔥")
        traceback.print_exc()

        resp.message(
            "⚠️ Carlflow_AI is temporarily unavailable. Please try again shortly."
        )
        return HttpResponse(str(resp))
