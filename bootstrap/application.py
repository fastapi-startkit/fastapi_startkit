from pathlib import Path

from fastapi_startkit import Application
from fastapi_startkit.logging import LogProvider

from config.fastapi import FastAPIConfig
from providers.fastapi_provider import FastapiProvider
from fastapi_startkit.skills import AISkillProvider

app: Application = Application(
    base_path=Path(__file__).resolve().parent.parent,
    providers=[
        AISkillProvider,
        LogProvider,
        (FastapiProvider,FastAPIConfig)
    ]
)
