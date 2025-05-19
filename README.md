# momiji_generator

## Overview

`momiji_generator` is a Python tool designed to process and generate image-text interleaved data. It can extract textual information (specifically `text` and `text_list` fields) from the [MOMIJI dataset](https://huggingface.co/datasets/turing-motors/MOMIJI) and can also fetch HTML from URLs to create similar interleaved data.

## Features

*   Extracts `text` and `text_list` from entries in the MOMIJI dataset.
*   Downloads HTML content from specified URLs to generate image-text interleaved data.

## Requirements

*   Python (specify version if known, e.g., Python 3.8+)
*   (Potentially other dependencies, like `requests` for fetching URLs, `beautifulsoup4` for parsing HTML, etc. - please specify if known)
*   `uv` (recommended for running scripts, as shown in usage examples)

## Installation

To set up the project and install dependencies, use `uv`:

```bash
uv sync
```

This command will create a virtual environment (if one doesn't exist) and install all the necessary packages specified in your project's configuration (e.g., `pyproject.toml` or `requirements.txt` if `uv` is configured to use them).

Make sure you have `uv` installed. If not, you can find installation instructions [here](https://github.com/astral-sh/uv#installation).

## Usage

The primary way to use `momiji_generator` is via its command-line interface.

### Example: Retrieving text from a MOMIJI dataset file

```bash
uv run python retrieve_text_from_jsonl.py --input_path 1707947473360.9.jsonl.gz --output_path 1707947473360.9.jsonl --limit 20
```

This command processes a gzipped JSONL file (presumably from the MOMIJI dataset), extracts relevant text fields, and saves the output to `1707947473360.9.jsonl`, limiting the processing to the first 20 entries.

### Example: Using with Docker

If you prefer to use Docker, you can build an image and run the tool in a container.

1.  **Build the Docker image:**

    ```bash
    docker build -t momiji_generator .
    ```

2.  **Run the container:**

    This example mounts the current directory (`$(pwd)`) to `/data_io` inside the container, allowing the script to read input from and write output to your host machine.

    ```bash
    docker run --rm \
      -v "$(pwd):/data_io" \
      momiji_generator \
      --input_path /data_io/1707947473360.9.jsonl.gz \
      --output_path /data_io/new_output.jsonl \
      --limit 5
    ```

    This command will process `1707947473360.9.jsonl.gz` from your current directory and save the output as `new_output.jsonl` in the same directory, processing up to 5 entries.

### Example: Generating interleaved data from a URL

```bash
# Add command example for URL processing here if applicable
# e.g., uv run python generate_from_url.py --url https://example.com/article --output_path output.jsonl
```

## Data Source: MOMIJI Dataset

This tool is designed to work with the [MOMIJI (Modern Open Multimodal Japanese filtered Dataset)](https://huggingface.co/datasets/turing-motors/MOMIJI). MOMIJI is a large-scale public dataset of image-text–interleaved web documents.

**Important Note on MOMIJI Dataset License and Usage:**
The MOMIJI dataset is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). However, its use is **strictly limited to "information analysis"** as defined in Article 30-4 of the Japanese Copyright Act. This means it can be used for non-consumptive machine processing (like training AI models, research) but not for human enjoyment of the works. Please refer to the [Hugging Face dataset card](https://huggingface.co/datasets/turing-motors/MOMIJI) for detailed permitted and prohibited uses.

## Contributing

Contributions are welcome! 🎉 Please feel free to:
*   Open an issue to report bugs or suggest features.
*   Submit a pull request with improvements.
