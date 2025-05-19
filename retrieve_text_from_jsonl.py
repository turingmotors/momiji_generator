import logging
import argparse

from src.extract_text_from_jsonl import process_records_from_jsonl

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def retrieve_text_from_jsonl(
    input_path: str, output_path: str, limit: int | None = None
) -> dict[str, int]:
    """Processes a single S3 object: downloads, extracts text, and uploads result."""
    return process_records_from_jsonl(
        input_path, output_path, verbose=False, limit=limit
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSONL files.")
    parser.add_argument(
        "--input_path", type=str, required=True, help="Path to the JSONL file."
    )
    parser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output file."
    )
    parser.add_argument(
        "--limit", type=int, help="Limit the number of records to process."
    )
    args = parser.parse_args()

    logger.info("Starting JSONL file processing...")
    result = retrieve_text_from_jsonl(args.input_path, args.output_path, args.limit)
    logger.info("Processing finished: %s", result)
