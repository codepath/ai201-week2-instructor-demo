"""
Agent State Tracker
===================
Tracks what the agent has done across tool calls so it doesn't repeat work.

Demo talking point:
    Without state, the agent might search for Tyler, the Creator three times
    in the same run, or draft a duplicate message. State is what turns a
    single LLM call into a coherent agent with memory across steps.

    Ask students: "Where does this state live between tool calls?"
    Answer: In Python memory, right here. In production you'd persist this
    to a database or cache so it survives across sessions.
"""

from dataclasses import dataclass, field


@dataclass
class AgentState:
    """
    Tracks the agent's progress across tool calls for a single run.

    Attributes
    ----------
    artists_requested : list[str]
        Artists the user wants alerts for (the input).
    artists_checked : set[str]
        Artists the agent has already run search_shows on.
        Prevents duplicate searches.
    shows_with_tickets : list[dict]
        Shows the agent confirmed have available tickets.
        Each entry: {artist, show_id, venue, city, date, price_range}
    shows_sold_out : list[dict]
        Shows the agent found but confirmed are sold out.
    artists_no_shows : list[str]
        Artists with no upcoming concerts at all.
    messages_drafted : list[str]
        The drafted friend-alert messages, ready to send.
    tool_call_count : int
        Total number of tool calls made. Useful for demo narration.
    """
    artists_requested: list[str] = field(default_factory=list)
    artists_checked: set[str] = field(default_factory=set)
    shows_with_tickets: list[dict] = field(default_factory=list)
    shows_sold_out: list[dict] = field(default_factory=list)
    artists_no_shows: list[str] = field(default_factory=list)
    messages_drafted: list[str] = field(default_factory=list)
    tool_call_count: int = 0

    def mark_checked(self, artist_name: str):
        """Record that this artist has been searched."""
        self.artists_checked.add(artist_name.lower().strip())

    def already_checked(self, artist_name: str) -> bool:
        """Return True if we've already searched for this artist."""
        return artist_name.lower().strip() in self.artists_checked

    def summary(self) -> str:
        """Return a readable summary of what the agent accomplished."""
        lines = [
            f"Artists requested:  {', '.join(self.artists_requested) or 'none'}",
            f"Tool calls made:    {self.tool_call_count}",
            f"Shows with tickets: {len(self.shows_with_tickets)}",
            f"Shows sold out:     {len(self.shows_sold_out)}",
            f"Artists no shows:   {len(self.artists_no_shows)}",
            f"Messages drafted:   {len(self.messages_drafted)}",
        ]
        if self.messages_drafted:
            lines.append("\nDrafted messages:")
            for i, msg in enumerate(self.messages_drafted, 1):
                lines.append(f"  [{i}] {msg}")
        return "\n".join(lines)
