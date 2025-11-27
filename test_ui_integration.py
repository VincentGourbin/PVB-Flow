#!/usr/bin/env python
"""
Test script to verify UI integration and URL generation.
"""
from src.pvb_flow.ui.handlers import handle_open_mermaid_chart

# Test with a simple diagram
test_diagram = """flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E

    style A fill:#4A90D9
    style B fill:#4A90D9
    style C fill:#50C878
    style D fill:#FF9F43
    style E fill:#E74C3C
"""

print("=" * 80)
print("Testing UI Integration")
print("=" * 80)
print()

# Test URL generation
url = handle_open_mermaid_chart(test_diagram)

if url:
    print("✅ URL Generation: SUCCESS")
    print()
    print("Generated URL (first 100 chars):")
    print(url[:100] + "...")
    print()
    print(f"Full URL length: {len(url)} characters")
    print()
    print("Expected behavior:")
    print("  1. User clicks '🔗 Open in Mermaid Chart' button")
    print("  2. Python handler generates this URL")
    print("  3. JavaScript receives URL and calls window.open(url, '_blank')")
    print("  4. New tab opens with MermaidChart.com playground")
    print("  5. Diagram is loaded and ready to edit/export")
else:
    print("❌ URL Generation: FAILED")
    print("No URL generated")

print()
print("=" * 80)

# Test with empty diagram
print()
print("Testing with empty diagram...")
empty_url = handle_open_mermaid_chart("")

if not empty_url:
    print("✅ Empty diagram handling: SUCCESS (returns empty string)")
else:
    print("❌ Empty diagram handling: FAILED (should return empty string)")

print()
print("=" * 80)
print("All integration tests completed!")
print("=" * 80)
