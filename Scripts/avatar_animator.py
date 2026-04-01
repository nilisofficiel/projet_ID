"""
Avatar Animator - Animate cartoon avatars with facial expressions and body movements

This module provides functionality to animate static avatars using various AI services.

Supported services:
- D-ID (facial animation and lip sync)
- DeepMotion Animate 3D (body movements)
- Runway ML (scene composition)
"""

import os
import requests
import time
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AvatarAnimator:
    """Main class for animating avatar images"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the animator

        Args:
            api_key: API key for animation services (D-ID, etc.)
        """
        self.api_key = api_key or os.getenv('DID_API_KEY')
        self.output_dir = Path('output/animations')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def animate_with_did(
        self,
        image_path: str,
        text: Optional[str] = None,
        expression: str = 'neutral',
        output_name: str = 'animated_avatar'
    ) -> str:
        """
        Animate an avatar using D-ID API

        Args:
            image_path: Path to the avatar image
            text: Optional text for lip sync (None for no voice)
            expression: Facial expression type
            output_name: Name for output video

        Returns:
            Path to the animated video
        """
        logger.info(f"Animating {image_path} with D-ID")

        if not self.api_key:
            raise ValueError("D-ID API key is required. Set DID_API_KEY environment variable.")

        # D-ID API endpoints
        CREATE_URL = "https://api.d-id.com/talks"

        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare animation request
        payload = {
            "source_url": image_path,
            "driver_url": "bank://lively",  # Use built-in animation driver
            "config": {
                "stitch": True,
                "result_format": "mp4"
            }
        }

        # Add text for lip sync if provided
        if text:
            payload["script"] = {
                "type": "text",
                "input": text,
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                }
            }

        try:
            # Create animation
            response = requests.post(CREATE_URL, headers=headers, json=payload)
            response.raise_for_status()

            talk_id = response.json()['id']
            logger.info(f"Animation created with ID: {talk_id}")

            # Poll for completion
            result_url = self._poll_did_status(talk_id, headers)

            # Download result
            output_path = self.output_dir / f"{output_name}.mp4"
            self._download_video(result_url, output_path)

            logger.info(f"Animated video saved to {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error animating with D-ID: {e}")
            raise

    def _poll_did_status(self, talk_id: str, headers: Dict) -> str:
        """Poll D-ID API for animation completion"""
        STATUS_URL = f"https://api.d-id.com/talks/{talk_id}"
        max_attempts = 60

        for attempt in range(max_attempts):
            response = requests.get(STATUS_URL, headers=headers)
            response.raise_for_status()

            status = response.json()['status']
            logger.info(f"Animation status: {status} (attempt {attempt + 1}/{max_attempts})")

            if status == 'done':
                return response.json()['result_url']
            elif status == 'error':
                raise Exception(f"Animation failed: {response.json()}")

            time.sleep(5)

        raise TimeoutError("Animation timed out")

    def _download_video(self, url: str, output_path: Path):
        """Download video from URL"""
        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

    def animate_body_movement(
        self,
        avatar_path: str,
        motion_reference: str,
        output_name: str = 'body_animated'
    ) -> str:
        """
        Add body movement to avatar using motion reference

        Args:
            avatar_path: Path to avatar image/video
            motion_reference: Path to reference motion video
            output_name: Output filename

        Returns:
            Path to animated result
        """
        logger.info(f"Adding body animation to {avatar_path}")

        # This would integrate with DeepMotion API
        # For now, returns a placeholder
        output_path = self.output_dir / f"{output_name}.mp4"
        logger.warning("DeepMotion integration pending - returning placeholder")
        return str(output_path)

    def create_multi_avatar_scene(
        self,
        avatar_videos: list,
        scene_config: Dict[str, Any],
        output_name: str = 'scene'
    ) -> str:
        """
        Combine multiple animated avatars into a scene

        Args:
            avatar_videos: List of paths to animated avatar videos
            scene_config: Scene composition configuration
            output_name: Output filename

        Returns:
            Path to composed scene video
        """
        logger.info(f"Creating multi-avatar scene with {len(avatar_videos)} avatars")

        # This would integrate with Runway ML API
        # For now, returns a placeholder
        output_path = self.output_dir / f"{output_name}.mp4"
        logger.warning("Runway ML integration pending - returning placeholder")
        return str(output_path)

    def batch_animate(
        self,
        image_paths: list,
        expressions: Optional[list] = None
    ) -> list:
        """
        Animate multiple avatars

        Args:
            image_paths: List of avatar image paths
            expressions: Optional list of expressions for each avatar

        Returns:
            List of paths to animated videos
        """
        if expressions is None:
            expressions = ['neutral'] * len(image_paths)

        results = []
        for i, (image_path, expression) in enumerate(zip(image_paths, expressions)):
            try:
                output_name = f"avatar_animation_{i+1}"
                result = self.animate_with_did(
                    image_path,
                    expression=expression,
                    output_name=output_name
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to animate {image_path}: {e}")
                continue

        return results


def main():
    """Example usage of the AvatarAnimator"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python avatar_animator.py <avatar_image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    animator = AvatarAnimator()
    output = animator.animate_with_did(image_path, expression='happy')
    print(f"Animated avatar saved to: {output}")


if __name__ == "__main__":
    main()
