from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .whatsapp import process_message
import traceback

@csrf_exempt
def whatsapp_webhook(request):
    try:
        phone = request.POST.get('From')
        body = request.POST.get('Body')
        if not body:
            resp = MessagingResponse()
            resp.message("👋 Carlflow_AI is online. How can I help you today?")
            return HttpResponse(str(resp))

        reply = process_message(phone, body)

        resp = MessagingResponse()
        resp.message(reply)
        return HttpResponse(str(resp))

    except Exception as e:
        print("🔥 WHATSAPP WEBHOOK ERROR 🔥")
        traceback.print_exc()

        resp = MessagingResponse()
        resp.message(
            "⚠️ Carlflow_AI is temporarily unavailable. Please try again shortly."
        )
        return HttpResponse(str(resp))
