# AI 201 — Week 2 Demo: Concert Alert Agent

**For instructors only.** Starter repo for the Week 2 lecture demo.

## What This Demo Does

You'll build a live 3-tool agent that searches for upcoming concerts, checks ticket availability, and drafts a friend-alert text message — handling sold-out shows and missing artists gracefully along the way.

Students will watch you write the two most important pieces of any agent: the tool definitions (how you describe tools to the model) and the ReAct agent loop (how the model decides what to do next).

**Artists in the mock database:**

| Artist | Scenario |
|---|---|
| Tyler, the Creator | Shows available ✓ |
| Chappell Roan | Shows available ✓ |
| Doechii | Shows available ✓ |
| Kendrick Lamar | Mixed — one available, one sold out |
| Sabrina Carpenter | All shows sold out |
| Bad Bunny | Sold out |
| Frank Ocean | No upcoming shows |

---

## Setup

### Step 1 — Prerequisites

Python 3.11+ required.

```bash
python --version
```

### Step 2 — Clone and Install

```bash
git clone <repo-url>
cd ai201-week2-starter-repo
pip install -r requirements.txt
```

### Step 3 — Set Up Your OpenRouter Key

Sign up free at [openrouter.ai](https://openrouter.ai). Get your API key at [openrouter.ai/keys](https://openrouter.ai/keys).

```bash
cp .env.example .env
# Open .env and replace the placeholder with your actual key
```

### Step 4 — Verify Everything Works

```bash
python setup/verify_setup.py
```

This confirms all three tools run correctly and OpenRouter responds with a tool call. If anything fails, the output tells you exactly what to fix.

### Step 5 — Open the Notebook

```bash
jupyter notebook demo.ipynb
```

Run **Cell 1** (setup) to confirm imports load cleanly. Leave it there — ready to demo.

---

## Demo Guide

### What You're Writing Live

Two things — read through both before class so you can type them confidently:

**The tool definitions** (~10 min total with discussion): A list of JSON schema objects describing each tool to the model. Write `search_shows` together with students, then fill in `check_tickets` and `draft_message` while narrating the pattern.

**The agent loop** (~5 min): A while loop that sends messages to the LLM, checks for tool calls, executes them, appends results, and repeats until done. ~20 lines of code.

---

### Before You Start

- Cell 1 already run, notebook ready at Cell 2
- Concert data slide visible (the table of artists and scenarios above)
- Know the two functions you'll write (they're in the notebook cells with full instructor comments — read them before class)

---

### Part 1: Look at the Pre-Built Tools (~2 min)

**Run Cells 2–4.**

Cells 2–3 show `search_shows` and `check_tickets` returning real JSON. Cell 4 shows a sold-out result for Sabrina Carpenter at MSG.

Ask after Cell 4: *"What should the agent do when it sees this? Should it stop? Tell the user? Try resale?"* Don't answer yet — let students think. The demo will show what the model actually does.

**Talking point:** These tools are just Python functions that return strings. The agent doesn't call them directly — the LLM reads a description of them and decides when to use them. That description is what we write next.

---

### Part 2: Write the Tool Definitions (~4 min)

**Write Cell 5 live.**

Start by asking: *"What does the model need to know about a tool?"* Take a few answers, then land on: the name, what it does (description), and what arguments to pass (parameters schema).

Write `search_shows` together:

```python
{
    "type": "function",
    "function": {
        "name": "search_shows",
        "description": "Search for upcoming concerts for a given artist. Call this first for any artist before checking tickets.",
        "parameters": {
            "type": "object",
            "properties": {
                "artist_name": {
                    "type": "string",
                    "description": "The name of the artist to search for",
                }
            },
            "required": ["artist_name"],
        },
    },
}
```

Then say: *"Same pattern for the other two — different name, description, and parameters."* Fill in `check_tickets` and `draft_message` while students predict the structure.

**Key talking point to land:** *"We're not calling these tools. We're describing them. The model reads these descriptions and decides when to call each one, based on context."*

---

### Part 3: Write the Agent Loop (~4 min)

**Write Cell 6 live.**

Ask before starting: *"What are the steps in the loop?"* Take answers. Then land on:

1. Ask the model what to do next
2. Did it want to call a tool? → run the tool, give it the result, loop
3. Did it give a final answer? → done

Narrate as you type:

- *"msg.tool_calls is how we know the model wants to use a tool"*
- *"TOOL_REGISTRY maps the name 'search_shows' to the actual Python function"*
- *"We append the tool result as a 'tool' role message — that's how the model reads what came back"*
- *"The loop keeps running until tool_calls is empty — that's our stop condition"*
- *"max_steps is our safety valve — prevents an infinite loop if the model gets stuck"*

---

### Part 4: Run the Three Scenarios (~4 min)

**Run Cells 7–9.**

**Cell 7 — Tyler, the Creator (happy path):** Watch the step log as it runs. Ask: *"What did the model call first? Why that order?"* Then show the drafted message. *"We didn't write any drafting logic — we just described a tool. The model decided when to use it."*

**Cell 8 — Sabrina Carpenter (sold out):** Ask: *"We didn't write any 'if sold out, do this' logic. How does the agent know what to do?"* Answer: it read the check_tickets response and adapted its behavior. Ask: *"Is this the behavior you'd want in production? What might go wrong?"*

**Cell 9 — Chappell Roan + Frank Ocean + Doechii (multiple artists, one with no shows):** Watch it work through all three. Show the state summary at the end. Ask: *"What would go wrong if we didn't track state across tool calls?"* (The agent might search the same artist twice, or draft duplicate messages.)

---

### Part 5: Show the Message History (~1 min)

**Run Cell 10.**

This prints every message the model received during a single agent run — system prompt, user message, tool calls, tool results, final response.

Ask: *"Why do we keep the whole conversation history in memory?"* Answer: the model has no memory between calls. The message history IS the memory. Without it, the model would forget what it already searched.

Ask: *"What would happen if we only sent the last message each time?"* (The model would lose context and likely call the same tool over and over.)

---

## Troubleshooting

**Model doesn't make tool calls — just responds with text**
Some free models on OpenRouter have inconsistent tool-call behavior. Try switching to `mistralai/mistral-7b-instruct:free` in your `.env` file. The demo logic still works — you can show the tool manually and explain what the model should have called.

**"Unknown tool" error in the loop**
The model generated a tool name that doesn't match the registry. This usually means the description was ambiguous. Point it out to students as a real-world debugging moment: *"This is why the description field matters — vague descriptions lead to unpredictable tool selection."*

**Agent loops more steps than expected**
Normal for complex multi-artist runs. The max_steps limit prevents it from running forever. If it hits the limit, reduce the number of artists in the request.

**OpenRouter rate limit**
Free tier has generous limits but can hit them during a busy class. If you get a 429 error, wait 30 seconds and retry. As a fallback, pre-run the scenarios and show the output.

---

## Repo Structure

```plaintext
ai201-week2-starter-repo/
├── README.md
├── requirements.txt
├── .env.example
├── demo.ipynb                    # The demo notebook
│
├── data/
│   └── concerts.py               # Mock concert database (7 artists, 4 scenarios)
│
├── tools/
│   ├── __init__.py               # TOOL_REGISTRY — maps tool names to functions
│   ├── search_shows.py
│   ├── check_tickets.py
│   └── draft_message.py
│
├── utils/
│   ├── llm.py                    # OpenRouter client with tool_call support
│   └── state.py                  # AgentState — tracks what the agent has done
│
└── setup/
    └── verify_setup.py           # Pre-demo sanity check
```
