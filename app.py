import os
import json
import streamlit as st

from connector import get_deals, get_sample_records
from semantic_mapper import build_semantic_memory
from query_planner import generate_query_plan
from semantic_resolver import resolve_filters
from executor import execute_query
from response_generator import generate_human_response


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Semantic CRM Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Semantic CRM Assistant")
st.markdown(
    "Ask questions about your CRM using natural language."
)

# -----------------------------
# Load Deal Data
# -----------------------------
with st.spinner("Loading CRM data..."):
    deals_df = get_deals()

# -----------------------------
# Load / Build Semantic Memory
# -----------------------------
SEMANTIC_FILE = "semantic_memory.json"

if os.path.exists(SEMANTIC_FILE):

    with open(SEMANTIC_FILE, "r") as f:
        semantic_memory = json.load(f)

else:

    with st.spinner("Building semantic memory..."):

        sample_df = get_sample_records()

        semantic_memory = build_semantic_memory(sample_df)

        with open(SEMANTIC_FILE, "w") as f:
            json.dump(semantic_memory, f, indent=4)

# -----------------------------
# User Input
# -----------------------------
question = st.text_input(
    "Ask a CRM question",
    placeholder="Example: How many open deals does Garima own?"
)

# -----------------------------
# Example Questions
# -----------------------------
st.markdown("### Try these examples:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Open deals for Garima"):
        question = "How many open deals does Garima own?"

with col2:
    if st.button("High priority deals"):
        question = "Show all high priority deals."

with col3:
    if st.button("Dead leads"):
        question = "List all dead leads."

# -----------------------------
# Ask Button
# -----------------------------
if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Understanding your question..."):

            # Query Planner
            plan = generate_query_plan(
                question,
                semantic_memory
            )

            # Semantic Resolver
            resolved_filters = resolve_filters(
                plan,
                semantic_memory
            )

            # Execute Query
            filtered_df = execute_query(
                deals_df,
                resolved_filters
            )

            # Generate Response
            answer = generate_human_response(
                question,
                plan,
                resolved_filters,
                filtered_df
            )

        # -----------------------------
        # Final Answer
        # -----------------------------
        st.success(answer)

        st.metric(
            label="Matching Deals",
            value=len(filtered_df)
        )

        # -----------------------------
        # Matching Records
        # -----------------------------
        st.subheader("Matching Deals")

        if filtered_df.empty:

            st.info("No matching records found.")

        else:

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

        # -----------------------------
        # Developer View
        # -----------------------------
        with st.expander("Developer View"):

            st.subheader("Execution Plan")
            st.json(plan)

            st.subheader("Semantic Translation")
            st.json(resolved_filters)

            st.subheader("Semantic Memory")
            st.json(semantic_memory)