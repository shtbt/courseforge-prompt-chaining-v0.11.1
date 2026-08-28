"""Small tests for the architecture, not a separate testing showcase."""

from app import chain
from app.exporter import to_markdown
from app.schemas import (
    Assessment,
    Concept,
    ConceptSet,
    Course,
    Curriculum,
    Flashcard,
    Lesson,
    LessonSet,
    Module,
    Question,
)


def sample_course_parts():
    """Create compact valid objects for architecture and exporter tests."""

    concepts = ConceptSet(
        concepts=[
            Concept(
                name="Trilateration",
                explanation="Position from distances to known reference points.",
                why_it_matters="It is the geometric core of GPS positioning.",
            )
        ]
    )
    curriculum = Curriculum(
        course_title="How GPS Finds You",
        course_hook="Turn invisible radio signals into a position on Earth.",
        modules=[
            Module(
                title="How Can a Satellite Measure Distance?",
                hook="Timing turns a radio signal into a ruler.",
                objective="Understand how signal travel time gives distance.",
                concepts=["Trilateration"],
            )
        ],
    )
    lessons = LessonSet(
        lessons=[
            Lesson(
                title="Measuring Space with Time",
                opening_question="How can a clock act like a ruler?",
                intuition="Measure how long a signal spends travelling.",
                explanation="Distance follows from travel time and signal speed.",
                analogy="It is like estimating a storm's distance from thunder delay.",
                example="A GPS receiver compares transmit and receive times.",
                misconception="GPS primarily measures distances, not viewing angles.",
                key_takeaways=[
                    "Signals carry precise timing information.",
                    "Travel time can be converted into distance.",
                    "Several distances are needed for position.",
                ],
                challenge="Why would a tiny clock error matter so much?",
            )
        ]
    )
    assessment = Assessment(
        questions=[
            Question(
                question="What does GPS primarily infer from signal travel time?",
                choices=["Distance", "Angle", "Temperature", "Altitude only"],
                answer="Distance",
                explanation="Known signal speed converts travel time into distance.",
            )
        ],
        flashcards=[
            Flashcard(
                front="What is trilateration?",
                back="Finding position from distances to known reference points.",
            )
        ],
    )
    return concepts, curriculum, lessons, assessment


def test_run_chain_passes_validated_outputs_between_stages(monkeypatch):
    """The core contract: the four stages run in order and feed one another."""

    concepts, curriculum, lessons, assessment = sample_course_parts()
    calls: list[str] = []

    monkeypatch.setattr(
        chain,
        "extract_concepts",
        lambda source, model: calls.append("concepts") or concepts,
    )
    monkeypatch.setattr(
        chain,
        "design_curriculum",
        lambda received, model: (
            calls.append("curriculum")
            or (curriculum if received is concepts else None)
        ),
    )
    monkeypatch.setattr(
        chain,
        "generate_lessons",
        lambda received_concepts, received_curriculum, model: (
            calls.append("lessons")
            or (
                lessons
                if received_concepts is concepts and received_curriculum is curriculum
                else None
            )
        ),
    )
    monkeypatch.setattr(
        chain,
        "generate_assessment",
        lambda received_curriculum, received_lessons, model: (
            calls.append("assessment")
            or (
                assessment
                if received_curriculum is curriculum and received_lessons is lessons
                else None
            )
        ),
    )

    result = chain.run_chain("source", model=object())

    assert isinstance(result, Course)
    assert calls == ["concepts", "curriculum", "lessons", "assessment"]
    assert result.concepts is concepts
    assert result.curriculum is curriculum
    assert result.lessons is lessons
    assert result.assessment is assessment


def test_markdown_uses_the_richer_course_structure():
    """The deterministic exporter should expose the engaging lesson sections."""

    concepts, curriculum, lessons, assessment = sample_course_parts()
    course = Course(
        concepts=concepts,
        curriculum=curriculum,
        lessons=lessons,
        assessment=assessment,
    )

    markdown = to_markdown(course)

    assert "# How GPS Finds You" in markdown
    assert "## Course Map" in markdown
    assert "### Start with this question" in markdown
    assert "### Common misconception" in markdown
    assert "## Knowledge Check" in markdown
    assert "## Flashcards" in markdown
