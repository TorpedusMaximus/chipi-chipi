from pathlib import Path
from typing import TypedDict

DIR = Path(__file__).parent.parent.absolute() / "data"


class DataDescription(TypedDict):
    video: Path
    audio: Path
    frames: Path
    resolution: tuple[int, int]
    resolution_multiplier: float
    total_frames: int
    base_scale: int
    chosen_scale: int


DATA_DESCRIPTION: dict[str, DataDescription] = {
    "chipi-chipi": DataDescription(
        video=DIR / "chipi-chipi" / "chipichipi.mp4",
        audio=DIR / "chipi-chipi" / "audio.mp3",
        frames=DIR / "chipi-chipi" / "frames",
        resolution=(1920, 1080),
        resolution_multiplier=1920 / 1080,
        base_scale=33,
        chosen_scale=33,
        total_frames=740,
    ),
    "shikonoko": DataDescription(
        video=DIR / "shikonoko" / "shikonoko.mp4",
        audio=DIR / "shikonoko" / "audio.mp3",
        frames=DIR / "shikonoko" / "frames",
        resolution=(1920, 1080),
        resolution_multiplier=1920 / 1080,
        base_scale=19,
        chosen_scale=19,
        total_frames=334,
    ),
    "kiss-me": DataDescription(
        video=DIR / "kiss_me" / "kiss_me.mp4",
        audio=DIR / "kiss_me" / "audio.mp3",
        frames=DIR / "kiss_me" / "frames",
        resolution=(1920, 1080),
        resolution_multiplier=1920 / 1080,
        base_scale=19,
        chosen_scale=19,
        total_frames=1032,
    ),
    "shigure-loli": DataDescription(
        video=DIR / "shigure_loli" / "loli.mp4",
        audio=DIR / "shigure_loli" / "audio.mp3",
        frames=DIR / "shigure_loli" / "frames",
        resolution=(1920, 1080),
        resolution_multiplier=1920 / 1080,
        base_scale=24,
        chosen_scale=24,
        total_frames=850,
    ),
    "shigure-catcher": DataDescription(
        video=DIR / "shigure_catcher" / "catcher.mp4",
        audio=DIR / "shigure_catcher" / "audio.mp3",
        frames=DIR / "shigure_catcher" / "frames",
        resolution=(480, 854),
        resolution_multiplier=480 / 854,
        base_scale=33,
        chosen_scale=33,
        total_frames=781,
    ),
    "02": DataDescription(
        video=DIR / "02" / "02.mp4",
        audio=DIR / "02" / "audio.mp3",
        frames=DIR / "02" / "frames",
        resolution=(720, 1280),
        resolution_multiplier=720 / 1280,
        base_scale=33,
        chosen_scale=33,
        total_frames=1368,
    ),
}
