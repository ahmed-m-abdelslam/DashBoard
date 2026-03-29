from config import GROQ_API_KEY

groq_client = None

if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except ImportError:
        print("Warning: groq package not installed. AI features disabled.")
    except Exception as e:
        print(f"Warning: Failed to initialize Groq client: {e}")


def is_ai_available():
    return groq_client is not None
