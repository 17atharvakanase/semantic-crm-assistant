import json
from llm import client


def build_semantic_memory(sample_df):
    """
    Uses an LLM to infer business semantics from CRM data.

    Args:
        sample_df (pd.DataFrame): Sample CRM records.

    Returns:
        dict: Semantic memory.
    """

    prompt = f"""
You are an AI system responsible for building a semantic translation layer for a CRM.

CRM Schema:
- assigned_to
- internal_status
- priority_tag
- region
- dealstage

Sample CRM Records:

{sample_df.to_markdown(index=False)}

Your tasks:

1. Identify which field represents the deal owner.
2. Identify which field represents the deal status.
3. Infer owner aliases.
   Example:
   Amit:
   - A
   - A Sharma
   - Amit S
   - A K

4. Categorize statuses into:
   - open
   - closed

5. Infer any business rules from the data.

6. Assign confidence scores between 0 and 1.

Return ONLY valid JSON.

Output format:

{{
  "owner_field": "",
  "status_field": "",
  "priority_field": "",
  "region_field": "",
  "owner_aliases": {{
      "Canonical Name": ["alias1","alias2"]
  }},
  "status_groups": {{
      "open": [],
      "closed": []
  }},
  "business_rules": [],
  "confidence": {{
      "owner_aliases": 0.0,
      "status_groups": 0.0
  }}
}}

Do not return markdown.
Do not explain outside JSON.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.7-flash",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in CRM semantic modeling. "
                    "Always return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        semantic_memory = json.loads(content)

    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        )

    return semantic_memory