"""
Example: Create a simple animated reality show episode

This example demonstrates how to create a complete episode
from influencer photos with minimal configuration.
"""

from Scripts.reality_show_workflow import RealityShowProducer


def example_quick_episode():
    """Create a quick episode from sample images"""
    print("=== Example 1: Quick Episode from Images ===\n")

    # Initialize producer
    producer = RealityShowProducer()

    # List of influencer images (replace with your actual image paths)
    images = [
        'path/to/influencer1.jpg',
        'path/to/influencer2.jpg',
        'path/to/influencer3.jpg'
    ]

    # Create episode
    episode = producer.quick_episode_from_images(
        image_paths=images,
        episode_name='quick_episode_example',
        platform='tiktok'
    )

    print(f"\n✓ Episode created: {episode}\n")


def example_custom_scenes():
    """Create an episode with custom scene configurations"""
    print("=== Example 2: Custom Scene Configuration ===\n")

    # Initialize producer
    producer = RealityShowProducer()

    # Define custom scenes
    scenes = [
        # Scene 1: Introduction - Single influencer, happy expression
        {
            'influencer_images': ['path/to/influencer1.jpg'],
            'expressions': ['happy'],
            'script': None,  # No dialogue
            'duration': 10
        },

        # Scene 2: Interaction - Two influencers
        {
            'influencer_images': [
                'path/to/influencer1.jpg',
                'path/to/influencer2.jpg'
            ],
            'expressions': ['surprised', 'neutral'],
            'duration': 15
        },

        # Scene 3: Resolution - Three influencers, all happy
        {
            'influencer_images': [
                'path/to/influencer1.jpg',
                'path/to/influencer2.jpg',
                'path/to/influencer3.jpg'
            ],
            'expressions': ['happy', 'happy', 'happy'],
            'duration': 10
        }
    ]

    # Create episode with background music
    episode = producer.create_episode(
        episode_name='custom_episode_example',
        scenes=scenes,
        background_music='path/to/music.mp3',  # Optional
        platform='tiktok'
    )

    print(f"\n✓ Episode created: {episode}\n")


def example_save_and_load_project():
    """Demonstrate saving and loading project configurations"""
    print("=== Example 3: Save and Load Projects ===\n")

    producer = RealityShowProducer()

    # Define scenes
    scenes = [
        {
            'influencer_images': ['path/to/influencer1.jpg'],
            'expressions': ['happy'],
            'duration': 10
        }
    ]

    # Save project for later editing
    producer.save_project('my_reality_show_project', scenes)
    print("✓ Project saved\n")

    # Load project
    project = producer.load_project('my_reality_show_project')
    print(f"✓ Project loaded: {project['name']}\n")

    # Create episode from loaded project
    episode = producer.create_episode(
        episode_name=project['name'],
        scenes=project['scenes'],
        platform='instagram'
    )

    print(f"✓ Episode created from saved project: {episode}\n")


def example_batch_production():
    """Produce multiple episodes in batch"""
    print("=== Example 4: Batch Episode Production ===\n")

    producer = RealityShowProducer()

    # Configure multiple episodes
    episodes_config = [
        {
            'episode_name': 'episode_01',
            'scenes': [
                {
                    'influencer_images': ['path/to/influencer1.jpg'],
                    'expressions': ['happy'],
                    'duration': 10
                }
            ],
            'platform': 'tiktok'
        },
        {
            'episode_name': 'episode_02',
            'scenes': [
                {
                    'influencer_images': ['path/to/influencer2.jpg'],
                    'expressions': ['surprised'],
                    'duration': 10
                }
            ],
            'platform': 'instagram'
        }
    ]

    # Produce all episodes
    results = producer.batch_produce_episodes(episodes_config)

    print(f"\n✓ Produced {len(results)} episodes:")
    for episode in results:
        print(f"  - {episode}")
    print()


if __name__ == "__main__":
    print("Animated Reality Show - Examples\n")
    print("=" * 50)
    print()

    # Uncomment the example you want to run:

    # example_quick_episode()
    # example_custom_scenes()
    # example_save_and_load_project()
    # example_batch_production()

    print("\nTo run an example, uncomment the corresponding function call")
    print("and update the image paths with your actual files.\n")
