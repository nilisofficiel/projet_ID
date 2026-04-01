"""
Reality Show Workflow - Orchestrate the complete animated reality show production pipeline

This module coordinates all steps of the avatar reality show production:
1. Image cartoonization (create avatars)
2. Avatar animation (expressions and movements)
3. Video editing and composition
4. Audio integration
5. Final optimization for social media

Example workflow:
- Input: Influencer photos
- Output: Ready-to-publish episode video
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from avatar_cartoonizer import AvatarCartoonizer
from avatar_animator import AvatarAnimator
from video_editor import VideoEditor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealityShowProducer:
    """Main orchestrator for reality show production"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the reality show producer

        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or self._load_config()

        # Initialize components
        self.cartoonizer = AvatarCartoonizer(
            api_key=self.config.get('huggingface_api_key')
        )
        self.animator = AvatarAnimator(
            api_key=self.config.get('did_api_key')
        )
        self.editor = VideoEditor()

        # Setup directories
        self.project_dir = Path('projects')
        self.project_dir.mkdir(exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment"""
        config_file = Path('config/reality_show_config.json')

        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)

        # Default config from environment variables
        return {
            'huggingface_api_key': os.getenv('HUGGINGFACE_API_KEY'),
            'did_api_key': os.getenv('DID_API_KEY'),
            'default_platform': 'tiktok',
            'episode_duration': 180,  # 3 minutes
        }

    def create_episode(
        self,
        episode_name: str,
        scenes: List[Dict[str, Any]],
        background_music: Optional[str] = None,
        platform: str = 'tiktok'
    ) -> str:
        """
        Create a complete episode from scenes

        Args:
            episode_name: Name for the episode
            scenes: List of scene configurations
            background_music: Path to background music file
            platform: Target social media platform

        Returns:
            Path to final episode video

        Scene configuration format:
        {
            'influencer_images': ['path1.jpg', 'path2.jpg'],
            'script': 'Optional dialogue text',
            'expressions': ['happy', 'surprised'],
            'duration': 10
        }
        """
        logger.info(f"Creating episode: {episode_name}")

        # Create project directory
        episode_dir = self.project_dir / episode_name
        episode_dir.mkdir(exist_ok=True)

        animated_clips = []

        # Process each scene
        for i, scene in enumerate(scenes):
            logger.info(f"Processing scene {i+1}/{len(scenes)}")

            scene_clips = self._process_scene(
                scene,
                scene_number=i+1,
                episode_dir=episode_dir
            )
            animated_clips.extend(scene_clips)

        # Combine clips into episode
        logger.info("Combining clips into episode")
        episode_video = self.editor.concatenate_videos(
            animated_clips,
            output_name=f"{episode_name}_raw"
        )

        # Add background music if provided
        if background_music and os.path.exists(background_music):
            logger.info("Adding background music")
            episode_video = self.editor.add_audio(
                episode_video,
                background_music,
                output_name=f"{episode_name}_with_audio",
                audio_volume=0.3  # Lower volume so it's background
            )

        # Optimize for target platform
        logger.info(f"Optimizing for {platform}")
        final_video = self.editor.optimize_for_social_media(
            episode_video,
            platform=platform,
            output_name=episode_name
        )

        logger.info(f"Episode complete: {final_video}")
        return final_video

    def _process_scene(
        self,
        scene: Dict[str, Any],
        scene_number: int,
        episode_dir: Path
    ) -> List[str]:
        """Process a single scene with one or more avatars"""
        influencer_images = scene.get('influencer_images', [])
        expressions = scene.get('expressions', ['neutral'] * len(influencer_images))
        script = scene.get('script')

        scene_clips = []

        # Create and animate avatars for this scene
        for i, (image_path, expression) in enumerate(zip(influencer_images, expressions)):
            logger.info(f"Processing avatar {i+1} in scene {scene_number}")

            # Step 1: Cartoonize the image
            avatar_path = self.cartoonizer.cartoonize_with_huggingface(
                image_path,
                output_name=f"scene{scene_number}_avatar{i+1}"
            )

            # Step 2: Animate the avatar
            animated_path = self.animator.animate_with_did(
                avatar_path,
                text=script if i == 0 else None,  # Only first avatar speaks
                expression=expression,
                output_name=f"scene{scene_number}_animation{i+1}"
            )

            scene_clips.append(animated_path)

        return scene_clips

    def quick_episode_from_images(
        self,
        image_paths: List[str],
        episode_name: str = 'quick_episode',
        platform: str = 'tiktok'
    ) -> str:
        """
        Quickly create an episode from a list of images

        Args:
            image_paths: List of influencer image paths
            episode_name: Name for the episode
            platform: Target platform

        Returns:
            Path to final episode
        """
        # Create simple scenes - one avatar per scene
        scenes = [
            {
                'influencer_images': [image_path],
                'expressions': ['happy'],
                'duration': 5
            }
            for image_path in image_paths
        ]

        return self.create_episode(
            episode_name=episode_name,
            scenes=scenes,
            platform=platform
        )

    def batch_produce_episodes(
        self,
        episodes_config: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Produce multiple episodes in batch

        Args:
            episodes_config: List of episode configurations

        Returns:
            List of paths to produced episodes
        """
        results = []

        for i, config in enumerate(episodes_config):
            try:
                logger.info(f"Producing episode {i+1}/{len(episodes_config)}")
                episode_path = self.create_episode(**config)
                results.append(episode_path)
            except Exception as e:
                logger.error(f"Failed to produce episode {i+1}: {e}")
                continue

        return results

    def save_project(self, project_name: str, scenes: List[Dict[str, Any]]):
        """Save project configuration for later editing"""
        project_file = self.project_dir / f"{project_name}_config.json"

        project_data = {
            'name': project_name,
            'scenes': scenes,
            'created_at': str(Path.ctime(project_file)) if project_file.exists() else None
        }

        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)

        logger.info(f"Project saved to {project_file}")

    def load_project(self, project_name: str) -> Dict[str, Any]:
        """Load a saved project configuration"""
        project_file = self.project_dir / f"{project_name}_config.json"

        if not project_file.exists():
            raise FileNotFoundError(f"Project not found: {project_name}")

        with open(project_file) as f:
            return json.load(f)


def main():
    """Example usage of RealityShowProducer"""
    import sys

    print("=== Animated Reality Show Producer ===")
    print()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python reality_show_workflow.py <image1> <image2> <image3> ...")
        print()
        print("This will create a quick episode from the provided images.")
        sys.exit(1)

    image_paths = sys.argv[1:]

    print(f"Creating episode from {len(image_paths)} images...")
    print()

    producer = RealityShowProducer()

    # Create a quick episode
    episode = producer.quick_episode_from_images(
        image_paths=image_paths,
        episode_name='my_reality_show_ep1',
        platform='tiktok'
    )

    print()
    print(f"✓ Episode created successfully!")
    print(f"  Location: {episode}")
    print()
    print("Next steps:")
    print("  1. Review the episode video")
    print("  2. Upload to TikTok, Instagram, or YouTube")
    print("  3. Create more episodes with different scenes!")


if __name__ == "__main__":
    main()
