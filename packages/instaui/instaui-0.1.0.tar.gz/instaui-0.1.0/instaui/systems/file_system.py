import uuid
from pathlib import Path

from urllib.parse import quote as urllib_quote


def generate_hash_name_from_path(file_path: Path):
    path_str = str(file_path)
    unique_id = uuid.uuid5(uuid.NAMESPACE_URL, path_str)
    return str(unique_id)


def generate_static_url_from_file_path(file_path: Path):
    file_path = Path(file_path).resolve()
    return urllib_quote(
        f"/_instaui/static/{generate_hash_name_from_path(file_path)}/{file_path.name}"
    )
