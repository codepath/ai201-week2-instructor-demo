"""
Tool: search_shows
==================
Searches for upcoming concerts for a given artist.
Returns show details if found, or a clear "no shows" message if not.

This is the first tool the agent will call for any artist. Its output
determines whether the agent proceeds to check tickets or moves on.

Demo talking point:
    The return value here is a plain string — that's what goes back into
    the message history as the "tool result." The LLM reads this string
    and decides what to do next. It's just text in, text out.
"""

import json
from data.concerts import lookup_artist, lookup_show


def search_shows(artist_name: str) -> str:
    """
    Search for upcoming shows for an artist.

    Parameters
    ----------
    artist_name : str
        The name of the artist to search for.

    Returns
    -------
    str
        A JSON string with show results, or a message indicating no shows found.
    """
    show_ids = lookup_artist(artist_name)

    if not show_ids:
        return json.dumps({
            "artist": artist_name,
            "shows_found": 0,
            "message": f"No upcoming shows found for {artist_name}.",
            "shows": [],
        })

    shows = []
    for show_id in show_ids:
        show = lookup_show(show_id)
        if show:
            shows.append({
                "show_id": show["id"],
                "venue": show["venue"],
                "city": show["city"],
                "date": show["date"],
                "doors": show["doors"],
                "price_range": show["price_range"],
                "tour": show["tour"],
            })

    return json.dumps({
        "artist": artist_name,
        "shows_found": len(shows),
        "message": f"Found {len(shows)} upcoming show(s) for {artist_name}.",
        "shows": shows,
    })
