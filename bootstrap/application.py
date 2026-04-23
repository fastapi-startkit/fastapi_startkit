from pathlib import Path

from fastapi_startkit import Application
from fastapi_startkit.logging import LogProvider
from providers.fastapi_provider import FastapiProvider

app: Application = Application(
    base_path=str(Path().cwd()),
    providers=[
        LogProvider,
        FastapiProvider
    ]
)
