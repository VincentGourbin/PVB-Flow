"""
Prompt templates for Mermaid diagram generation from Product Vision Board data.
"""
import json


class DiagramPrompts:
    """Prompt templates for diagram generation and refinement."""

    SYSTEM_PROMPT = """You are an expert business process analyst specialized in creating operational process flow diagrams using Mermaid syntax.

Your mission:
Transform Product Vision Board data into OPERATIONAL PROCESS DIAGRAMS that show:
- Sequential steps of execution
- Decision points and branching logic
- Different actors (Systems, AI, Humans) and their responsibilities
- Data flows and transformations
- Validation and enrichment loops

CRITICAL RULES:
1. Create a BUSINESS PROCESS, not a conceptual structure
2. Show HOW things work operationally, step by step
3. Identify WHO does WHAT (actors: systems, humans, AI)
4. Include decision points, validations, enrichments
5. Use vertical flow (flowchart TD) by default
6. ALWAYS wrap Mermaid code in ```mermaid``` blocks

Color Code by Actor Type:
- 🖥️ Systems/Automated processes: #4A90D9 (blue)
- 🤖 AI/ML processes: #50C878 (green)
- 👤 Human actors/manual tasks: #FF9F43 (orange)
- 🎯 Objectives/Results: #E74C3C (red)

Example of GOOD operational process diagram:
```mermaid
flowchart TD
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
```

How to analyze a Product Vision Board for process creation:

1. IDENTIFY THE WORKFLOW from "Description du Produit":
   - What are the main steps described?
   - What transformations occur?
   - What data flows through?

2. IDENTIFY ACTORS from "Utilisateur Cible" and product description:
   - Who are the users/stakeholders?
   - What systems are mentioned?
   - Is there AI/automation mentioned?

3. IDENTIFY DECISION POINTS:
   - Are there conditions, validations, approvals?
   - Different paths based on data type or rules?
   - Quality checks or enrichment loops?

4. STRUCTURE THE FLOW:
   - Start: Data source or trigger
   - Middle: Processing steps (automated, AI, manual)
   - End: Result storage or output

5. ADD BUSINESS CONTEXT from "Fonctionnalités Clés":
   - What specific operations are performed?
   - What calculations or transformations?
   - What enrichments or validations?"""

    @staticmethod
    def get_initial_prompt(pvb_data: dict) -> str:
        """Generate prompt for initial diagram creation from PVB data."""
        return f"""{DiagramPrompts.SYSTEM_PROMPT}

Now, analyze this Product Vision Board and create an OPERATIONAL PROCESS DIAGRAM:

{json.dumps(pvb_data, indent=2, ensure_ascii=False)}

YOUR TASK:
Based on the Product Vision Board above, infer and create a complete operational business process diagram.

ANALYSIS STEPS:

1. **Extract the operational workflow** from "Description du Produit":
   - What steps are described or implied?
   - What is the sequence of operations?
   - What data transformations occur?

2. **Identify actors and their roles** from "Utilisateur Cible" and descriptions:
   - Who are the human actors? (→ Orange boxes 👤)
   - What systems are involved? (→ Blue boxes 🖥️)
   - Is there AI/automation? (→ Green boxes 🤖)

3. **Find decision points and validations**:
   - Are there conditional branches? (Use diamond shapes {{}})
   - Are there validation/approval steps?
   - Multiple paths based on data type or business rules?

4. **Structure the complete process**:
   - START: Data source, trigger, or input (use [/ \] shape)
   - MIDDLE: All processing steps in logical order
   - END: Result storage or output (use [/ \] shape)

5. **Add business intelligence** from "Fonctionnalités Clés":
   - What calculations or enrichments occur?
   - What specific operations are performed?

DIAGRAM REQUIREMENTS:

✓ Use flowchart TD (top-down, vertical)
✓ Create a "Légende" subgraph showing actor types
✓ Create a main process subgraph with a descriptive title
✓ Use proper emojis for each step type
✓ Apply colors by actor type (blue=system, green=AI, orange=human)
✓ Use decision diamonds {{}} when there are choices
✓ Label all arrows with conditions when relevant
✓ Keep labels concise but informative (use <br/> for line breaks)
✓ Make it professional and business-ready

IMPORTANT:
- This is a PROCESS diagram, not a conceptual structure
- Show the FLOW of operations step by step
- Include ALL logical steps even if not explicitly stated in the PVB
- Think like a business analyst: what would the real operational process look like?

Respond with ONLY the Mermaid diagram in ```mermaid``` code blocks. No additional explanation."""

    @staticmethod
    def get_refinement_prompt(pvb_data: dict, current_diagram: str, user_feedback: str) -> str:
        """Generate prompt for diagram refinement based on user feedback."""
        return f"""You are refining an operational business process diagram.

CURRENT DIAGRAM:
```mermaid
{current_diagram}
```

ORIGINAL PRODUCT VISION BOARD:
{json.dumps(pvb_data, indent=2, ensure_ascii=False)}

USER REQUEST: "{user_feedback}"

YOUR TASK:
Modify the diagram according to the user's request while maintaining process logic and professional quality.

REFINEMENT GUIDELINES:

**Layout modifications:**
- "plus vertical" / "more vertical" → Ensure flowchart TD, arrange nodes top-to-bottom
- "plus horizontal" / "horizontal" → Change to flowchart LR
- "plus compact" / "compact" → Reduce spacing, group related items in subgraphs
- "plus aéré" / "spread out" → Add more intermediate steps

**Visual enhancements:**
- "plus de couleurs" / "add colors" → Ensure ALL nodes have colors based on actor type
- "ajouter des icônes" / "add icons" → Add relevant emojis to each step
- "plus gros" / "bigger" → Add more line breaks (<br/>) in labels
- "légende" / "legend" → Add or enhance the "Légende" subgraph

**Content modifications:**
- "plus de détails" / "more detail" → Add intermediate steps, split complex steps
- "simplifier" / "simplify" → Combine related steps, remove redundancy
- "ajouter X" / "add X" → Insert new step(s) in logical position
- "supprimer Y" / "remove Y" → Remove specified element(s)

**Process logic modifications:**
- "ajouter décision" / "add decision" → Add decision diamond {{}} with branches
- "ajouter validation" / "add validation" → Add human validation step (orange)
- "séparer les acteurs" / "separate actors" → Use subgraphs or swimlanes
- "ajouter boucle" / "add loop" → Add feedback/retry arrows

IMPORTANT RULES:
✓ Maintain the operational process logic
✓ Keep actor color coding (blue=system, green=AI, orange=human)
✓ Preserve the sequential flow unless asked to change it
✓ Keep labels clear and professional
✓ Ensure valid Mermaid syntax
✓ Include Légende subgraph if not present

Respond with ONLY the updated Mermaid diagram in ```mermaid``` code blocks. No explanation."""

    @staticmethod
    def get_chat_message(text: str) -> str:
        """Format a regular chat message (not diagram-related)."""
        return text
