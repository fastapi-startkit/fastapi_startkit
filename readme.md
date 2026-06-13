# FastAPI StartKit

FastAPI StartKit is a modular, provider-driven framework for building robust FastAPI applications with minimal boilerplate. That said, it doesn't lock you into FastAPI at all — you can build entirely headless CLI utilities, cron scripts, or background task workers and still get the full suite of infrastructure components: logging, database, configuration, and dependency injection.

[Full Documentation](https://fastapi-startkit.github.io/docs/fastapi.html)

## Quick Start

### 1. Clone the repository
```shell
git clone https://github.com/fastapi-startkit/fastapi_startkit example-app
cd example-app
cp .env.example .env
```

### 2. Install dependencies
```shell
uv sync
```

### 3. Run the application
```shell
uv run python artisan serve
```

## AI Skills

The application ships with **agent skills** — concise, framework-aware guides that teach AI
coding agents (Claude Code, Gemini) the conventions of this project: routing, controllers,
the ORM, requests, and the action pattern. They live alongside your providers and are
published into each agent's native format on demand.

### List skills
List every provider that declares skills (this is the default action):

```shell
uv run python artisan ai:skills
```

### Update & sync skills
Publish the skill stubs and sync them to the supported AI agents:

```shell
uv run python artisan ai:skills --sync
```

`--sync` regenerates each agent's skill files from the providers that declare them — for
example writing the Claude Code skill to `.claude/skills/<name>/SKILL.md` and the Gemini
equivalent. Run it after adding a new provider that declares a skill, or after editing an
existing skill, so every agent picks up the latest version.

> **Tip:** commit the generated skill files (e.g. `.claude/skills/`) so anyone who clones the
> project gets framework-aware AI assistance out of the box. Keep personal, machine-specific
> files like `.claude/settings.local.json` out of version control.
