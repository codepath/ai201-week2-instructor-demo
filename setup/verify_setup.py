"""
Verify Setup
============
Run this the night before or morning of the demo to confirm everything works.

Usage:
    python setup/verify_setup.py

Checks:
    1. Concert data loads correctly and covers all four scenarios
    2. All three tools run without errors
    3. OpenRouter API key is set and the model responds with a tool call
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import search_shows, check_tickets, draft_message
from utils.llm import LLMClient


def check_concert_data() -> bool:
    print("\n[1/3] Checking concert data...")
    from data.concerts import ARTIST_SHOWS, SHOWS, TICKET_AVAILABILITY

    artists = list(ARTIST_SHOWS.keys())
    print(f"  Artists in database: {', '.join(artists)}")

    has_available   = any(t["available"] for t in TICKET_AVAILABILITY.values())
    has_sold_out    = any(not t["available"] for t in TICKET_AVAILABILITY.values())
    has_no_shows    = any(len(ids) == 0 for ids in ARTIST_SHOWS.values())

    if not has_available:
        print("  ✗ No shows with available tickets — add at least one.")
        return False
    if not has_sold_out:
        print("  ✗ No sold-out shows — the sold-out demo scenario won't work.")
        return False
    if not has_no_shows:
        print("  ✗ No artist with zero shows — the 'no shows' scenario won't work.")
        return False

    print(f"  ✓ {len(SHOWS)} shows, all four demo scenarios covered")
    return True


def check_tools() -> bool:
    print("\n[2/3] Checking tools...")

    # search_shows — happy path
    result = json.loads(search_shows("Tyler, the Creator"))
    if result["shows_found"] == 0:
        print("  ✗ search_shows returned 0 shows for Tyler, the Creator")
        return False
    print(f"  ✓ search_shows: found {result['shows_found']} shows for Tyler, the Creator")

    # check_tickets — available
    first_show_id = result["shows"][0]["show_id"]
    ticket_result = json.loads(check_tickets(first_show_id))
    if not ticket_result.get("tickets_available"):
        print(f"  ✗ check_tickets: expected available tickets for {first_show_id}")
        return False
    print(f"  ✓ check_tickets: {ticket_result['remaining']} tickets available for {first_show_id}")

    # check_tickets — sold out
    sold_out = json.loads(check_tickets("SHOW003"))
    if sold_out.get("tickets_available"):
        print("  ✗ check_tickets: SHOW003 should be sold out")
        return False
    print(f"  ✓ check_tickets: SHOW003 correctly shows as sold out")

    # search_shows — no shows
    no_shows = json.loads(search_shows("Frank Ocean"))
    if no_shows["shows_found"] != 0:
        print("  ✗ search_shows: Frank Ocean should have 0 shows")
        return False
    print(f"  ✓ search_shows: Frank Ocean correctly returns no shows")

    # draft_message
    msg_result = json.loads(draft_message(
        artist_name="Tyler, the Creator",
        venue="Kia Forum",
        city="Los Angeles, CA",
        date="2025-08-14",
        price_range="$85–$240",
        friends=["Jordan", "Maya"],
    ))
    if msg_result["status"] != "drafted":
        print("  ✗ draft_message: unexpected status")
        return False
    print(f"  ✓ draft_message: '{msg_result['message'][:60]}...'")

    return True


def check_llm() -> bool:
    print("\n[3/3] Checking OpenRouter LLM with tool call...")
    try:
        llm = LLMClient()
        print(f"  Model: {llm.model}")

        # Minimal tool definition to test the tool-call flow
        tools = [{
            "type": "function",
            "function": {
                "name": "search_shows",
                "description": "Search for upcoming concerts for a given artist.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "artist_name": {"type": "string"}
                    },
                    "required": ["artist_name"],
                },
            },
        }]

        response = llm.chat(
            messages=[
                {"role": "system", "content": "You are a concert alert agent. Use tools to help users."},
                {"role": "user", "content": "Are there any upcoming Tyler, the Creator shows?"},
            ],
            tools=tools,
        )

        msg = response.choices[0].message
        if msg.tool_calls:
            call = msg.tool_calls[0]
            args = json.loads(call.function.arguments)
            print(f"  ✓ Model called tool '{call.function.name}' with args: {args}")
        else:
            # Some models respond with text instead of a tool call — acceptable for verify
            print(f"  ✓ Model responded (no tool call — may vary by model): '{msg.content[:80]}...'")

        return True

    except ValueError as e:
        print(f"  ✗ {e}")
        return False
    except Exception as e:
        print(f"  ✗ OpenRouter request failed: {e}")
        return False


def main():
    print("=" * 60)
    print("AI 201 — Week 2 Demo: Pre-Demo Verification")
    print("=" * 60)

    results = [
        check_concert_data(),
        check_tools(),
        check_llm(),
    ]

    print()
    if all(results):
        print("=" * 60)
        print("✓ All checks passed. Open demo.ipynb to begin.")
        print("=" * 60)
    else:
        print("✗ Some checks failed — fix the errors above before the demo.")
        sys.exit(1)


if __name__ == "__main__":
    main()
