"""Typed contracts passed between Prompt Chaining stages.

READ THIS FILE FOURTH.

These Pydantic models are part of the architecture. They make every stage
handoff explicit and keep the richer output predictable without introducing
extra model calls.

The important handoffs remain simple:

    ConceptSet → Curriculum → LessonSet → Assessment
"""

from pydantic import BaseModel, Field


class Concept(BaseModel):
    """One important idea extracted from the source material."""

    name: str = Field(description="Short, precise concept name")
    explanation: str = Field(description="Beginner-friendly explanation")
    why_it_matters: str = Field(
        description="Why this concept matters for understanding the larger topic"
    )


class ConceptSet(BaseModel):
    """Validated output of Stage 1."""

    concepts: list[Concept]


class Module(BaseModel):
    """One step in the learning journey designed during Stage 2."""

    title: str = Field(description="Curiosity-driven module title")
    hook: str = Field(description="Short reason this module is worth learning")
    objective: str = Field(description="What the learner should understand afterward")
    concepts: list[str] = Field(description="Concept names taught in this module")


class Curriculum(BaseModel):
    """Validated output of Stage 2."""

    course_title: str = Field(description="Short, memorable title for the course")
    course_hook: str = Field(description="One-sentence hook for the whole course")
    modules: list[Module]


class Lesson(BaseModel):
    """One engaging lesson corresponding to one curriculum module."""

    title: str
    opening_question: str
    intuition: str
    explanation: str
    analogy: str
    example: str
    misconception: str
    key_takeaways: list[str] = Field(min_length=3, max_length=5)
    challenge: str


class LessonSet(BaseModel):
    """Validated output of Stage 3."""

    lessons: list[Lesson]


class Question(BaseModel):
    """One multiple-choice assessment question."""

    question: str
    choices: list[str] = Field(min_length=4, max_length=4)
    answer: str
    explanation: str


class Flashcard(BaseModel):
    """One compact memory aid produced during Stage 4."""

    front: str
    back: str


class Assessment(BaseModel):
    """Validated output of Stage 4."""

    questions: list[Question]
    flashcards: list[Flashcard]


class Course(BaseModel):
    """Final deterministic container assembled from all four stage outputs."""

    concepts: ConceptSet
    curriculum: Curriculum
    lessons: LessonSet
    assessment: Assessment
