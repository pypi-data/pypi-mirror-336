import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional
from together import Together, AsyncTogether

PATH_TO_DOTENV = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=PATH_TO_DOTENV)


# Initialize optional OpenAI client
client: Optional['OpenAI'] = None
if os.getenv("OPENAI_API_KEY"):
    try:
        from openai import OpenAI
        client = OpenAI()
    except ImportError:
        # openai package not installed
        pass
    
# Initialize optional Together clients
together_client: Optional['Together'] = None
async_together_client: Optional['AsyncTogether'] = None

# Only initialize Together clients if API key is available
if os.getenv("TOGETHERAI_API_KEY"):
    try:
        together_client = Together(api_key=os.getenv("TOGETHERAI_API_KEY"))
        async_together_client = AsyncTogether(api_key=os.getenv("TOGETHERAI_API_KEY"))
    except Exception:
        pass

