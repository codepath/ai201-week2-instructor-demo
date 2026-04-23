"""
Mock Concert Database
=====================
Fake but realistic concert data used for the Week 2 demo.
Covers four scenarios the agent needs to handle:

    Happy path      — shows exist, tickets available     (Tyler, the Creator / Chappell Roan / Doechii)
    Sold out        — shows exist, no tickets left        (Sabrina Carpenter / Bad Bunny)
    Partial         — some shows available, some sold out (Kendrick Lamar)
    No shows        — artist has nothing upcoming         (Frank Ocean)

Instructor note: feel free to swap in artists your cohort is excited about.
The scenarios (happy / sold-out / no-shows) are what matter for the demo —
just make sure at least one artist represents each.
"""

from datetime import date

# ---------------------------------------------------------------------------
# Show catalog
# Each show has a unique ID, artist, venue, city, date, and price range.
# ---------------------------------------------------------------------------
SHOWS: dict[str, dict] = {
    "SHOW001": {
        "id": "SHOW001",
        "artist": "Tyler, the Creator",
        "tour": "Chromakopia World Tour",
        "venue": "Kia Forum",
        "city": "Los Angeles, CA",
        "date": "2025-08-14",
        "doors": "7:00 PM",
        "price_range": "$85–$240",
    },
    "SHOW002": {
        "id": "SHOW002",
        "artist": "Tyler, the Creator",
        "tour": "Chromakopia World Tour",
        "venue": "Chase Center",
        "city": "San Francisco, CA",
        "date": "2025-08-17",
        "doors": "7:30 PM",
        "price_range": "$90–$260",
    },
    "SHOW003": {
        "id": "SHOW003",
        "artist": "Sabrina Carpenter",
        "tour": "Short n' Sweet Tour",
        "venue": "Madison Square Garden",
        "city": "New York, NY",
        "date": "2025-07-22",
        "doors": "7:00 PM",
        "price_range": "$75–$200",
    },
    "SHOW004": {
        "id": "SHOW004",
        "artist": "Sabrina Carpenter",
        "tour": "Short n' Sweet Tour",
        "venue": "United Center",
        "city": "Chicago, IL",
        "date": "2025-07-25",
        "doors": "7:00 PM",
        "price_range": "$80–$210",
    },
    "SHOW005": {
        "id": "SHOW005",
        "artist": "Kendrick Lamar",
        "tour": "The Pop Out Tour",
        "venue": "Crypto.com Arena",
        "city": "Los Angeles, CA",
        "date": "2025-09-06",
        "doors": "8:00 PM",
        "price_range": "$120–$400",
    },
    "SHOW006": {
        "id": "SHOW006",
        "artist": "Kendrick Lamar",
        "tour": "The Pop Out Tour",
        "venue": "T-Mobile Arena",
        "city": "Las Vegas, NV",
        "date": "2025-09-10",
        "doors": "8:00 PM",
        "price_range": "$110–$380",
    },
    "SHOW007": {
        "id": "SHOW007",
        "artist": "Chappell Roan",
        "tour": "The Midwest Princess Tour",
        "venue": "Red Rocks Amphitheatre",
        "city": "Morrison, CO",
        "date": "2025-08-02",
        "doors": "6:30 PM",
        "price_range": "$65–$150",
    },
    "SHOW008": {
        "id": "SHOW008",
        "artist": "Chappell Roan",
        "tour": "The Midwest Princess Tour",
        "venue": "Moody Center",
        "city": "Austin, TX",
        "date": "2025-08-05",
        "doors": "7:00 PM",
        "price_range": "$70–$160",
    },
    "SHOW009": {
        "id": "SHOW009",
        "artist": "Bad Bunny",
        "tour": "Nadie Sabe Lo Que Va a Pasar Mañana Tour",
        "venue": "SoFi Stadium",
        "city": "Inglewood, CA",
        "date": "2025-10-11",
        "doors": "7:00 PM",
        "price_range": "$100–$350",
    },
    "SHOW010": {
        "id": "SHOW010",
        "artist": "Doechii",
        "tour": "Alligator Bites Never Heal Tour",
        "venue": "The Novo",
        "city": "Los Angeles, CA",
        "date": "2025-07-30",
        "doors": "8:00 PM",
        "price_range": "$45–$95",
    },
    "SHOW011": {
        "id": "SHOW011",
        "artist": "Doechii",
        "tour": "Alligator Bites Never Heal Tour",
        "venue": "Brooklyn Steel",
        "city": "Brooklyn, NY",
        "date": "2025-08-03",
        "doors": "8:00 PM",
        "price_range": "$50–$100",
    },
}

# ---------------------------------------------------------------------------
# Ticket availability
# Maps show ID → availability status and remaining count.
# ---------------------------------------------------------------------------
TICKET_AVAILABILITY: dict[str, dict] = {
    "SHOW001": {"available": True,  "remaining": 312, "resale_only": False},
    "SHOW002": {"available": True,  "remaining": 87,  "resale_only": False},
    "SHOW003": {"available": False, "remaining": 0,   "resale_only": True},
    "SHOW004": {"available": False, "remaining": 0,   "resale_only": True},
    "SHOW005": {"available": True,  "remaining": 44,  "resale_only": False},
    "SHOW006": {"available": False, "remaining": 0,   "resale_only": True},
    "SHOW007": {"available": True,  "remaining": 203, "resale_only": False},
    "SHOW008": {"available": True,  "remaining": 156, "resale_only": False},
    "SHOW009": {"available": False, "remaining": 0,   "resale_only": True},
    "SHOW010": {"available": True,  "remaining": 78,  "resale_only": False},
    "SHOW011": {"available": True,  "remaining": 122, "resale_only": False},
}

# ---------------------------------------------------------------------------
# Artist index — maps normalized artist name → list of show IDs.
# Frank Ocean intentionally has no shows (models the "nothing found" case).
# ---------------------------------------------------------------------------
ARTIST_SHOWS: dict[str, list[str]] = {
    "tyler, the creator": ["SHOW001", "SHOW002"],
    "sabrina carpenter":  ["SHOW003", "SHOW004"],
    "kendrick lamar":     ["SHOW005", "SHOW006"],
    "chappell roan":      ["SHOW007", "SHOW008"],
    "bad bunny":          ["SHOW009"],
    "doechii":            ["SHOW010", "SHOW011"],
    "frank ocean":        [],  # No upcoming shows — intentional demo scenario
}


def lookup_artist(artist_name: str) -> list[str]:
    """Return a list of show IDs for an artist. Case-insensitive."""
    return ARTIST_SHOWS.get(artist_name.lower().strip(), [])


def lookup_show(show_id: str) -> dict | None:
    """Return show details for a given show ID, or None if not found."""
    return SHOWS.get(show_id)


def lookup_tickets(show_id: str) -> dict | None:
    """Return ticket availability for a given show ID, or None if not found."""
    return TICKET_AVAILABILITY.get(show_id)
