"""
JSON validation utilities for Product Vision Board data.
"""
import json
from typing import Tuple, Dict, Optional


class PVBValidator:
    """Validates and parses Product Vision Board JSON data."""

    # Expected sections in a Product Vision Board
    EXPECTED_SECTIONS = [
        "1. Utilisateur Cible",
        "2. Description du Produit",
        "3. Fonctionnalités Clés",
        "4. Enjeux et Indicateurs"
    ]

    @staticmethod
    def validate_pvb_json(user_input: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Validate if the user input is valid Product Vision Board JSON.

        Args:
            user_input: String that might be JSON

        Returns:
            Tuple of (is_valid, parsed_data, error_message)
        """
        # Try to parse as JSON
        try:
            data = json.loads(user_input)
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON format: {str(e)}"

        # Check if it's a dictionary
        if not isinstance(data, dict):
            return False, None, "JSON must be an object/dictionary, not an array or primitive"

        # Check for at least some expected sections
        found_sections = [section for section in PVBValidator.EXPECTED_SECTIONS if section in data]

        if len(found_sections) == 0:
            # Not a PVB, might be a regular JSON
            return False, None, "No Product Vision Board sections found"

        # Validate that sections contain lists
        for section in found_sections:
            if not isinstance(data[section], list):
                return False, None, f"Section '{section}' must be a list"

        # Valid PVB JSON
        return True, data, None

    @staticmethod
    def is_pvb_like(user_input: str) -> bool:
        """
        Quick check if input looks like PVB JSON (without full validation).

        Args:
            user_input: User input string

        Returns:
            True if it looks like PVB JSON
        """
        # Check if it starts with { and contains at least one expected section
        if not user_input.strip().startswith("{"):
            return False

        for section in PVBValidator.EXPECTED_SECTIONS:
            if section in user_input:
                return True

        return False

    @staticmethod
    def extract_summary(pvb_data: Dict) -> str:
        """
        Extract or generate a summary from PVB data.

        Args:
            pvb_data: Parsed PVB dictionary

        Returns:
            Summary string
        """
        if "Summary" in pvb_data:
            return pvb_data["Summary"]

        # Generate basic summary from sections
        summary_parts = []
        if "1. Utilisateur Cible" in pvb_data:
            users = pvb_data["1. Utilisateur Cible"]
            summary_parts.append(f"Target users: {', '.join(users)}")

        if "4. Enjeux et Indicateurs" in pvb_data:
            objectives = pvb_data["4. Enjeux et Indicateurs"]
            if objectives:
                summary_parts.append(f"Key objective: {objectives[0]}")

        return " | ".join(summary_parts) if summary_parts else "Product Vision Board"


# Convenience functions
def validate_pvb_json(user_input: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """Shorthand for PVBValidator.validate_pvb_json()"""
    return PVBValidator.validate_pvb_json(user_input)


def is_pvb_like(user_input: str) -> bool:
    """Shorthand for PVBValidator.is_pvb_like()"""
    return PVBValidator.is_pvb_like(user_input)
