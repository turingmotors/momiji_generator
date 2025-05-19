from typing import Any
import trafilatura
from bunkai import Bunkai
import requests
from src.modules.image_processor import ImageProcessor
from src.config import config


class RecordProcessor:
    """
    Extracts data from a WARC record.
    """

    def __init__(self, record: dict, verbose: bool = False):
        self.record = record
        self.verbose = verbose
        self.data: dict[str, Any] = {}
        self.record_url = self.record["url"]
        self.bunkai_instance = Bunkai()
        self.image_processor = ImageProcessor(self.record["image_info"])

    def html_content(self, url: str) -> str:
        """
        Fetches the HTML content from the given URL.

        Args:
            url (str): The URL to fetch HTML from.

        Returns:
            str: The HTML content of the page.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    def generate_content(self) -> dict[str, Any]:
        """
        Extracts data from the record if it is valid for processing.
        """

        html_content_original = self.html_content(self.record_url)

        if not html_content_original:
            print(f"Could not retrieve HTML content for {self.record_url}")
            return self.data

        html_content_processed_for_images = (
            self.image_processor.replace_images_with_placeholders(
                html_content_original, self.record_url
            )
        )

        ext_text = self.extract_text(html_content_processed_for_images, self.record_url)

        if ext_text is None:
            print(f"Could not extract text from {self.record_url}")
            return self.data

        text_list = self.split_text_preserving_placeholders(ext_text)
        self.data = self.generate_output(ext_text, text_list)
        return self.data

    def extract_text(self, content: str, url: str) -> str | None:
        """
        Extracts the main text content from an HTML string.
        """
        return trafilatura.extract(
            content,
            **config.TRAFILATURA_SETTINGS,
            url=url,
        )

    def generate_output(self, ext_text: str, text_list: list[str]) -> dict[str, Any]:
        """
        Generates the output data.
        """
        return {
            "docId": self.record["docId"],
            "url": self.record_url,
            "text": ext_text,
            "text_list": text_list,
            "image_info": self.record["image_info"],
        }

    def split_text_preserving_placeholders(self, text: str) -> list[str]:
        """
        Splits text by image placeholders, keeping placeholders intact,
        and further splitting other parts using bunkai.
        """
        segments = self.image_processor.split_text_by_image_placeholders(text)
        result: list[str] = []

        for segment in segments:
            if self.image_processor.is_image_placeholder(segment):
                result.append(segment)
            else:
                result.extend(self.split_text_with_bunkai(segment))

        return result

    def split_text_with_bunkai(self, text: str) -> list[str]:
        """Splits text using bunkai."""
        if text.strip():
            return [s.rstrip() for s in self.bunkai_instance(text) if s.strip()]
        return []
