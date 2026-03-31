from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    bitgn_api_key: str = os.getenv("BITGN_API_KEY", "")
    bitgn_base_url: str = os.getenv("BITGN_BASE_URL", "")
    max_steps: int = 12
    stagnation_limit: int = 3


settings = Settings()