# llmchat/views.py
import os
import re
from typing import List

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from groq import Groq

# --- simple rule-based filter -------------------------------------------------

PC_KEYWORDS: List[str] = [
    # components
    "cpu", "processor", "gpu", "graphics card", "video card", "motherboard",
    "ram", "memory", "psu", "power supply", "ssd", "hdd", "cooler", "aio",
    "case", "chassis", "pc case", "thermal paste", "fan", "heatsink",
    "monitor", "display", "keyboard", "mouse",
    # platforms/compat
    "am4", "am5", "lga", "intel", "amd", "ryzen", "core i3", "i5", "i7", "i9",
    "xmp", "expo", "pcie", "ddr4", "ddr5",
    # actions/topics
    "pc build", "build a pc", "bottleneck", "compatibility", "overclock",
    "undervolt", "benchmark", "frames", "fps", "thermals", "temps", "power draw",
    "wattage", "budget build", "gaming pc", "workstation", "itx", "atx", "micro atx",
    # local context
    "bdt", "bangladesh", "startech", "techland", "ryans"
]

PC_RE = re.compile(r"|".join(re.escape(k) for k in PC_KEYWORDS), re.IGNORECASE)


def is_pc_related(text: str) -> bool:
    """Very fast heuristic gate to avoid unnecessary LLM calls."""
    if not text:
        return False
    return bool(PC_RE.search(text))


# --- view --------------------------------------------------------------------

class LLMChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = (request.data.get("message") or "").strip()
        if not user_message:
            return Response({"error": "No message provided."}, status=400)

        # Hard gate: if message doesn't look PC-related, refuse immediately
        if not is_pc_related(user_message):
            return Response({
                "response": (
                    "I am sorry but I can only help with PC building and components. Ask me something in that domain!"
                )
            }, status=200)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return Response(
                {"error": "GROQ_API_KEY not configured."},
                status=500,
            )

        try:
            client = Groq(api_key=api_key)

            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a **strict PC building assistant**. "
                            "You must ONLY answer questions about desktop PC components and PC builds: "
                            "If the user asks anything outside PC hardware/building, politely refuse and redirect them to PC topics. "
                            "DO NOT engage in any other topics. "
                            "CPUs/GPUs/RAM/motherboards/PSUs/cases/SSDs, compatibility (sockets, chipsets, DDR4/DDR5, PCIe), "
                            "thermals, wattage, performance tiers, and price/performance recommendations "
                            "(especially for Bangladesh retailers like Startech, Techland, and Ryans). "
                            "Be concise, practical, and include concrete part suggestions and reasoning. "
                            "When budgets are in BDT, assume Bangladesh market context."
                        ),
                    },
                    {"role": "user", "content": user_message},
                ],
                temperature=0.6,
                max_tokens=800,
                top_p=1,
            )

            reply = completion.choices[0].message.content
            # Safety net: if model goes off-topic, wrap it
            if not is_pc_related(reply):
                reply = (
                    "Let's keep it to PC building and components. "
                    "Tell me your budget, and PC preferences."
                )

            return Response({"response": reply})

        except Exception as e:
            return Response(
                {"error": f"Failed to get AI response: {e}"},
                status=500,
            )
