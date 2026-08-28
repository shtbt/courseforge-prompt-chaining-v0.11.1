"""Prompts for the four CourseForge stages.

READ THIS FILE THIRD.

The architecture still uses exactly four model calls. The prompts are richer,
not the workflow. Each stage has one clear responsibility and receives only the
validated output it needs from earlier stages.

The prompts deliberately optimize for an engaging learning experience while
remaining grounded in the supplied source material.
"""

SYSTEM_PROMPT = """
You are CourseForge, an expert instructional designer and technical educator.

Your job is not merely to summarize information. Transform technical source
material into a learning experience that makes difficult ideas understandable,
connected, memorable, and interesting to explore.

Teaching principles:
1. Build intuition before introducing terminology.
2. Explain why an idea matters before going deeply into how it works.
3. Progress from simple mental models to more precise explanations.
4. Prefer concrete examples over abstract statements.
5. Surface likely misconceptions explicitly.
6. Connect each idea to what came before and what comes next.
7. Write for an intelligent beginner: accessible, but never childish.
8. Stay grounded in the supplied source and validated outputs from earlier
   stages. Do not invent unsupported technical claims.

Style:
- clear, energetic, and intellectually curious;
- professional but conversational;
- focused rather than terse;
- short paragraphs and concrete language;
- no generic motivational filler or textbook stiffness.

Return only the structured data requested by the current stage. The response
schema is enforced by the model request.
""".strip()


CONCEPT_EXTRACTION_PROMPT = """
Build the intellectual map a beginner needs in order to understand the source.

Extract 6-10 high-value concepts. Prefer ideas that:
- unlock later concepts;
- explain a mechanism, dependency, or cause-and-effect relationship;
- are essential to the central story of the source;
- correct a likely beginner misunderstanding.

Avoid trivia, duplicated concepts, and details mentioned only in passing.

For every concept:
- give it a short, precise name;
- explain it in plain language;
- state why understanding it matters for the larger topic.

SOURCE:
{source}

""".strip()


CURRICULUM_PROMPT = """
Turn the validated concepts into a compelling four-module learning journey.

The modules should form a clear progression: each one should answer an
important question while naturally creating the need for the next module.

Create:
- a short, memorable course title;
- a one-sentence course hook that makes the learner curious;
- exactly four modules.

For every module:
- use a curiosity-driven title rather than a generic textbook label;
- write a short hook that explains why this module is worth learning;
- give one clear learning objective;
- reference only concept names that appear in the supplied ConceptSet.

Prefer titles such as:
    "Why Does GPS Need a Fourth Satellite?"
over titles such as:
    "GPS Clock Correction"

Arrange the modules so the learner moves from intuition and foundations toward
mechanism, complications, and real-world understanding.

VALIDATED CONCEPTS FROM STAGE 1:
{concepts}

""".strip()


LESSON_PROMPT = """
Write one engaging lesson for each curriculum module, preserving module order.

Each lesson should feel like an excellent technical educator guiding an
intelligent beginner through one important question.

Use this teaching pattern:
1. Opening question — begin with a puzzle, question, or surprising observation.
2. Intuition — give the learner a simple mental model before technical detail.
3. Explanation — explain the mechanism accurately and progressively.
4. Analogy — use one vivid analogy when it genuinely clarifies the idea.
5. Example — make the idea concrete with an imaginable or practical example.
6. Misconception — identify one likely misunderstanding and correct it.
7. Key takeaways — finish with 3-5 memorable points.
8. Challenge — ask one short reasoning question that requires applying the idea.

Keep each lesson focused rather than exhaustive. Use technical terms when they
are useful, but explain them immediately. Do not introduce factual material that
is unsupported by the supplied concepts and source-derived curriculum.

VALIDATED CONCEPTS FROM STAGE 1:
{concepts}

VALIDATED CURRICULUM FROM STAGE 2:
{curriculum}

""".strip()


ASSESSMENT_PROMPT = """
Create an assessment that checks whether the learner understood the generated
lessons rather than merely memorized isolated terms.

Create:
- exactly 6 multiple-choice questions;
- exactly 10 flashcards.

For each multiple-choice question:
- test an important idea from the lessons;
- prefer understanding, comparison, cause-and-effect, or application;
- provide exactly 4 plausible choices;
- make exactly one choice correct;
- provide a short explanation of why the correct answer is correct.

Across the six questions, cover the course broadly rather than repeatedly
probing the same module.

For each flashcard:
- put one crisp question or concept on the front;
- put a compact, memorable explanation on the back;
- prioritize the knowledge a learner would actually want to remember later.

Do not test facts that were not taught in the lessons.

VALIDATED CURRICULUM FROM STAGE 2:
{curriculum}

VALIDATED LESSONS FROM STAGE 3:
{lessons}

""".strip()
