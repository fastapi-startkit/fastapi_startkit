from pathlib import Path

from fastapi_startkit import Application
from fastapi_startkit.logging import LogProvider
from fastapi_startkit.skills import AISkillProvider

from config.fastapi import FastAPIConfig
from providers.fastapi_provider import FastapiProvider

providers = [
    AISkillProvider,
    LogProvider,
    (FastapiProvider, FastAPIConfig),
]

app: Application = Application(
    base_path=Path(__file__).resolve().parent.parent,
    providers=providers,
)
