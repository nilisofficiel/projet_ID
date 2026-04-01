"""
Video Editor - Edit and compose animated reality show episodes

This module provides functionality to edit, compose, and produce
final episodes from animated avatars with music and effects.

Integrates with:
- FFmpeg for video editing
- Audio libraries for music/sound effects
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEditor:
    """Main class for video editing and composition"""

    def __init__(self):
        """Initialize the video editor"""
        self.output_dir = Path('output/episodes')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path('/tmp/video_editing')
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("FFmpeg not found. Please install FFmpeg to use video editing features.")
            return False

    def concatenate_videos(
        self,
        video_paths: List[str],
        output_name: str = 'episode',
        transition_duration: float = 0.5
    ) -> str:
        """
        Concatenate multiple video clips into one episode

        Args:
            video_paths: List of paths to video clips
            output_name: Name for output episode
            transition_duration: Duration of transitions between clips (seconds)

        Returns:
            Path to the final episode
        """
        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg is required for video editing")

        logger.info(f"Concatenating {len(video_paths)} video clips")

        # Create concat list file
        concat_file = self.temp_dir / 'concat_list.txt'
        with open(concat_file, 'w') as f:
            for video_path in video_paths:
                f.write(f"file '{os.path.abspath(video_path)}'\n")

        output_path = self.output_dir / f"{output_name}.mp4"

        # FFmpeg concat command
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Episode saved to {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error concatenating videos: {e.stderr.decode()}")
            raise

    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_name: str = 'episode_with_audio',
        audio_volume: float = 1.0
    ) -> str:
        """
        Add background music or sound effects to video

        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_name: Name for output file
            audio_volume: Volume multiplier for audio (0.0 to 1.0)

        Returns:
            Path to video with audio
        """
        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg is required for video editing")

        logger.info(f"Adding audio {audio_path} to {video_path}")

        output_path = self.output_dir / f"{output_name}.mp4"

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-filter:a', f'volume={audio_volume}',
            '-shortest',  # Match shortest stream duration
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Video with audio saved to {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error adding audio: {e.stderr.decode()}")
            raise

    def add_transitions(
        self,
        video_paths: List[str],
        transition_type: str = 'fade',
        output_name: str = 'episode_transitions'
    ) -> str:
        """
        Add transitions between video clips

        Args:
            video_paths: List of video clip paths
            transition_type: Type of transition (fade, wipe, etc.)
            output_name: Output filename

        Returns:
            Path to video with transitions
        """
        logger.info(f"Adding {transition_type} transitions to {len(video_paths)} clips")

        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg is required for video editing")

        # For complex transitions, use xfade filter
        # This is a simplified version - full implementation would handle multiple clips
        if len(video_paths) < 2:
            return video_paths[0] if video_paths else ""

        output_path = self.output_dir / f"{output_name}.mp4"

        # Build filter complex for transitions
        filter_complex = self._build_transition_filter(video_paths, transition_type)

        cmd = [
            'ffmpeg',
            *self._get_input_args(video_paths),
            '-filter_complex', filter_complex,
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Video with transitions saved to {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error adding transitions: {e.stderr.decode()}")
            raise

    def _get_input_args(self, video_paths: List[str]) -> List[str]:
        """Generate FFmpeg input arguments for multiple videos"""
        args = []
        for path in video_paths:
            args.extend(['-i', path])
        return args

    def _build_transition_filter(self, video_paths: List[str], transition_type: str) -> str:
        """Build FFmpeg filter complex for transitions"""
        # Simplified - just concatenate for now
        # Full implementation would use xfade filter
        num_videos = len(video_paths)
        inputs = ''.join(f'[{i}:v]' for i in range(num_videos))
        return f'{inputs}concat=n={num_videos}:v=1:a=0[outv]'

    def trim_video(
        self,
        video_path: str,
        start_time: float,
        duration: float,
        output_name: str = 'trimmed'
    ) -> str:
        """
        Trim video to specific duration

        Args:
            video_path: Path to video file
            start_time: Start time in seconds
            duration: Duration in seconds
            output_name: Output filename

        Returns:
            Path to trimmed video
        """
        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg is required for video editing")

        logger.info(f"Trimming {video_path} from {start_time}s for {duration}s")

        output_path = self.output_dir / f"{output_name}.mp4"

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c', 'copy',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Trimmed video saved to {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error trimming video: {e.stderr.decode()}")
            raise

    def optimize_for_social_media(
        self,
        video_path: str,
        platform: str = 'tiktok',
        output_name: str = 'optimized'
    ) -> str:
        """
        Optimize video for specific social media platform

        Args:
            video_path: Path to video file
            platform: Target platform (tiktok, instagram, youtube)
            output_name: Output filename

        Returns:
            Path to optimized video
        """
        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg is required for video editing")

        logger.info(f"Optimizing {video_path} for {platform}")

        # Platform-specific settings
        settings = {
            'tiktok': {'width': 1080, 'height': 1920, 'bitrate': '2M'},
            'instagram': {'width': 1080, 'height': 1920, 'bitrate': '2M'},
            'youtube': {'width': 1920, 'height': 1080, 'bitrate': '4M'}
        }

        config = settings.get(platform, settings['tiktok'])
        output_path = self.output_dir / f"{output_name}_{platform}.mp4"

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"scale={config['width']}:{config['height']}:force_original_aspect_ratio=decrease,pad={config['width']}:{config['height']}:(ow-iw)/2:(oh-ih)/2",
            '-c:v', 'libx264',
            '-b:v', config['bitrate'],
            '-c:a', 'aac',
            '-b:a', '128k',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Optimized video saved to {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error optimizing video: {e.stderr.decode()}")
            raise


def main():
    """Example usage of the VideoEditor"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_editor.py <video1> [video2] [video3] ...")
        sys.exit(1)

    video_paths = sys.argv[1:]

    editor = VideoEditor()
    episode = editor.concatenate_videos(video_paths, output_name='my_episode')
    print(f"Episode created: {episode}")


if __name__ == "__main__":
    main()
