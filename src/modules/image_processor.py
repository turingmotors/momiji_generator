from typing import Any
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup, ParserRejectedMarkup

from src.config import Config


class ImageProcessor:
    """
    Handles image-related processing for WARC records.
    """

    IMAGE_PATTERN = re.compile(r"\\[\\[IMAGE: .*?\\]\\]")

    def __init__(self, image_info: list[dict[str, Any]]):
        """
        Initializes the ImageProcessor.

        Args:
            image_info (list[dict[str, Any]]): A list of dictionaries, each containing image URL and placeholder.
        """
        self.image_info_map = self._create_image_info_map(image_info)

    def _create_image_info_map(
        self, image_info: list[dict[str, Any]]
    ) -> dict[str, str]:
        """
        Creates a map from image URLs to their placeholders.

        Args:
            image_info (list[dict[str, Any]]): A list of dictionaries, each containing image URL and placeholder.

        Returns:
            dict[str, str]: A dictionary mapping image URLs to placeholders.
        """
        return {record["url"]: record["placeholder"] for record in image_info}

    def replace_images_with_placeholders(self, html_content: str, base_url: str) -> str:
        """
        Replaces <img> tags in HTML content with their corresponding placeholders.

        Args:
            html_content (str): The HTML content string.
            base_url (str): The base URL to resolve relative image URLs.

        Returns:
            str: HTML content with <img> tags replaced by placeholders.
        """
        try:
            soup = BeautifulSoup(html_content, "lxml")
            for img in soup.find_all("img"):
                img_url = img.get("src") or img.get("data-src")
                if img_url:
                    absolute_img_url = urljoin(base_url, img_url)
                    img_placeholder = self.image_info_map.get(absolute_img_url, "")
                    if img_placeholder:
                        img.replace_with(img_placeholder)
                    else:
                        img.decompose()
        except ValueError as e:
            print(f"Error processing an image tag: {e}")
        except ParserRejectedMarkup as e:
            print(f"Error parsing HTML for image replacement: {e}")

        return soup.prettify(
            encoding=Config.DEFAULT_ENCODING, formatter="minimal"
        ).decode(Config.DEFAULT_ENCODING)

    def is_image_placeholder(self, segment: str) -> bool:
        """
        Checks if a text segment is an image placeholder.

        Args:
            segment (str): The text segment to check.

        Returns:
            bool: True if the segment is an image placeholder, False otherwise.
        """
        return bool(re.fullmatch(self.IMAGE_PATTERN, segment))

    def split_text_by_image_placeholders(self, text: str) -> list[str]:
        """
        Splits text by image placeholders, keeping placeholders intact.

        Args:
            text (str): The text to split.

        Returns:
            list[str]: A list of text segments, with image placeholders preserved.
        """
        if not text:
            return []
        return re.split(f"({self.IMAGE_PATTERN.pattern})", text)
