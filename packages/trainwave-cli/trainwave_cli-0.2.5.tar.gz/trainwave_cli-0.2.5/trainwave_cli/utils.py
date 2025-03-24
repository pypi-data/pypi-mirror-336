import asyncio
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import TypeVar

import typer
from dacite import from_dict as dacite_from_dict
from dacite.config import Config

from trainwave_cli.config.config import config


def has_running_event_loop() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        # No running event loop in this thread
        return False


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if has_running_event_loop():
            return f(*args, **kwargs)

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(f(*args, **kwargs))
            finally:
                loop.close()
        except RuntimeError as e:
            if "Event loop is closed" in str(e):
                # Create a new event loop for testing environments
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(f(*args, **kwargs))
                finally:
                    loop.close()
            raise

    return wrapper


def ensure_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if config.api_key in {"", None}:
            typer.echo(
                "No access token found. Please run `trainwave auth login` to login to your account."
            )
            raise typer.Exit(1)
        return f(*args, **kwargs)

    return wrapper


def truncate_string(s: str, max_len: int) -> str:
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


T = TypeVar("T")


def from_dict(data_class: type[T], data: dict) -> T:
    """Recursively constructs a dataclass from a nested dictionary, skipping unmatched fields."""
    return dacite_from_dict(
        data_class,
        data,
        config=Config(cast=[Enum], type_hooks={datetime: datetime.fromisoformat}),
    )
