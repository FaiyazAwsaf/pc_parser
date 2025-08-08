# llmchat/views.py

import os
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

        try:
            # Initialize Groq client with API key from environment
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return Response({
                    "error": "GROQ_API_KEY not configured. Please add it to your environment variables."
                }, status=500)
            
            client = Groq(api_key=api_key)
            
            # Create completion with proper error handling
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",  # Using a more stable model
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a PC building assistant. Help users build computers by recommending components, explaining compatibility, and providing advice on PC builds within their budget. Focus on practical, actionable advice."
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
            )
            
            # Extract the response
            reply = completion.choices[0].message.content
            return Response({"response": reply})
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error calling Groq API: {str(e)}")
            print(f"Full traceback: {error_details}")
            return Response({
                "error": f"Failed to get AI response: {str(e)}",
                "details": error_details if os.getenv('DEBUG') == 'True' else None
            }, status=500)