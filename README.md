# CourseForge — Prompt Chaining

A small, professional, teaching-first project that transforms a technical source
primer into an engaging micro-course using **four fixed LLM stages**.

The goal is not to build a course platform. The goal is to make **Prompt
Chaining visible in real code** while producing an output that is useful enough
to feel real.

```text
source document
      ↓
1. Concept Extraction      → ConceptSet
      ↓
2. Curriculum Design       → Curriculum
      ↓
3. Lesson Generation       → LessonSet
      ↓
4. Assessment Generation   → Assessment
      ↓
Markdown + JSON
```

Python decides the sequence. The model does **not** choose the next step, route
the request, use tools, or loop until satisfied. CourseForge is therefore a
**workflow**, not an autonomous agent.

## Read the code in this order

The repository is intentionally designed to be read as teaching material.

1. **`main.py`** — see how configuration, input, workflow, and output connect.
2. **`app/chain.py`** — the architecture. Start with `run_chain()`.
3. **`app/prompts.py`** — see how each stage has a different teaching job.
4. **`app/schemas.py`** — inspect the typed contracts passed between stages.
5. **`app/exporter.py`** — see where LLM work ends and deterministic Python begins.

If you understand `main.py` and `run_chain()`, you already understand the core
architecture.

## Why four stages?

CourseForge intentionally stops at four LLM calls. Each call has a distinct
responsibility:

### 1. Concept Extraction

The raw source is converted into a compact intellectual map. Each concept has a
plain-language explanation and a reason it matters.

### 2. Curriculum Design

The validated concepts become a four-module learning journey with a compelling
course title, course hook, curiosity-driven module titles, and clear objectives.

### 3. Lesson Generation

Each module becomes an engaging lesson built around a repeatable teaching
pattern:

```text
opening question
      ↓
intuition
      ↓
explanation
      ↓
analogy
      ↓
concrete example
      ↓
misconception
      ↓
key takeaways
      ↓
challenge
```

### 4. Assessment Generation

The lessons become six understanding-focused multiple-choice questions with
explanations plus ten compact flashcards.

Course assembly and Markdown formatting are ordinary Python. They do not need
another model call.

## What changed in v0.11

v0.10 used `ChatOpenAI` with OpenRouter's OpenAI-compatible base URL. That can
work for ordinary chat completions, but it is a weaker fit for OpenRouter-specific
features such as provider routing and structured output.

v0.11 uses LangChain's dedicated `ChatOpenRouter` integration instead. Every
stage requests strict JSON Schema output, and the model is configured with
`openrouter_provider={"require_parameters": True}` so OpenRouter only routes
requests to provider endpoints that support the parameters CourseForge needs.

## Where LangChain fits

LangChain is deliberately used only inside each model stage:

```text
PromptTemplate → ChatModel + JSON Schema → Pydantic object
```

In LangChain Expression Language (LCEL):

```python
prompt | model.with_structured_output(Schema, method="json_schema")
```

The overall four-stage workflow remains ordinary Python. This keeps the
architecture readable instead of hiding it inside framework orchestration.

### Why native structured output?

Each stage uses:

```python
structured_model = model.with_structured_output(
    OutputSchema,
    method="json_schema",
    strict=True,
)

stage = prompt | structured_model
```

The schema is therefore part of the model request itself. CourseForge does not
ask for JSON in plain text and then hope the response can be parsed afterward.
With a Pydantic schema, LangChain returns a validated Pydantic object directly.

For OpenRouter, this also gives `openrouter/free` a structured-output capability
requirement that it can use when choosing a compatible free model. Free-model
availability can still change, so pin a specific compatible model when you need
repeatable demonstrations.

## Structured handoffs

The LLM does not pass arbitrary text directly from one stage to the next.
Each model request declares its Pydantic schema using LangChain structured output,
and the returned object is validated before the next stage receives it:

```text
ConceptSet
    ↓
Curriculum
    ↓
LessonSet
    ↓
Assessment
```

The richer fields improve the final learning experience without changing the
architecture. Because the schema is sent with the model request, this is more
reliable than asking the model for JSON in prompt text and parsing it afterward.

## Project structure

```text
courseforge-prompt-chaining/
├── main.py                  # Start here
├── app/
│   ├── chain.py             # ★ Prompt Chaining architecture
│   ├── prompts.py           # Four stage prompts
│   ├── schemas.py           # Typed handoffs
│   └── exporter.py          # Markdown / JSON output
├── examples/
│   ├── gps.md
│   ├── mrna_vaccines.md
│   ├── crispr.md
│   ├── jet_engine.md
│   └── public_key_cryptography.md
├── tests/
│   └── test_chain.py
├── output/
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── .env.example
└── README.md
```

