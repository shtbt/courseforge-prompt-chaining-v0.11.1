"""CourseForge — a small, readable Prompt Chaining project.

START HERE.

This file deliberately contains only the application-level flow:

    1. load configuration from .env
    2. read the source document
    3. run the Prompt Chaining workflow
    4. export the final course

The Prompt Chaining architecture itself lives in ``app/chain.py``.
After reading this file, open that file next.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

from app.chain import run_chain
from app.exporter import export_course


# Keeping these paths here makes the example easy to run and easy to teach.
# A production application could expose them as CLI options or configuration.
SOURCE_FILE = Path("examples/gps.md")
OUTPUT_DIR = Path("output")


def create_model() -> ChatOpenRouter:
    """Create the chat model configured in ``.env``.

    The application-facing variables stay provider-neutral (``LLM_API_KEY``
    and ``LLM_MODEL``), while this implementation deliberately uses
    LangChain's dedicated ``ChatOpenRouter`` integration instead of pointing
    ``ChatOpenAI`` at an OpenRouter base URL.
    That keeps OpenRouter-specific features—especially structured output and
    provider routing—explicit and reliable.

    ``require_parameters=True`` is important for this project: every stage
    requests JSON Schema structured output, so OpenRouter should only route the
    request to provider endpoints that actually support those parameters.
    """

    api_key = os.environ["LLM_API_KEY"]
    model_name = os.getenv("LLM_MODEL", "openrouter/free")

    return ChatOpenRouter(
        model=model_name,
        api_key=api_key,
        temperature=0,
        max_retries=2,
        openrouter_provider={"require_parameters": True},
    )


def main() -> None:
    """Assemble the application around the Prompt Chaining workflow."""

    # ------------------------------------------------------------------
    # STEP 1 — CONFIGURATION
    # .env exposes a provider-neutral application contract: an LLM key and
    # model name. This implementation currently connects them to OpenRouter.
    # ------------------------------------------------------------------
    load_dotenv()
    model = create_model()

    # ------------------------------------------------------------------
    # STEP 2 — INPUT
    # CourseForge intentionally starts with one committed source document so
    # a learner can run the example without first learning a CLI interface.
    # ------------------------------------------------------------------
    source = SOURCE_FILE.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # STEP 3 — PROMPT CHAINING
    # This is the architectural center of the application.
    # Open app/chain.py to see the four model stages and their handoffs.
    # ------------------------------------------------------------------
    course = run_chain(source, model)

    # ------------------------------------------------------------------
    # STEP 4 — OUTPUT
    # Exporting is deterministic Python code. It is deliberately outside the
    # LLM workflow so learners can see where Prompt Chaining ends.
    # ------------------------------------------------------------------
    files = export_course(course, OUTPUT_DIR)

    print("\nCourse complete.")
    for path in files:
        print(f"  → {path}")


if __name__ == "__main__":
    main()
