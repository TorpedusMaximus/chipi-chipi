import math
from os import terminal_size
import shutil
from pathlib import Path

from fpstimer import FPSTimer
from playsound import playsound
from pydub import AudioSegment
from rich.progress import Progress
from to_ascii import to_ascii
from vid_info import vid_info

DIR = Path(__file__).parent.parent.absolute() / "data"


# DIR = Path.home() / ".chipi-chipi"

class Animation:
    name: str
    video_path: Path
    audio_path: Path
    frames_path: Path
    resolution: tuple[int, int] | list[int, int]
    resolution_multiplier: float
    scale: int
    chosen_scale: int
    frame_count: int
    framerate: int

    def __init__(self, name: str, resolution: tuple[int, int] | list[int, int], scale: int):
        self.name = name
        self.chosen_scale = scale
        self.video_path = DIR / "videos" / f"{name}.mp4"
        self.audio_path = DIR / "audio" / f"{name}.mp3"
        self.frames_path = DIR / "frames" / name
        self.resolution = resolution
        self.resolution_multiplier = resolution[0] / resolution[1]
        self.scale = scale
        self.frame_count = int(vid_info(str(self.video_path)).get_framecount())
        self.framerate = int(vid_info(str(self.video_path)).get_framerate())

    def save_audio(self) -> None:
        self.audio_path.parent.mkdir(parents=True, exist_ok=True)
        audio = AudioSegment.from_file(self.video_path, "mp4")
        audio.export(self.audio_path, format="mp3")

    def save_frames(self) -> None:
        with Progress() as progress:
            self.video_path.parent.mkdir(parents=True, exist_ok=True)
            frame_info: vid_info = vid_info(str(self.video_path))
            generating = progress.add_task(
                f"[red]Generating custom scale frames for {self.name}: ", total=self.frame_count
            )

            self.frames_path.mkdir(parents=True, exist_ok=True)
            try:
                for frame_number in range(self.frame_count):
                    image = frame_info.get_frame(frame_number)
                    frame: to_ascii = to_ascii(
                        image, self.scale,
                        width_multiplication=self.resolution_multiplier
                    )

                    frame_colored: str = frame.asciify_colored()
                    progress.update(generating, advance=1)
                    with open(self.frames_path / f"{frame_number}.txt", "w") as f:
                        f.write(frame_colored)
            except Exception as e:
                shutil.rmtree(self.frames_path)

    def load_frames(self) -> list[str]:
        frames: list[str] = []
        for index in range(self.frame_count):
            with open(self.frames_path / f"{index}.txt", "r") as f:
                frame = f.read()
            frames.append(frame)
        return frames

    def get_timer(self) -> FPSTimer:
        return FPSTimer(self.framerate)

    def play_music(self):
        playsound(self.audio_path, block=False)

    def customize_frames(self, size: terminal_size) -> None:
        if self.chosen_scale != self.scale:
            print(f"Chosen downscale: {self.chosen_scale}")
            self.frames_path = self.frames_path / str(self.chosen_scale)
            return

        width = size.columns
        height = size.lines

        if width < 1:
            self.frames_path = self.frames_path / str(self.scale)
            self.chosen_scale = self.scale
            return

        scale_width: int = math.ceil(self.resolution_multiplier * self.resolution[0] / width)
        scale_height: int = math.ceil(self.resolution[1] / height)
        total_downscale: int = max(scale_height, scale_width)

        if total_downscale > self.scale:
            print(
                "Terminal size doesn't allow default configuration, both sizes should be higher tha needed:"
            )
            print(
                f"Width: actual - {width}, needed - {int(self.resolution_multiplier * self.resolution[0] / 33)}"
            )
            print(f"Height: actual - {height}, needed - {int(self.resolution[1] / 33)}")

            self.frames_path = self.frames_path / str(total_downscale)
            self.chosen_scale = total_downscale

            print(f"Your total downscale is {total_downscale}")
        else:
            self.frames_path = self.frames_path / str(self.scale)
