import re

def detect_persona(message: str) -> str:
    message = message.lower()

    if re.search(r"\b(api|code|error|debug|json|server|script|deploy|integration)\b", message):
        return "technical expert"
    elif re.search(r"\b(fix|angry|not working|issue|problem|why|urgent)\b", message):
        return "frustrated user"
    elif re.search(r"\b(cost|pricing|ROI|contract|budget|client)\b", message):
        return "business exec"
    else:
        return "general user"
