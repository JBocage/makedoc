import click
import pathlib


@click.command("config")
@click.option(
    "-v",
    "verbose",
    is_flag=True,
    help="Sets verbosity",
)
@click.pass_context
def config(ctx, *args, **kwargs):
    """Gets config utilities"""

    autocomp_script = (
        pathlib.Path(__file__).resolve().absolute().parent
        / "bash_scripts/source_for_bash_completion.sh"
    )

    print(autocomp_script.__str__())
