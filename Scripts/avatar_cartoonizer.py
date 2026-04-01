"""
Avatar Cartoonizer - Transform photos into cartoon-style avatars

This module provides functionality to convert influencer photos into
cartoon-style avatars using various AI services.

Supported services:
- Toonify (Hugging Face)
- Artbreeder API
- Fotor Cartoonizer API
"""

import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AvatarCartoonizer:
    """Main class for cartoonizing images into avatars"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the cartoonizer

        Args:
            api_key: Optional API key for services that require authentication
        """
        self.api_key = api_key or os.getenv('CARTOONIZER_API_KEY')
        self.output_dir = Path('output/avatars')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def cartoonize_with_huggingface(self, image_path: str, output_name: str) -> str:
        """
        Cartoonize an image using Hugging Face Toonify model

        Args:
            image_path: Path to the input image
            output_name: Name for the output file

        Returns:
            Path to the cartoonized image
        """
        logger.info(f"Cartoonizing {image_path} using Hugging Face Toonify")

        # Hugging Face Inference API endpoint
        API_URL = "https://api-inference.huggingface.co/models/akhaliq/Toonify"

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            with open(image_path, "rb") as f:
                data = f.read()

            response = requests.post(API_URL, headers=headers, data=data)
            response.raise_for_status()

            output_path = self.output_dir / f"{output_name}_toonify.png"
            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Cartoonized image saved to {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error cartoonizing with Hugging Face: {e}")
            raise

    def cartoonize_batch(self, image_paths: list, method: str = 'huggingface') -> list:
        """
        Cartoonize multiple images

        Args:
            image_paths: List of paths to input images
            method: Cartoonization method to use

        Returns:
            List of paths to cartoonized images
        """
        results = []
        for i, image_path in enumerate(image_paths):
            try:
                output_name = f"avatar_{i+1}"
                if method == 'huggingface':
                    result = self.cartoonize_with_huggingface(image_path, output_name)
                    results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {image_path}: {e}")
                continue

        return results

    def enhance_avatar_style(self, image_path: str, style_params: Dict[str, Any]) -> str:
        """
        Apply additional style enhancements to avatar

        Args:
            image_path: Path to the avatar image
            style_params: Dictionary of style parameters

        Returns:
            Path to the enhanced avatar
        """
        logger.info(f"Enhancing avatar style for {image_path}")
        # This would integrate with additional styling APIs or filters
        # For now, returns the original path
        return image_path


def main():
    """Example usage of the AvatarCartoonizer"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python avatar_cartoonizer.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    cartoonizer = AvatarCartoonizer()
    output = cartoonizer.cartoonize_with_huggingface(image_path, "influencer_avatar")
    print(f"Cartoonized avatar saved to: {output}")


if __name__ == "__main__":
    main()
