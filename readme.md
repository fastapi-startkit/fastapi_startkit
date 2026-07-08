# FastAPI StartKit

FastAPI StartKit is a modular, provider-driven framework for building robust FastAPI applications with minimal boilerplate. That said, it doesn't lock you into FastAPI at all — you can build entirely headless CLI utilities, cron scripts, or background task workers and still get the full suite of infrastructure components: logging, database, configuration, and dependency injection.

[Full Documentation](https://fastapi-startkit.github.io/docs/fastapi.html)

## Quick Start

```shell
git clone https://github.com/fastapi-startkit/fastapi_startkit example-app
cd example-app
cp .env.example .env
uv sync
uv run python artisan serve
```

Then open [http://127.0.0.1:7654](http://127.0.0.1:7654) in your browser.

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
