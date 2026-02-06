import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """
You are Carlflow AI Assistant, the official virtual assistant for Carlflow_AI.

Company Name: Carlflow_AI
Mission: Automating Business with Intelligence
Services: AI Automation for businesses in any sector
Operating Hours: 24/7
Phone: 0716406994
Email: carlflow.ai@gmail.com

Tone:
Professional, friendly, confident, and clear.
Explain AI in simple, non-technical language.

Goals:
1. Greet users politely
2. Explain Carlflow_AI services
3. Ask what business they are in
4. Identify automation opportunities
5. Encourage contact via phone or email

Rules:
- Keep responses short
- Ask one question at a time
- Never give pricing unless asked
- Always guide serious users to contact Carlflow_AI
"""

def get_ai_reply(message: str) -> str:
    """
    DeepSeek AI – hardened for WhatsApp production use.
    NEVER crashes webhook.
    """

    if not message:
        return "👋 Hi! How can Carlflow_AI help you today?"

    if not DEEPSEEK_API_KEY:
        return "⚠️ AI service is not configured."

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
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "temperature": 0.4,
            },
            timeout=15,
        )

        # 🔒 Never trust external APIs
        try:
            data = response.json()
        except Exception:
            return "⚠️ AI service returned an invalid response."

        # ✅ Expected success response
        if (
            isinstance(data, dict)
            and "choices" in data
            and isinstance(data["choices"], list)
            and len(data["choices"]) > 0
            and "message" in data["choices"][0]
        ):
            return data["choices"][0]["message"]["content"]

        # ⚠️ Known DeepSeek fallback responses
        if "error" in data:
            return "⚠️ AI service is temporarily busy. Please try again."

        if "message" in data:
            return "🤖 Carlflow_AI is online. How can I help you?"

        # Final fallback
        return "🤖 Carlflow_AI is ready to assist you."

    except requests.exceptions.Timeout:
        return "⚠️ AI response took too long. Please try again."

    except Exception as e:
        print("🔥 AI ENGINE ERROR 🔥", str(e))
        return "⚠️ Carlflow_AI AI service is temporarily unavailable."
