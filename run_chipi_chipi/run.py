import math
import os
import sys
from pathlib import Path

import cursor  # type: ignore
from fpstimer import FPSTimer  # type: ignore
from playsound import playsound
from pydub import AudioSegment  # type: ignore
from rich.progress import Progress
from to_ascii import to_ascii  # type: ignore
from vid_info import vid_info  # type: ignore

RED = "\u001b[31m"
GREEN = "\u001b[32m"
CYAN = "\u001b[36m"

RESET_PRINT = "\u001b[m"
RESET_CURSOR = "\u001b[H"
CLEAR_TERMINAL = "\u001b[2J"

SCALE = 33

DIR = Path(__file__).parent.parent.absolute() / "data"
AUDIO_PATH = DIR / "audio.mp3"
VIDEO_PATH = DIR / "chipichipi.mp4"
FRAMES_PATH = DIR

TOTAL_FRAMES = 740

RESOLUTION = (1920, 1080)
RESOLUTION_MULTIPLIER = RESOLUTION[0] / RESOLUTION[1]


def customize_frames() -> None:
    global SCALE, FRAMES_PATH
    args = sys.argv
    if len(args) > 1:
        SCALE = int(args[1])
        FRAMES_PATH = FRAMES_PATH / str(args[1])
        return

    size = os.get_terminal_size()

    width = size.columns
    height = size.lines

    scale_width: int = math.ceil(RESOLUTION_MULTIPLIER * RESOLUTION[0] / width)
    scale_height: int = math.ceil(RESOLUTION[1] / height)
    total_downscale: int = max(scale_height, scale_width)

    if total_downscale > SCALE:
        print(
            "Terminal size doesn't allow default configuration, both sizes should be higher tha needed:"
        )
        print(
            f"Width: actual - {width}, needed - {int(RESOLUTION_MULTIPLIER * RESOLUTION[0] / 33)}"
        )
        print(f"Height: actual - {height}, needed - {int(RESOLUTION[1] / 33)}")

        SCALE = total_downscale
        FRAMES_PATH = FRAMES_PATH / str(total_downscale)

        print(f"Your total downscale is {total_downscale}")
    else:
        FRAMES_PATH = FRAMES_PATH / str(SCALE)


def get_timer() -> FPSTimer:
    info: vid_info = vid_info(str(VIDEO_PATH))
    framerate: int = info.get_framerate()
    timer = FPSTimer(framerate)
    return timer


def save_audio() -> None:
    AUDIO_PATH.parent.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(VIDEO_PATH, "mp4")
    audio.export(AUDIO_PATH, format="mp3")


def save_frames() -> None:
    with Progress() as progress:
        generating = progress.add_task(
            "[red]Generating custom scale frames: ", total=TOTAL_FRAMES
        )

        VIDEO_PATH.parent.mkdir(parents=True, exist_ok=True)
        frame_info: vid_info = vid_info(str(VIDEO_PATH))

        rendered_result: list[str] = []

        for frame_number in range(TOTAL_FRAMES):
            image = frame_info.get_frame(frame_number)
            frame: to_ascii = to_ascii(
                image, SCALE, width_multiplication=RESOLUTION_MULTIPLIER
            )

            frame_colored: str = frame.asciify_colored()
            rendered_result.append(frame_colored)
            progress.update(generating, advance=1)

        FRAMES_PATH.mkdir(parents=True, exist_ok=True)
        for index, frame_colored in enumerate(rendered_result):
            with open(FRAMES_PATH / f"{index}.txt", "w") as f:
                f.write(frame_colored)


def load_frames() -> list[str]:
    frames: list[str] = []
    for index in range(TOTAL_FRAMES):
        with open(FRAMES_PATH / f"{index}.txt", "r") as f:
            frame = f.read()
        frames.append(frame)
    return frames


def play(frames: list[str]) -> None:
    timer: FPSTimer = get_timer()
    print(CLEAR_TERMINAL)

    playsound(AUDIO_PATH, block=False)
    for frame in frames:
        print(RESET_CURSOR + frame + RESET_PRINT)
        timer.sleep()


def chipi_chipi() -> None:
    customize_frames()

    if os.name == "nt":
        os.system("cls")

    if not AUDIO_PATH.exists():
        save_frames()

    if not FRAMES_PATH.exists():
        save_frames()

    try:
        frames: list[str] = load_frames()
        cursor.hide()

        while True:
            play(frames)
    except KeyboardInterrupt:
        cursor.show()
        print(CLEAR_TERMINAL + RESET_CURSOR + RESET_PRINT)
        print("UwU :3")


if __name__ == "__main__":
    chipi_chipi()
