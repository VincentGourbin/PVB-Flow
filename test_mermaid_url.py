#!/usr/bin/env python
"""
Test script to verify MermaidChart URL generation.
"""
from src.pvb_flow.core.mermaid_encoder import generate_mermaid_chart_url

# Test with a realistic business process diagram
test_diagram = """flowchart TD
    subgraph Légende
        L1[🖥️ Système]
        L2[🤖 IA]
        L3[👤 Humain]
    end

    subgraph Process["Processus de Traitement"]
        A[/"📊 Source de Données<br/>Extraction initiale"/]

        B{{"Type de<br/>données ?"}}

        C1["📁 Système A<br/>Récupération fichiers"]
        C2["📁 Système B<br/>Récupération fichiers"]

        D["🤖 Analyse IA<br/>Extraction informations"]

        E["👤 Validation Humaine<br/>Enrichissement données"]

        F["⚙️ Calcul Automatique<br/>Application règles métier"]

        G["👤 Validation Finale<br/>Contrôle qualité"]

        H[/"📊 Base de Données<br/>Intégration résultats"/]
    end

    A --> B
    B -->|"Type 1"| C1
    B -->|"Type 2"| C2
    C1 --> D
    C2 --> D
    D --> E
    E --> F
    F --> G
    G --> H

    style A fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style B fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style C1 fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style C2 fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style D fill:#50C878,stroke:#2E8B57,color:#fff
    style E fill:#FF9F43,stroke:#E67E22,color:#fff
    style F fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style G fill:#FF9F43,stroke:#E67E22,color:#fff
    style H fill:#4A90D9,stroke:#2E5F8A,color:#fff

    style L1 fill:#4A90D9,stroke:#2E5F8A,color:#fff
    style L2 fill:#50C878,stroke:#2E8B57,color:#fff
    style L3 fill:#FF9F43,stroke:#E67E22,color:#fff
"""

if __name__ == "__main__":
    print("=" * 80)
    print("Testing MermaidChart URL Generation")
    print("=" * 80)
    print()

    # Generate URL
    url = generate_mermaid_chart_url(test_diagram)

    print("✅ URL Generated Successfully!")
    print()
    print("📋 Copy this URL and paste it in your browser:")
    print()
    print(url)
    print()
    print("=" * 80)
    print("The diagram will open in MermaidChart.com playground where you can:")
    print("  • View the rendered diagram")
    print("  • Edit the diagram code")
    print("  • Export as PNG/SVG")
    print("  • Share with others")
    print("=" * 80)
