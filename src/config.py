from dataclasses import dataclass


@dataclass
class Config:
    """
    Centralized configuration for the Lambda function.
    Values can be overridden by environment variables.
    """

    DEFAULT_ENCODING: str = "utf-8"
