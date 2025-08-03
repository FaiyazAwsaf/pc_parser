# llmchat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.http import StreamingHttpResponse
from .serializers import ChatPromptSerializer

from groq import Groq


class LLMChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "No message provided."}, status=400)

        # Call Groq LLM as before
        client = Groq()
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": user_message}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
        )
        reply = ""
        for chunk in completion:
            reply += chunk.choices[0].delta.content or ""
        return Response({"response": reply})
