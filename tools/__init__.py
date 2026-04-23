from .search_shows import search_shows
from .check_tickets import check_tickets
from .draft_message import draft_message

# Registry used by the agent loop to dispatch tool calls by name
TOOL_REGISTRY = {
    "search_shows": search_shows,
    "check_tickets": check_tickets,
    "draft_message": draft_message,
}

__all__ = ["search_shows", "check_tickets", "draft_message", "TOOL_REGISTRY"]
