"""Console script for shoestring_assembler."""

import shoestring_assembler as shoestring_assembler_top
from shoestring_assembler import assembler, display

import typer
from typing_extensions import Annotated
import os
import sys

from rich.prompt import Prompt, Confirm

typer_app = typer.Typer(name="Shoestring Assembler", no_args_is_help=True)


CANCEL_PHRASE = "cancel"


@typer_app.command()
def update(
    version: Annotated[
        str, typer.Argument(help="Update to this version. (optional)")
    ] = "",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes", "-y", help="Automatically download and assemble the latest version"
        ),
    ] = False,
    recipe: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
):
    """
    Updates the solution to the specified version. If a version is not specified - it lists the available versions that you can choose from.
    """
    if verbose:
        display.debug = True

    display.print_top_header("Updating Solution")

    assembler.git_fetch_current()

    if not version:
        has_update, available_versions = assembler.git_check_update()
        if not has_update:
            display.print_notification("Latest version installed.")
            return
        else:
            display.print_notification("A new version is available.")
            if yes:
                version = available_versions[0]
            elif Confirm.ask("? Do you want to update now?", default=True):
                selected_version = Prompt.ask(
                    "? Select a version?",
                    choices=available_versions
                    + [
                        CANCEL_PHRASE,
                    ],
                    default=available_versions[0],
                )
                if selected_version != CANCEL_PHRASE:
                    version = selected_version

    if version:
        updated = assembler.git_update(version)
        if updated:
            if yes or Confirm.ask(
                "? Do you want to assemble the solution now?", default=True
            ):
                try:
                    assemble(recipe)
                    return
                except SystemExit:
                    display.print_error(
                        "Solution assembly failed. If you want to run it again use: [green]shoestring assemble[/green]"
                    )
                    raise
    else:
        display.print_log(
            "If you want to update later - run: [green]shoestring update <version>[/green]"
        )

    display.print_top_header("Finished")


@typer_app.command()
def check_recipe(
    recipe: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
):
    display.print_top_header("Checking Recipe")
    assembler_inst = assembler.Assembler(recipe)
    assembler_inst.load_recipe()
    display.print_top_header("Finished")


@typer_app.command()
def bootstrap(
    recipe: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Uses templates to bootstrap the solution config for the specified sources
    """
    pass


@typer_app.command()
def assemble(
    recipe: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    download: bool = True,
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Assembles the solution using the provided recipe
    """
    if verbose:
        display.debug = True
    display.root_console.record = True
    try:
        display.print_top_header("Assembling Solution")
        assembler_inst = assembler.Assembler(recipe)
        assembler_inst.load_recipe()
        assembler_inst.clean(clean_sources=download)
        assembler_inst.verify_filestructure(check_sources=not download)
        assembler_inst.gather_base_service_modules(do_gather=download)
        assembler_inst.check_user_config()
        assembler_inst.generate_compose_file()
        display.print_top_header("Finished")
        display.print_next_steps("* Configure the service modules according to your needs (refer to the guide for details) \n\n* Once the solution is ready - run [white]shoestring build[/white] to build the solution")
    finally:
        display.root_console.save_html("./console.log")


import urllib
import yaml
from rich.prompt import Prompt
import rich.progress
import subprocess
from .solution_picker import SolutionPickerApp


# Temporary implementation - refactor once proof-of-concept complete
@typer_app.command()
def get(
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Downloads the specified solution
    """
    if verbose:
        display.debug = True

    display.print_top_header("Get Solution")

    display.print_header(f"Selecting Solution")
    # fetch solution list
    list_branch = os.getenv("SHOESTRING_LIST_BRANCH","main")
    with urllib.request.urlopen(
        f"https://github.com/DigitalShoestringSolutions/solution_list/raw/refs/heads/{list_branch}/list.yaml"
    ) as web_in:
        content = web_in.read()
        provider_list = yaml.safe_load(content)

    selected = SolutionPickerApp(provider_list).run()

    if selected == None:
        display.print_log("Solution selection cancelled")
    else:
        display.print_log(f"Selected [green]{selected['name']}[/green]")

        display.print_header(f"Downloading {selected['name']}")
        tag_or_branch = selected["tag"] if "tag" in selected else selected["branch"]

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        command = [
            "git",
            "clone",
            "--progress",  # force inclusion of progress updates
            "--branch",
            tag_or_branch,
            selected["url"],
        ]

        display.print_debug(f"command: {command}")

        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env
        )  # git outputs updates over stderr

        with rich.progress.Progress(transient=True) as progress:
            assembler.git_clone_progress_bars(process, progress, progress.console)

        if process.returncode == 0:
            display.print_complete("Done")
        else:
            display.print_error("Unable to download solution")
    display.print_top_header("Finished")

import select

@typer_app.command()
def build():
    display.print_top_header("Starting solution")
    command = ["docker", "compose", "build"]
    process = subprocess.Popen(
        command, stdout=None, stderr=None
    )
    process.wait()
    if process.returncode ==0:
        display.print_complete("Solution Built")
        display.print_next_steps("To run the solution use [white]shoestring start[/white]")
    else:
        display.print_error("Solution Building Failed")
    display.print_top_header("Finished")
    # buffer = bytearray()
    # while process.returncode == None:
    #     while True:
    #         out_line = None
    #         err_line = None

    #         read_list, _wlist, _xlist = select.select([process.stderr,process.stdout], [], [], 1)
    #         # display.print_log(read_list,console=console)
    #         if process.stderr in read_list:
    #             char = process.stderr.read(1)
    #             if char == b"\n":
    #                 err_line = buffer.decode()
    #                 buffer.clear()
    #             elif char:
    #                 # display.print_log(f"char: {char}", console=console)
    #                 buffer += char
    #             else:
    #                 break  # end of file
    #         if process.stdout in read_list:
    #             char = process.stdout.read(1)
    #             if char == b"\n":
    #                 out_line = buffer.decode()
    #                 buffer.clear()
    #             elif char:
    #                 # display.print_log(f"char: {char}", console=console)
    #                 buffer += char
    #             else:
    #                 break  # end of file
    #         else:
    #             break  # timeout - break to check if process terminated

    #         if out_line:
    #             display.print_log(f"[white]{out_line}")
    #         if err_line:
    #             display.print_error(f"{err_line}")

    #     process.poll()

@typer_app.command()
def start():
    display.print_top_header("Starting solution")
    command = ["docker", "compose", "up", "-d", "--remove-orphans"]
    process = subprocess.Popen(command, stdout=None, stderr=None)
    process.wait()

    if process.returncode ==0:
        display.print_complete("Solution is now running in the background")
    display.print_top_header("Finished")


@typer_app.callback(invoke_without_command=True)
def main(
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Assembler version")
    ] = False,
):
    if version:
        display.print_log(
            f"Shoestring Assembler version {shoestring_assembler_top.__version__}"
        )
    else:
        pass


def app():
    if os.geteuid() == 0:
        display.print_error(
            "To try prevent you from accidentally breaking things, this program won't run with sudo or as root! \nRun it again without sudo or change to a non-root user."
        )
        sys.exit(255)
    typer_app()


if __name__ == "__main__":
    app()


"""
* shoestring
    * bootstrap (maybe for a separate developer focussed tool?)
"""
