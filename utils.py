import json

def extract_json_from_text(text: str) -> dict:
    """Extract JSON from text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        new_text = '\n'.join(text.split("\n")[1:-1])
        try:
            return json.loads(new_text)
        except json.JSONDecodeError:
            return {}