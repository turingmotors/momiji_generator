from typing import Any, IO
from tqdm import tqdm
from .modules.record_processor import RecordProcessor
from .modules.file_manager import FileManager
from src.config import Config


def _process_and_write_record(
    record: dict[str, Any],
    file_object: IO[str],
    verbose: bool,
    file_manager: FileManager,
) -> bool:
    """
    Processes a single record and writes it to the provided file object.
    Returns True if the record was successfully processed and written, False otherwise.

    Args:
        record (dict[str, Any]): The record to process.
        file_object (IO[str]): The file object to write to.
        verbose (bool): Enables verbose logging for the processor.
        file_manager (FileManager): Instance of FileManager to handle file operations.

    Returns:
        bool: True if the content was parsed and written, False otherwise.
    """
    processor = RecordProcessor(record, verbose=verbose)
    parsed_content = processor.generate_content()
    if parsed_content:
        file_manager.write_json_line(file_object, parsed_content)
        return True
    return False


def process_records_from_jsonl(
    input_filepath: str, output_filepath: str, verbose: bool, limit: int | None = None
) -> dict[str, int]:
    """
    Extracts main content from Japanese web pages in WARC files
    and writes them to a JSONL file directly, returning processing statistics.

    Args:
        input_filepath (str): Path to the gzipped JSONL input file.
        output_filepath (str): Path to the JSONL output file.
        verbose (bool): Enables verbose logging.
        limit (int | None, optional): Maximum number of records to process. Defaults to None (no limit).

    Returns:
        dict[str, int]: A dictionary containing processing statistics,
                        specifically `processed_records` and `failed_records` counts.
    """
    file_manager = FileManager(tmp_dir=".")
    successful_processing_count = 0
    failed_processing_count = 0

    with open(output_filepath, "w", encoding=Config.DEFAULT_ENCODING) as fo:
        records_iterable = file_manager.extract_records_from_jsonl(
            input_filepath, limit=limit
        )
        for record in tqdm(records_iterable, desc="Processing records"):
            if _process_and_write_record(record, fo, verbose, file_manager):
                successful_processing_count += 1
            else:
                failed_processing_count += 1

    return {
        "processed_records": successful_processing_count,
        "failed_records": failed_processing_count,
    }
