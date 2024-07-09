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
        total_frames=740,
        base_scale=33,
        chosen_scale=33,
    ),
}
