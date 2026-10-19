def resolve_filters(plan, semantic_memory):
    """
    Converts business-level filters into CRM-specific filters
    using semantic memory.

    Args:
        plan (dict): Execution plan from Query Planner.
        semantic_memory (dict): Semantic memory inferred by the LLM.

    Returns:
        dict: CRM-ready filters.
    """

    resolved = {}

    filters = plan.get("filters", {})

    # -----------------------------
    # Resolve Owner
    # -----------------------------
    if "owner" in filters:

        owner = filters["owner"]

        owner_field = semantic_memory["owner_field"]

        aliases = semantic_memory.get(
            "owner_aliases",
            {}
        ).get(owner, [])

        resolved[owner_field] = [owner] + aliases

    # -----------------------------
    # Resolve Status
    # -----------------------------
    if "status" in filters:

        status = filters["status"].lower()

        status_field = semantic_memory["status_field"]

        status_groups = semantic_memory.get(
            "status_groups",
            {}
        )

        if status in status_groups:

            resolved[status_field] = status_groups[status]

        else:

            resolved[status_field] = [filters["status"]]

    # -----------------------------
    # Resolve Priority
    # -----------------------------
    if "priority" in filters:

        priority_field = semantic_memory["priority_field"]

        resolved[priority_field] = [
            filters["priority"]
        ]

    # -----------------------------
    # Resolve Region
    # -----------------------------
    if "region" in filters:

        region_field = semantic_memory["region_field"]

        resolved[region_field] = [
            filters["region"]
        ]

    return resolved