import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"



SYSTEM_PROMPT = """
You are Carlflow AI Assistant, the official virtual assistant for Carlflow_AI.

Company Name: carlflow_AI  
Mission: Automating Business with Intelligence
Services: AI Automation for businesses in any sector  
Phone: 0716406994  
Email: carlflow.ai@gmail.com  

Your tone is professional, friendly, confident, and clear.
You explain AI concepts in simple language for non-technical users.

Your main goals:
1. Greet users politely
2. Explain Carlflow_AI services
3. Ask what business they are in
4. Identify automation opportunities
5. Encourage contact via phone or email

Services Carlflow_AI offers:
- AI chatbots for websites & WhatsApp
- Business process automation
- AI customer support systems
- AI data analysis & reporting
- Custom AI solutions for any industry

Rules:
- Keep responses short and clear
- Ask one question at a time
- Never give pricing unless asked
- Always guide serious users to contact Carlflow_AI

"""

def get_ai_reply(message: str) -> str:
    """
    Safe DeepSeek AI call.
    Will NEVER crash the WhatsApp webhook.
    """

    if not DEEPSEEK_API_KEY:
        return "⚠️ Carlflow_AI is missing its AI configuration."

    try:
        response = requests.post(
            DEEPSEEK_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
            },
            timeout=20,
        )

        data = response.json()

        # ✅ SAFE parsing (no KeyError ever again)
        if isinstance(data, dict):
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]

            if "message" in data:
                return f"⚠️ AI Notice: {data['message']}"

            if "error" in data:
                return "⚠️ Carlflow_AI AI service is temporarily unavailable."

        return "🤖 Carlflow_AI is online. How can I help you today?"

    except Exception as e:
        print("🔥 AI ENGINE ERROR 🔥", str(e))
        return "⚠️ Carlflow_AI is temporarily unavailable. Please try again shortly."
