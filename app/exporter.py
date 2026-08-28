"""Deterministic output generation.

READ THIS FILE LAST if you are following the teaching path.

Prompt Chaining ends when ``run_chain()`` returns a validated ``Course``.
Everything here is ordinary Python: no model calls, no prompts, no agent logic.

The Markdown renderer intentionally makes the richer structured output pleasant
to read. This demonstrates an important boundary: presentation can be polished
without spending another LLM call on formatting.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.schemas import Course


def export_course(course: Course, output_dir: Path) -> list[Path]:
    """Save the final Course as readable Markdown and machine-readable JSON."""

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / "course.md"
    json_path = output_dir / "course.json"

    markdown_path.write_text(to_markdown(course), encoding="utf-8")
    json_path.write_text(
        json.dumps(course.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return [markdown_path, json_path]


def to_markdown(course: Course) -> str:
    """Render a polished course without asking the LLM to format it again."""

    curriculum = course.curriculum
    lines = [
        f"# {curriculum.course_title}",
        "",
        f"> {curriculum.course_hook}",
        "",
        "---",
        "",
        "## Course Map",
        "",
    ]

    for index, module in enumerate(curriculum.modules, start=1):
        lines.extend(
            [
                f"### {index}. {module.title}",
                "",
                f"**Why this matters:** {module.hook}",
                "",
                f"**Goal:** {module.objective}",
                "",
                f"**Concepts:** {', '.join(module.concepts)}",
                "",
            ]
        )

    lines.extend(["---", "", "## Concepts at a Glance", ""])
    for concept in course.concepts.concepts:
        lines.extend(
            [
                f"### {concept.name}",
                "",
                concept.explanation,
                "",
                f"**Why it matters:** {concept.why_it_matters}",
                "",
            ]
        )

    lines.extend(["---", "", "## Lessons", ""])
    for index, lesson in enumerate(course.lessons.lessons, start=1):
        lines.extend(
            [
                f"## Lesson {index} — {lesson.title}",
                "",
                "### Start with this question",
                "",
                f"> {lesson.opening_question}",
                "",
                "### Build the intuition",
                "",
                lesson.intuition,
                "",
                "### How it works",
                "",
                lesson.explanation,
                "",
                "### A useful analogy",
                "",
                lesson.analogy,
                "",
                "### Make it concrete",
                "",
                lesson.example,
                "",
                "### Common misconception",
                "",
                lesson.misconception,
                "",
                "### Key takeaways",
                "",
            ]
        )
        for takeaway in lesson.key_takeaways:
            lines.append(f"- {takeaway}")
        lines.extend(
            [
                "",
                "### Try this",
                "",
                f"> {lesson.challenge}",
                "",
                "---",
                "",
            ]
        )

    lines.extend(["## Knowledge Check", ""])
    for index, question in enumerate(course.assessment.questions, start=1):
        lines.extend(
            [
                f"### {index}. {question.question}",
                "",
            ]
        )
        for choice in question.choices:
            lines.append(f"- {choice}")
        lines.extend(
            [
                "",
                f"**Answer:** {question.answer}",
                "",
                f"**Why:** {question.explanation}",
                "",
            ]
        )

    lines.extend(["---", "", "## Flashcards", ""])
    for index, card in enumerate(course.assessment.flashcards, start=1):
        lines.extend(
            [
                f"### Card {index}",
                "",
                f"**Front:** {card.front}",
                "",
                f"**Back:** {card.back}",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"
