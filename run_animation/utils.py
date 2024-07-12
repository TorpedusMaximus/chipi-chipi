from pathlib import Path

from vid_info import vid_info

from run_animation.run import save_audio, save_frames
from run_animation.sources import DATA_DESCRIPTION

ANIMATIONS_DESCRIPTIONS = DATA_DESCRIPTION.copy()


def analyze_videos():
    for source in ANIMATIONS_DESCRIPTIONS.keys():
        properties = vid_info(str(ANIMATIONS_DESCRIPTIONS[source]["video"]))

        properties.get_framecount()

        print(f"{source}: {properties.get_framecount()} {properties.get_framerate()}")

analyze_videos()