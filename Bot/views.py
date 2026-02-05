from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .whatsapp import process_message

@csrf_exempt
def whatsapp_webhook(request):
    phone = request.POST.get('From')
    body = request.POST.get('Body')

    reply = process_message(phone, body)

    resp = MessagingResponse()
    resp.message(reply)
    return HttpResponse(str(resp))