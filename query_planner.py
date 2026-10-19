import json
from llm import client


def generate_query_plan(question, semantic_memory):
    """
    Converts a natural language question into a structured execution plan.

    Args:
        question (str): User's question.
        semantic_memory (dict): Business semantic memory.

    Returns:
        dict: Structured execution plan.
    """

    planner_prompt = f"""
You are a Query Planner for a CRM Semantic Translation Layer.

You are given:

1. Semantic Memory (business understanding of the CRM)
2. A user's natural language question

Your ONLY responsibility is to convert the user's question into a structured execution plan.

DO NOT answer the question.
DO NOT perform any calculations.
DO NOT resolve aliases.
DO NOT translate business concepts into CRM field names or values.

Semantic Memory:

{json.dumps(semantic_memory, indent=2)}

User Question:

"{question}"

Return ONLY valid JSON in the following format:

{{
    "intent": "",
    "entity": "deals",
    "aggregation": "",
    "filters": {{}}
}}

Rules:

1. Intent must be one of:
   - count
   - list
   - summarize
   - group_by

2. Aggregation must be one of:
   - count
   - none

3. Filters must use BUSINESS CONCEPTS only.

Valid business concepts:
- owner
- status
- priority
- region

4. NEVER use CRM field names such as:
- assigned_to
- internal_status
- priority_tag
- dealstage

5. Preserve the user's wording whenever possible.

Examples:

Question:
How many open deals does Amit own?

Output:

{{
    "intent": "count",
    "entity": "deals",
    "aggregation": "count",
    "filters": {{
        "owner": "Amit",
        "status": "open"
    }}
}}

Question:
Show all high priority deals in the West region.

Output:

{{
    "intent": "list",
    "entity": "deals",
    "aggregation": "none",
    "filters": {{
        "priority": "High",
        "region": "West"
    }}
}}

Return ONLY valid JSON.
Do not include markdown.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.7-flash",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert CRM questions into execution plans. "
                    "Always return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": planner_prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        plan = json.loads(content)

    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        )

    return plan