"""
Utilities for extracting and validating Mermaid diagrams from LLM responses.
"""
import re
from typing import Tuple, Optional


class MermaidExtractor:
    """Extracts and validates Mermaid code from text."""

    @staticmethod
    def extract_mermaid_code(llm_response: str) -> Tuple[Optional[str], bool]:
        """
        Extract Mermaid code from LLM response.

        Args:
            llm_response: Full response from the LLM

        Returns:
            Tuple of (mermaid_code, is_valid)
        """
        # Pattern to match ```mermaid ... ```
        pattern = r'```mermaid\n(.*?)\n```'
        match = re.search(pattern, llm_response, re.DOTALL)

        if match:
            code = match.group(1).strip()
            is_valid, _ = MermaidExtractor.validate_mermaid_syntax(code)
            return code, is_valid

        return None, False

    @staticmethod
    def validate_mermaid_syntax(code: str) -> Tuple[bool, str]:
        """
        Basic Mermaid syntax validation.

        Args:
            code: Mermaid diagram code

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Empty Mermaid code"

        # Check for diagram type declaration
        diagram_types = ['flowchart', 'graph', 'sequenceDiagram', 'classDiagram',
                        'stateDiagram', 'erDiagram', 'gantt', 'pie']

        has_diagram_type = any(dtype in code for dtype in diagram_types)
        if not has_diagram_type:
            return False, "Missing diagram type declaration (flowchart, graph, etc.)"

        # Check for connections (common syntax)
        connection_patterns = ['-->', '->', '---', '-.->', '==>','-.->']
        has_connections = any(conn in code for conn in connection_patterns)

        if not has_connections:
            return False, "No connections found in diagram"

        # Check for at least one node definition
        # Nodes are typically: ID[Label] or ID(Label) or ID{Label}
        node_pattern = r'[A-Z]\d*[\[\(\{]'
        if not re.search(node_pattern, code):
            return False, "No nodes defined in diagram"

        return True, "Valid Mermaid syntax"

    @staticmethod
    def format_for_display(mermaid_code: str, assistant_text: str = None) -> str:
        """
        Format Mermaid code for Gradio display.
        Gradio v6 automatically renders Mermaid in chatbot.

        Args:
            mermaid_code: The Mermaid diagram code
            assistant_text: Optional explanatory text from the assistant

        Returns:
            Formatted string with Mermaid code block
        """
        response = ""
        if assistant_text:
            response += assistant_text + "\n\n"
        response += f"```mermaid\n{mermaid_code}\n```"
        return response

    @staticmethod
    def extract_all_mermaid_blocks(text: str) -> list[str]:
        """
        Extract all Mermaid code blocks from text (if multiple exist).

        Args:
            text: Text potentially containing multiple Mermaid blocks

        Returns:
            List of Mermaid code strings
        """
        pattern = r'```mermaid\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches]


# Convenience functions
def extract_mermaid_code(llm_response: str) -> Tuple[Optional[str], bool]:
    """Shorthand for MermaidExtractor.extract_mermaid_code()"""
    return MermaidExtractor.extract_mermaid_code(llm_response)


def validate_mermaid_syntax(code: str) -> Tuple[bool, str]:
    """Shorthand for MermaidExtractor.validate_mermaid_syntax()"""
    return MermaidExtractor.validate_mermaid_syntax(code)


def format_for_display(mermaid_code: str, assistant_text: str = None) -> str:
    """Shorthand for MermaidExtractor.format_for_display()"""
    return MermaidExtractor.format_for_display(mermaid_code, assistant_text)
