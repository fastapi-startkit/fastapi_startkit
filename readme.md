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

Skills teach AI agents (Claude Code, Gemini) this project's conventions.

List providers that declare skills:

```shell
uv run python artisan ai:skills
```

Publish stubs and sync them to AI agents:

```shell
uv run python artisan ai:skills --sync
```
