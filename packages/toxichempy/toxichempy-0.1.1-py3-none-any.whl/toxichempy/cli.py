import sys
from typing import Optional

import typer
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typer.main import get_command

from toxichempy import __version__
from toxichempy.pipeline_framework.aop_data import \
    app as build_predictive_aop_data
from toxichempy.pipeline_framework.bioassay_data_for_ml import \
    app as build_bioassay_ML_data

console = Console()
app = typer.Typer(
    # help="ToxiChemPy - Bioassay Preparation Tool for ML",
    no_args_is_help=True,  # ensures 'toxichempy' alone triggers help
    rich_markup_mode="rich",
)

# Add your subcommands
app.add_typer(
    build_bioassay_ML_data,
    name="bioassay_ml_data",
    help="Run bioassay data preparation pipeline",
)
app.add_typer(
    build_predictive_aop_data,
    name="predictive_aop_data",
    help="Predictive adverse outcome pathway data preparation pipeline",
)


def get_custom_help_panel() -> Panel:
    body = Text(justify="left")
    body.append("Developer & Maintainer: ", style="bold blue")
    body.append("Deepak Kumar Sachan,CSIR-IITR\n", style="bold")
    body.append("Email: ctf.csir.iitr@gmail.com\n\n")
    body.append("Supervisor: ", style="bold blue")
    body.append("Dr. Parthasarathi Ramakrishnan, CSIR-IITR\n", style="bold")
    body.append("Email: partha.ram@iitr.res.in")

    return Align.center(
        Panel.fit(
            body,
            title="Welcome to ToxiChemPy",
            subtitle=f"Version: {__version__}",
            title_align="center",
            border_style="red",
            padding=(1, 2),
            box=box.ROUNDED,
        )
    )


# 📦 Handle `--help` and `--version`
@app.callback(invoke_without_command=True)
def cli_main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show version", is_eager=True
    ),
    help: Optional[bool] = typer.Option(
        None, "--help", "-h", help="Show this message and exit", is_eager=True
    ),
):
    if version:
        console.print(f"[bold magenta]ToxiChemPy v{__version__}[/bold magenta]")
        raise typer.Exit()

    if help or ctx.invoked_subcommand is None:
        console.print(get_custom_help_panel())
        cli = get_command(app)
        console.print(cli.get_help(ctx))
        raise typer.Exit()


# 🔧 Fallback for direct call with no args
def main():
    if len(sys.argv) == 1:
        # Same behavior as `--help`
        ctx = typer.Context(get_command(app))
        console.print(get_custom_help_panel())
        console.print(get_command(app).get_help(ctx))
    else:
        app()


if __name__ == "__main__":
    main()
