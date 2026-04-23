"""
Tool: check_tickets
===================
Checks ticket availability for a specific show ID.
Returns whether tickets are available, how many remain, and whether
resale-only tickets exist.

Demo talking point:
    This is where the agent hits a wall — sold-out shows.
    Ask students: "What should the agent do when it gets this response?
    Should it stop? Try resale? Alert the user differently?"
    This is error handling as a design decision, not just exception catching.
"""

import json
from data.concerts import lookup_show, lookup_tickets


def check_tickets(show_id: str) -> str:
    """
    Check ticket availability for a given show.

    Parameters
    ----------
    show_id : str
        The unique show identifier returned by search_shows.

    Returns
    -------
    str
        A JSON string describing availability, remaining count, and resale status.
    """
    show = lookup_show(show_id)
    if not show:
        return json.dumps({
            "show_id": show_id,
            "error": f"Show ID '{show_id}' not found.",
        })

    availability = lookup_tickets(show_id)
    if not availability:
        return json.dumps({
            "show_id": show_id,
            "error": f"No ticket data available for show '{show_id}'.",
        })

    result = {
        "show_id": show_id,
        "artist": show["artist"],
        "venue": show["venue"],
        "city": show["city"],
        "date": show["date"],
        "price_range": show["price_range"],
        "tickets_available": availability["available"],
        "remaining": availability["remaining"],
        "resale_only": availability["resale_only"],
    }

    if availability["available"]:
        result["status"] = f"{availability['remaining']} tickets available at {show['price_range']}"
    elif availability["resale_only"]:
        result["status"] = "Sold out — resale tickets may be available on secondary markets"
    else:
        result["status"] = "Sold out — no tickets available"

    return json.dumps(result)
