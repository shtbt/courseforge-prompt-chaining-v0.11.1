"""The Prompt Chaining architecture used by CourseForge.

READ THIS FILE SECOND, immediately after ``main.py``.

The entire architecture is intentionally visible in one place:

    source text
        ↓
    Stage 1: extract_concepts()        → ConceptSet
        ↓
    Stage 2: design_curriculum()       → Curriculum
        ↓
    Stage 3: generate_lessons()        → LessonSet
        ↓
    Stage 4: generate_assessment()     → Assessment
        ↓
    Course

Python controls every transition. The model does not choose what happens next.
That is why this project demonstrates a *workflow* (Prompt Chaining), not an
autonomous agent.

LangChain is used *inside* each stage to express the same small pipeline:

    PromptTemplate | ChatModel.with_structured_output(PydanticSchema)

After this file, read ``prompts.py`` to inspect the four prompts, then
``schemas.py`` to inspect the typed objects passed between stages.
"""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from app.prompts import (
    ASSESSMENT_PROMPT,
    CONCEPT_EXTRACTION_PROMPT,
    CURRICULUM_PROMPT,
    LESSON_PROMPT,
    SYSTEM_PROMPT,
)
from app.schemas import Assessment, ConceptSet, Course, Curriculum, LessonSet


def run_chain(source: str, model: BaseChatModel) -> Course:
    """Run the four Prompt Chaining stages in a fixed order.

    This function is the most important function in the repository. It shows
    the architecture without framework-specific orchestration machinery.

    Each returned Pydantic object becomes trusted, structured input to the
    following stage.
    """

    # ------------------------------------------------------------------
    # STAGE 1 — CONCEPT EXTRACTION
    # Raw source text → ConceptSet
    # ------------------------------------------------------------------
    print("\n[1/4] Concept Extraction")
    print("      source → ConceptSet")
    concepts = extract_concepts(source, model)
    print(f"      ✓ {len(concepts.concepts)} concepts")

    # ------------------------------------------------------------------
    # HANDOFF 1 → 2
    # Stage 2 receives the validated ConceptSet produced by Stage 1.
    # ------------------------------------------------------------------
    print("\n               ↓ ConceptSet")

    # ------------------------------------------------------------------
    # STAGE 2 — CURRICULUM DESIGN
    # ConceptSet → Curriculum
    # ------------------------------------------------------------------
    print("\n[2/4] Curriculum Design")
    print("      ConceptSet → Curriculum")
    curriculum = design_curriculum(concepts, model)
    print(f"      ✓ {len(curriculum.modules)} modules")

    # ------------------------------------------------------------------
    # HANDOFF 2 → 3
    # Stage 3 uses both the concepts and the designed curriculum.
    # ------------------------------------------------------------------
    print("\n               ↓ Curriculum")

    # ------------------------------------------------------------------
    # STAGE 3 — LESSON GENERATION
    # ConceptSet + Curriculum → LessonSet
    # ------------------------------------------------------------------
    print("\n[3/4] Lesson Generation")
    print("      ConceptSet + Curriculum → LessonSet")
    lessons = generate_lessons(concepts, curriculum, model)
    print(f"      ✓ {len(lessons.lessons)} lessons")

    # ------------------------------------------------------------------
    # HANDOFF 3 → 4
    # The final model call builds an assessment from what was taught.
    # ------------------------------------------------------------------
    print("\n               ↓ LessonSet")

    # ------------------------------------------------------------------
    # STAGE 4 — ASSESSMENT GENERATION
    # Curriculum + LessonSet → Assessment
    # ------------------------------------------------------------------
    print("\n[4/4] Assessment Generation")
    print("      Curriculum + LessonSet → Assessment")
    assessment = generate_assessment(curriculum, lessons, model)
    print(
        f"      ✓ {len(assessment.questions)} questions + "
        f"{len(assessment.flashcards)} flashcards"
    )

    # No model call is needed here. We simply combine the validated outputs.
    return Course(
        concepts=concepts,
        curriculum=curriculum,
        lessons=lessons,
        assessment=assessment,
    )


def extract_concepts(source: str, model: BaseChatModel) -> ConceptSet:
    """Stage 1: turn unstructured source text into a validated ConceptSet."""

    stage = create_stage(CONCEPT_EXTRACTION_PROMPT, ConceptSet, model)
    return stage.invoke({"source": source})


def design_curriculum(concepts: ConceptSet, model: BaseChatModel) -> Curriculum:
    """Stage 2: organize Stage 1 concepts into a small learning sequence."""

    stage = create_stage(CURRICULUM_PROMPT, Curriculum, model)
    return stage.invoke({"concepts": concepts.model_dump_json(indent=2)})


def generate_lessons(
    concepts: ConceptSet,
    curriculum: Curriculum,
    model: BaseChatModel,
) -> LessonSet:
    """Stage 3: write lessons using the validated concepts and curriculum."""

    stage = create_stage(LESSON_PROMPT, LessonSet, model)
    return stage.invoke(
        {
            "concepts": concepts.model_dump_json(indent=2),
            "curriculum": curriculum.model_dump_json(indent=2),
        }
    )


def generate_assessment(
    curriculum: Curriculum,
    lessons: LessonSet,
    model: BaseChatModel,
) -> Assessment:
    """Stage 4: build assessment questions from the material actually taught."""

    stage = create_stage(ASSESSMENT_PROMPT, Assessment, model)
    return stage.invoke(
        {
            "curriculum": curriculum.model_dump_json(indent=2),
            "lessons": lessons.model_dump_json(indent=2),
        }
    )


def create_stage(
    prompt_text: str,
    output_schema: type[BaseModel],
    model: BaseChatModel,
):
    """Create one LangChain stage with native structured output.

    Each stage follows the same small pattern:

        PromptTemplate
              ↓
        ChatModel + JSON Schema
              ↓
        validated Pydantic object

    ``with_structured_output`` sends the Pydantic schema as part of the model
    request instead of merely asking for JSON in the prompt. ``strict=True``
    tells OpenRouter/model providers that the response must conform exactly to
    that schema.

    OpenRouter routing is configured in ``main.py`` with
    ``require_parameters=True`` so requests are only sent to provider endpoints
    that support the parameters CourseForge requires.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", prompt_text),
        ]
    )

    structured_model = model.with_structured_output(
        output_schema,
        method="json_schema",
        strict=True,
    )

    # LCEL: the prompt feeds a model that returns the Pydantic object directly.
    return prompt | structured_model
