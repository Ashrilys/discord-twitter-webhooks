import os
from functools import lru_cache
from pathlib import Path

from loguru import logger
from reader import (
    Reader,
    make_reader,
)


@lru_cache
def get_reader(custom_location: Path | None = None) -> Reader:
    """Get the reader.

    Args:
        custom_location: The location of the database file.

    """
    data_dir: Path = get_data_location()
    db_location: Path = custom_location or Path(data_dir) / "discord_twitter_webhooks.sqlite3"

    return make_reader(url=str(db_location))


def get_data_location() -> Path:
    """Get the data location where the database file is stored.

    Raises:
        NotImplementedError: The OS is not supported.

    Returns:
        Path: The path to the data directory.
    """
    if os.name == "nt":
        # C:\Users\username\AppData\Roaming
        default_data_dir: Path = Path.home() / "AppData" / "Roaming"
        data_dir: Path = Path(os.environ.get("APPDATA", default_data_dir)) / "discord_twitter_webhooks"
    elif os.name == "posix":
        # /home/username/.local/share
        default_data_dir: Path = Path.home() / ".local" / "share"
        data_dir: Path = Path(os.environ.get("XDG_DATA_HOME", default_data_dir)) / "discord_twitter_webhooks"
    else:
        msg: str = (
            f"Unsupported OS: {os.name}, please open an issue on GitHub, email me at tlovinator@gmail.com or DM me on"
            " Discord at TheLovinator#9276"
        )
        raise NotImplementedError(msg)

    # Create the data directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Data will be stored in {data_dir}")
    return data_dir


@lru_cache
def init_reader(db_location: Path | None = None) -> Reader | None:
    """Create the Reader.

    This function is used to create the Reader and handle any errors
    that may occur.

    Args:
        db_location: Where to store the database.

    Raises:
        StorageError: An error occurred while connecting to storage
        while creating the Reader database.
        SearchError: An error occurred while enabling/disabling search.
        InvalidPluginError: An error occurred while loading plugins.
        PluginInitError: A plugin failed to initialize.
        PluginError: An ambiguous plugin-related error occurred.
        ReaderError: An ambiguous exception occurred while creating
        the reader.

    Returns:
        Reader: The Reader if no errors occurred.
    """
    db_location = get_data_location() if db_location is None else db_location
    db_file: Path = db_location / "discord_twitter_webhooks.db"
    reader: Reader = make_reader(url=str(db_file), search_enabled=False)
    return reader
