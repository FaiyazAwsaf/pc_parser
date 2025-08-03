from django.urls import path
from .views import LLMChatView

urlpatterns = [
    path("llmchat/", LLMChatView.as_view(), name="llm-chat"),
]
