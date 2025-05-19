from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Config:
    """
    Centralized configuration for the Lambda function.
    Values can be overridden by environment variables.
    """

    DEFAULT_ENCODING: str = "utf-8"
    TRAFILATURA_SETTINGS: Dict[str, Any] = field(
        default_factory=lambda: {
            "include_formatting": False,
            "include_images": False,
            "include_tables": False,
            "include_comments": False,
            "no_fallback": True,
        }
    )


config = Config()
