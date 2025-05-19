import json
from typing import Any
import gzip
import logging

from src.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FileManager:
    """
    Handles local file operations, including path generation, compression, and cleanup.
    """

    def __init__(self, tmp_dir):
        """
        Initializes the FileManager with a temporary directory.

        Args:
            tmp_dir (str): Path to the temporary directory.
        """
        self.tmp_dir = tmp_dir

    def write_json_line(self, file_object: Any, data: dict[str, Any]) -> None:
        """
        Writes a single JSON line to the provided file object.

        Args:
            file_object (Any): The file object to write to.
            data (dict[str, Any]): The data to write as a JSON line.
        """
        json_line = json.dumps(data, ensure_ascii=False)
        file_object.write(json_line + "\n")

    def extract_records_from_jsonl(
        self, filepath: str, limit: int | None = None
    ) -> Any:  # Iterator[dict[str, Any]]
        """
        Extracts records from a gzipped JSONL file.

        Args:
            filepath (str): Path to the gzipped JSONL file.
            limit (int | None, optional): Maximum number of records to extract. Defaults to None (no limit).

        Returns:
            Iterator[dict[str, Any]]: An iterator over JSON objects in the JSONL file.
        """
        with gzip.open(filepath, "rt", encoding=Config.DEFAULT_ENCODING) as file:
            for i, line in enumerate(file):
                if limit is not None and i >= limit:
                    break
                yield json.loads(line)
