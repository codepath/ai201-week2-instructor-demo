"""
Tool: draft_message
===================
Drafts a ready-to-send text message alerting friends about a concert.
The agent calls this after confirming tickets are available.

Demo talking point:
    This tool only gets called if the agent found available tickets.
    That's state management in action — the agent tracked what it learned
    from search_shows and check_tickets before deciding to call this.
    Ask students: "How does the agent know not to draft a message for
    Sabrina Carpenter?" (It read the check_tickets response and adapted.)
"""

import json


def draft_message(
    artist_name: str,
    venue: str,
    city: str,
    date: str,
    price_range: str,
    friends: list[str] | None = None,
) -> str:
    """
    Draft a text message alerting friends about available concert tickets.

    Parameters
    ----------
    artist_name : str
        Name of the artist performing.
    venue : str
        Name of the venue.
    city : str
        City and state of the show.
    date : str
        Date of the show (YYYY-MM-DD format).
    price_range : str
        Ticket price range string, e.g. "$85–$240".
    friends : list[str] | None
        Names of friends to address in the message. Defaults to a generic greeting.

    Returns
    -------
    str
        A JSON string containing the drafted message and metadata.
    """
    # Format the date more readably
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_formatted = date_obj.strftime("%A, %B %-d")
    except (ValueError, AttributeError):
        date_formatted = date

    # Build the greeting
    if friends:
        names = ", ".join(friends[:-1]) + (f" and {friends[-1]}" if len(friends) > 1 else friends[0])
        greeting = f"Hey {names}!"
    else:
        greeting = "Hey everyone!"

    message = (
        f"{greeting} {artist_name} has tickets available and we need to move. "
        f"{venue} in {city} on {date_formatted}. "
        f"Prices start at {price_range.split('–')[0]}. "
        f"Who's in? 🎶"
    )

    return json.dumps({
        "status": "drafted",
        "artist": artist_name,
        "message": message,
        "character_count": len(message),
        "note": "Message ready to send — copy and paste into your group chat.",
    })
