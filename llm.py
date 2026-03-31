from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.openai_api_key)


def ask_llm(prompt: str) -> str:
    response = client.responses.create(
        model=settings.model_name,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a strict JSON generator.\n"
                            "You MUST return ONLY valid JSON.\n"
                            "No explanations. No markdown. No text outside JSON.\n"
                            "If unsure, still return valid JSON."
                        )
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt}
                ],
            },
        ],
    )

    return response.output_text.strip()