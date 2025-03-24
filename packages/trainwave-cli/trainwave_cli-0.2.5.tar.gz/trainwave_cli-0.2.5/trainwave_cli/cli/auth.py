import time
import webbrowser
from typing import Annotated

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from trainwave_cli.api import Api, CLIAuthStatus
from trainwave_cli.config.config import config, config_manager
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()

_BOLD = "\033[1m"
_RESET = "\033[0;0m"

LOGIN_POLLING_TIME: Annotated[int, "minutes"] = 5
LOGIN_POLLING_SLEEP_TIME: Annotated[int, "seconds"] = 5


@app.command()
@async_command
async def login() -> None:
    """
    Login to Trainwave.

    This will open a browser window for you to authenticate.
    """
    api_client = Api(None, config.endpoint)
    session_url, session_token = await api_client.create_cli_auth_session()

    typer.echo("Opening your browser to complete the login.\n")
    typer.echo(f"{_BOLD}URL:{_RESET} {session_url} \n")

    webbrowser.open_new_tab(session_url)

    api_token: str | None = None
    end_polling_at = time.time() + 60 * LOGIN_POLLING_TIME

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Awaiting login...", total=None)

        while time.time() < end_polling_at:
            status, api_token = await api_client.check_cli_auth_session_status(
                session_token
            )
            if status == CLIAuthStatus.SUCCESS:
                break

            time.sleep(LOGIN_POLLING_SLEEP_TIME)

        if api_token:
            # Test the token
            api = Api(api_token, config.endpoint)
            user = await api.get_myself()

            typer.echo("\n")
            typer.echo("✅ Success!\n")
            typer.echo(f"Logged in as: {_BOLD}{user.email}{_RESET}")

            config.api_key = api_token
            config_manager.save()
        else:
            typer.echo("❌ Something went wrong. Try again.")


@app.command()
@async_command
@ensure_api_key
async def logout() -> None:
    """
    Logout from Trainwave.

    This will remove the API key from the configuration.
    """
    config.api_key = None
    config_manager.save()
    config_manager.delete()
    typer.echo("Logged out")


@app.command()
@async_command
@ensure_api_key
async def whoami() -> None:
    """Show the current user's information."""
    api_client = Api(config.api_key, config.endpoint)
    user = await api_client.get_myself()
    typer.echo(user.email)


@app.command()
@async_command
async def set_token(api_key: str) -> None:
    """Set the API key for Trainwave."""
    typer.echo("Checking API key...")
    api_client = Api(api_key, config.endpoint)
    if await api_client.check_api_key():
        config.api_key = api_key
        config_manager.save()
        typer.echo("API key is valid!")
    else:
        typer.echo("API key is invalid")


@app.command()
def token() -> None:
    """Show the current API key."""
    typer.echo(config.api_key)


@app.command()
def set_endpoint(endpoint: str) -> None:
    """Set the API endpoint for Trainwave."""
    config.endpoint = endpoint
    config_manager.save()
    typer.echo(f"Endpoint set to {endpoint}")
