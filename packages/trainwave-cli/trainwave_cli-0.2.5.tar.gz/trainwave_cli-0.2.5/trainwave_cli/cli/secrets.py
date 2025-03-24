import builtins
import sys
from datetime import datetime, timezone
from operator import itemgetter
from typing import Annotated

import human_readable
import typer
from tabulate import tabulate
from typer_config.decorators import use_toml_config

from trainwave_cli.api import Api, Secret
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def list(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
) -> None:
    """List all secrets."""
    try:
        api_client = Api(config.api_key, config.endpoint)
        secrets = await api_client.list_secrets(organization)

        project_scoped = [secret for secret in secrets if secret.project]
        org_scoped = [secret for secret in secrets if not secret.project]
        unique: dict[str, tuple[bool, Secret]] = {}

        for org_secret in org_scoped:
            unique[org_secret.name] = (False, org_secret)

        for project_secret in project_scoped:
            if project_secret.name in unique:
                unique[project_secret.name] = (True, project_secret)
            else:
                unique[project_secret.name] = (False, project_secret)

        sorted_secrets = dict(sorted(unique.items(), key=itemgetter(0)))

        headers = ["ID", "NAME", "SCOPE", "DIGEST", "CREATED"]
        table = [
            [
                secret.rid,
                secret.name if not overridden else f"{secret.name} (*)",
                "PROJECT" if secret.project else "ORG",
                secret.digest[:16],
                human_readable.date_time(
                    datetime.now(timezone.utc) - secret.created_at
                ),
            ]
            for _, (overridden, secret) in sorted_secrets.items()
        ]

        typer.echo(tabulate(table, headers=headers, tablefmt="grid"))
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def set(
    secrets: Annotated[
        builtins.list[str],
        typer.Argument(help="Secrets to set in the format KEY=VALUE"),
    ],
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    project: Annotated[str | None, typer.Option(help="The project ID or RID")] = None,
) -> None:
    """Set secrets for an organization or project."""
    try:
        # Parse secrets
        secrets_dict = {}
        for secret in secrets:
            if "=" not in secret:
                typer.echo(f"Error: Invalid secret format: {secret}")
                sys.exit(1)
            key, value = secret.split("=", 1)
            secrets_dict[key] = value

        # Set secrets
        api_client = Api(config.api_key, config.endpoint)
        await api_client.set_secrets(organization, secrets_dict, project)
        typer.echo("Secrets set successfully")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def unset(
    secrets: Annotated[builtins.list[str], typer.Argument(help="Secrets to unset")],
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    project: Annotated[str | None, typer.Option(help="The project ID or RID")] = None,
) -> None:
    """Unset secrets for an organization or project."""
    try:
        # Check if secrets exist
        api_client = Api(config.api_key, config.endpoint)
        existing_secrets = await api_client.list_secrets(organization)
        existing_names = {secret.name for secret in existing_secrets}

        # Check for nonexistent secrets
        nonexistent = [secret for secret in secrets if secret not in existing_names]
        if nonexistent:
            typer.echo(f"Error: Secrets not found: {', '.join(nonexistent)}")
            sys.exit(1)

        # Unset secrets
        await api_client.unset_secrets(organization, secrets)
        typer.echo("Secrets unset successfully")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
