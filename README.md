# 🧠 Semantic CRM Assistant

A semantic translation layer built on top of HubSpot CRM that allows users to query CRM data using natural language. The system learns client-specific business semantics and translates user intent into executable CRM queries.

## Features

- Connects to HubSpot CRM
- Discovers CRM schema automatically
- Learns business semantics using an LLM
- Supports natural language queries
- Resolves aliases and business concepts (e.g., "Open Deals")
- Returns human-friendly responses through a Streamlit UI

## Project Structure

```
semantic-crm/
│
├── app.py
├── connector.py
├── llm.py
├── semantic_mapper.py
├── query_planner.py
├── semantic_resolver.py
├── executor.py
├── response_generator.py
├── semantic_memory.json
├── requirements.txt
└── .env
```

## Architecture

```
User Question
      │
      ▼
Query Planner (LLM)
      │
      ▼
Semantic Resolver
      │
      ▼
Execution Engine
      │
      ▼
Response Generator (LLM)
      │
      ▼
Natural Language Answer
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file:

```env
HUBSPOT_TOKEN=YOUR_HUBSPOT_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

3. Run the application:

```bash
streamlit run app.py
```

## Example Queries

- How many open deals does Garima own?
- Show all high priority deals.
- List all dead leads.
- Show deals in the West region.

## Tech Stack

- Python
- Streamlit
- Pandas
- HubSpot CRM API
- OpenRouter (Qwen 3.7 Flash)
- Requests
- python-dotenv

---

Built as part of the **Treelife AI Technical Assessment**.