There are no API routes, frontend, database, queue, vector store, LangGraph,
agents, tools, provider factories, service layers, or demo execution path. Those
would be useful in other projects, but they would not teach Prompt Chaining.

## Included source examples

The repository includes five technical primers that are long enough to produce
meaningful transformations while still being easy to inspect manually:

- **How GPS Works** — the default example;
- **How mRNA Vaccines Work**;
- **How CRISPR Gene Editing Works**;
- **How a Jet Engine Produces Thrust**;
- **How Public-Key Cryptography Works**.

To teach with another example, change `SOURCE_FILE` near the top of `main.py`.
That explicit edit is intentional; the project avoids a CLI framework so the
execution path remains obvious.

## Configure an LLM

Copy the environment template:

```bash
cp .env.example .env
```

CourseForge exposes a provider-neutral application contract:

```dotenv
LLM_API_KEY=sk-or-v1-your-key
LLM_MODEL=openrouter/free
```

The current implementation uses OpenRouter through LangChain's dedicated
`ChatOpenRouter` integration because it reliably exposes OpenRouter structured
output and provider-routing controls. The environment-variable names remain
generic because CourseForge conceptually depends on an **LLM**, not on the
provider name.

If you demonstrate another provider later, change only `create_model()` in
`main.py`; the four-stage Prompt Chaining architecture in `app/chain.py` does
not change.

## Run with uv

```bash
uv sync
uv run python main.py
```

CourseForge reads `examples/gps.md` by default and writes:

```text
output/course.md
output/course.json
```

The terminal keeps the chain visible:

```text
[1/4] Concept Extraction
      source → ConceptSet
      ✓ ... concepts

               ↓ ConceptSet

[2/4] Curriculum Design
      ConceptSet → Curriculum
      ✓ 4 modules

               ↓ Curriculum

[3/4] Lesson Generation
      ConceptSet + Curriculum → LessonSet
      ✓ 4 lessons

               ↓ LessonSet

[4/4] Assessment Generation
      Curriculum + LessonSet → Assessment
      ✓ 6 questions + 10 flashcards
```

## Run with Docker Compose

Docker Compose is not part of Prompt Chaining. It provides a reproducible path
for readers who do not want to install Python or project dependencies locally.

After creating `.env`:

```bash
docker compose run --rm courseforge
```

Compose mounts `./output`, so generated files remain on the host after the
container exits. That is its entire purpose here: **portable execution and
persistent output**, not artificial infrastructure.

## The architecture in code

The central function is intentionally plain:

```python
def run_chain(source, model):
    concepts = extract_concepts(source, model)
    curriculum = design_curriculum(concepts, model)
    lessons = generate_lessons(concepts, curriculum, model)
    assessment = generate_assessment(curriculum, lessons, model)

    return Course(
        concepts=concepts,
        curriculum=curriculum,
        lessons=lessons,
        assessment=assessment,
    )
```

This is the whole pattern: **decompose a complex task into focused model calls,
validate each result, then pass that result into the next predefined step.**

## Why the output is richer without a more complex architecture

The project does not add evaluator loops or extra generation stages. Instead,
each existing stage has a stronger contract:

```text
Concept
  ├─ name
  ├─ explanation
  └─ why_it_matters

Module
  ├─ title
  ├─ hook
  ├─ objective
  └─ concepts

Lesson
  ├─ opening_question
  ├─ intuition
  ├─ explanation
  ├─ analogy
  ├─ example
  ├─ misconception
  ├─ key_takeaways
  └─ challenge

Assessment
  ├─ questions + explanations
  └─ flashcards
```

This is an important design lesson on its own: **better prompts and better
contracts can improve output quality without adding architectural complexity.**

## Tests

Tests stay intentionally small:

```bash
uv run pytest
uv run ruff check .
```

`tests/test_chain.py` verifies the most important architectural property—the
four stages execute in order and pass their validated outputs forward—and also
checks that the deterministic Markdown exporter exposes the richer course
structure.

## Why this design is intentionally small

Professional code does not require many layers. In CourseForge, professionalism
comes from:

- clear responsibilities;
- typed stage boundaries;
- grounded, purpose-built prompts;
- explicit configuration;
- focused tests;
- reproducible `uv` and Docker execution;
- deterministic export code;
- documentation that mirrors the implementation.

The project deliberately avoids abstractions that would make it look more
enterprise-like while making Prompt Chaining harder to see.
