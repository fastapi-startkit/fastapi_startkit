from cleo import Application
from clikit.args import ArgvArgs
from masoniteorm.commands import MigrateCommand, SeedRunCommand, MakeMigrationCommand
from typer import Typer

app = Typer()
cleo = Application()

cleo.add(MakeMigrationCommand())
cleo.add(MigrateCommand())
cleo.add(SeedRunCommand())

@app.command()
def migrate():
    args = ArgvArgs(["", 'migrate'])
    cleo.run(args)

@app.command()
def seed():
    args = ArgvArgs(["", 'seed:run', 'DatabaseSeeder'])
    cleo.run(args)

@app.command("make:migration")
def make(name: str):
    args = ArgvArgs(["", 'migration', name])
    cleo.run(args)
