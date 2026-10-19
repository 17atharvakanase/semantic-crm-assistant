import json
from llm import client


def generate_human_response(
    question,
    plan,
    resolved_filters,
    filtered_df
):
    """
    Generates a natural language response from the
    execution results.

    Args:
        question (str)
        plan (dict)
        resolved_filters (dict)
        filtered_df (pd.DataFrame)

    Returns:
        str
    """

    execution_result = {
        "records_found": len(filtered_df),
        "execution_plan": plan,
        "semantic_translation": resolved_filters
    }

    prompt = f"""
You are a helpful CRM assistant.

The user's question has ALREADY been executed.

Question:
{question}

Execution Result:

{json.dumps(execution_result, indent=2)}

Your job is ONLY to explain the result.

Instructions:

1. Answer the user's question naturally.
2. Mention how the semantic layer interpreted the query.
3. If aliases were expanded, briefly mention them.
4. If status groups were expanded, briefly mention them.
5. Never mention JSON.
6. Never invent numbers.
7. Use ONLY the provided execution result.
8. Keep the response under 120 words.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.7-flash",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional CRM assistant. "
                    "Generate concise and accurate responses."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()