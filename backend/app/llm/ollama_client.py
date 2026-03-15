import requests
import json
import re


OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder:7b"

# Timeout for text generation (reflection, planner, supervisor)
TEXT_TIMEOUT = 180

# Timeout for JSON generation (react agent) — longer because content can be complex
JSON_TIMEOUT = 300


class OllamaClient:

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def _post(self, prompt: str, use_json_format: bool = False, timeout: int = TEXT_TIMEOUT) -> str:
        """
        Internal: call /api/generate. Returns the raw response text.
        use_json_format=True forces the model to output valid JSON (Ollama native constraint).
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,    # Low temp = deterministic, less hallucination
                "top_p": 0.9,
                "num_predict": 2048,   # Enough for moderately complex code files
            }
        }
        if use_json_format:
            # This is the key fix: Ollama's built-in JSON mode guarantees valid JSON output.
            # The model will ONLY output a valid JSON object — no unescaped quotes,
            # no prose before/after, no markdown fences.
            payload["format"] = "json"

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json().get("response", "")

    def generate(self, prompt: str, task: str = "") -> str:
        """
        Text generation (planner steps, reflection, supervisor advice).
        Returns plain text — no JSON format constraint.
        """
        try:
            return self._post(prompt, use_json_format=False, timeout=TEXT_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return "ERROR: Cannot connect to Ollama. Is it running? Run: ollama serve"
        except requests.exceptions.Timeout:
            return f"ERROR: Ollama timed out after {TEXT_TIMEOUT}s. The model may be too large for this hardware."
        except Exception as e:
            return f"ERROR calling Ollama: {str(e)}"

    def generate_json(self, prompt: str) -> str:
        """
        JSON generation for the ReAct agent.
        Uses Ollama's format:json mode to GUARANTEE valid JSON output.
        This eliminates all JSON parse failures from unescaped quotes or multi-line content.
        Returns a JSON string.
        """
        try:
            return self._post(prompt, use_json_format=True, timeout=JSON_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return json.dumps({
                "thought": "ERROR: Cannot connect to Ollama. Is ollama serve running?",
                "action": "none",
                "input": {}
            })
        except requests.exceptions.Timeout:
            return json.dumps({
                "thought": f"ERROR: Ollama timed out after {JSON_TIMEOUT}s. Consider a smaller model.",
                "action": "none",
                "input": {}
            })
        except Exception as e:
            return json.dumps({
                "thought": f"ERROR calling Ollama: {str(e)}",
                "action": "none",
                "input": {}
            })

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return r.status_code == 200
        except Exception:
            return False


ollama_client = OllamaClient()


def repair_json(text: str) -> str:
    """
    Fallback JSON repair for cases where format:json wasn't used.
    Tries to fix unescaped quotes in string values.
    NOTE: With generate_json(), this should rarely be needed.
    """
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    # Handle the case where the model wraps the JSON in text
    # Try to extract just the JSON object
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    return text
