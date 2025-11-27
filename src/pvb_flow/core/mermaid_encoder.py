"""
Encode Mermaid diagrams for Mermaid Live Editor URLs.

Format: JSON state with zlib compression + base64url encoding.
Based on: Claude Desktop MCP implementation for Mermaid Live Editor.
"""
import zlib
import base64
import json


def encode_mermaid_for_url(mermaid_code: str) -> str:
    """
    Encode Mermaid diagram code for Mermaid Live Editor URL.

    Uses the official Mermaid Live Editor format:
    1. Wrap code in JSON state object
    2. Compress with zlib.compress (level 9, WITH header)
    3. Base64url encode (+ → -, / → _, remove =)

    Based on Claude Desktop MCP implementation for Mermaid Live Editor.

    Args:
        mermaid_code: Raw Mermaid diagram code

    Returns:
        Base64URL encoded string suitable for URL fragment
    """
    if not mermaid_code or not mermaid_code.strip():
        return ""

    # Create state object as per Mermaid Live Editor format
    state = {
        "code": mermaid_code,
        "mermaid": {
            "theme": "default"
        },
        "autoSync": True,
        "updateDiagram": True
    }

    # Convert to JSON string
    state_json = json.dumps(state)

    # Encode to bytes
    state_bytes = state_json.encode('utf-8')

    # Compress using zlib.compress() with header (level 9, maximum compression)
    # This matches the Claude Desktop MCP implementation
    compressed = zlib.compress(state_bytes, level=9)

    # Base64url encode (URL-safe variant)
    # urlsafe_b64encode automatically does: + → -, / → _
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')

    # Remove trailing = padding
    base64url = encoded.rstrip('=')

    return base64url


def generate_mermaid_chart_url(mermaid_code: str) -> str:
    """
    Generate a complete Mermaid Live Editor URL.

    Args:
        mermaid_code: Raw Mermaid diagram code

    Returns:
        Full URL to Mermaid Live Editor with encoded diagram
    """
    if not mermaid_code or not mermaid_code.strip():
        return ""

    encoded = encode_mermaid_for_url(mermaid_code)

    # Use Mermaid Live Editor (official editor that works with pako encoding)
    url = f"https://mermaid.live/edit#pako:{encoded}"

    return url
