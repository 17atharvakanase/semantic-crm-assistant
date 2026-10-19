import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

if not HUBSPOT_TOKEN:
    raise ValueError("HUBSPOT_TOKEN not found in .env")

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}


def get_schema():
    """
    Fetch all Deal properties (schema) from HubSpot.

    Returns:
        pandas.DataFrame
    """

    url = "https://api.hubapi.com/crm/v3/properties/deals"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch schema.\n"
            f"Status Code: {response.status_code}\n"
            f"Response: {response.text}"
        )

    properties = response.json()["results"]

    schema = []

    for prop in properties:
        schema.append({
            "name": prop["name"],
            "label": prop["label"],
            "type": prop["type"],
            "description": prop.get("description", "")
        })

    return pd.DataFrame(schema)


def get_custom_properties():
    """
    Returns only the custom properties used in this project.
    """

    schema_df = get_schema()

    custom_properties = [
        "assigned_to",
        "internal_status",
        "priority_tag",
        "region"
    ]

    return schema_df[
        schema_df["name"].isin(custom_properties)
    ]


def get_deals(limit=100):
    """
    Fetch deals from HubSpot.

    Args:
        limit (int): Maximum number of deals.

    Returns:
        pandas.DataFrame
    """

    properties = [
        "dealname",
        "dealstage",
        "assigned_to",
        "internal_status",
        "priority_tag",
        "region"
    ]

    url = (
        "https://api.hubapi.com/crm/v3/objects/deals"
        f"?limit={limit}&properties=" + ",".join(properties)
    )

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch deals.\n"
            f"Status Code: {response.status_code}\n"
            f"Response: {response.text}"
        )

    deals = response.json()["results"]

    rows = []

    for deal in deals:
        row = {
            "id": deal["id"]
        }

        row.update(deal.get("properties", {}))

        rows.append(row)

    return pd.DataFrame(rows)


def get_sample_records(sample_size=20):
    """
    Returns a small sample of CRM records for semantic discovery.

    Args:
        sample_size (int)

    Returns:
        pandas.DataFrame
    """

    deals_df = get_deals()

    columns = [
        "assigned_to",
        "internal_status",
        "priority_tag",
        "region",
        "dealstage"
    ]

    return deals_df[columns].head(sample_size)