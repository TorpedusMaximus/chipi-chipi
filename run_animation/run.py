import argparse
import math
import os
import sys
from pathlib import Path
from typing import TypedDict

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


class DataDescription(TypedDict):
    video: Path
    audio: Path
    frames: Path
    resolution: tuple[int, int]
    resolution_multiplier: float
    total_frames: int


SOURCE_DATA_DESCRIPTION: dict[str, DataDescription] = {
    "chipi-chipi": DataDescription(
        video=DIR / "chipi-chipi" / "chipichipi.mp4",
        audio=DIR / "chipi-chipi" / "audio.mp3",
        frames=DIR / "chipi-chipi" / "frames",
        resolution=(1920, 1080),
        resolution_multiplier=1920 / 1080,
        total_frames=740,
    ),
}


def customize_frames(source: str = "chipi-chipi") -> None:
    global SCALE, SOURCE_DATA_DESCRIPTION
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--scale", type=int, default=33)
    args = arg_parser.parse_args()
    if args.scale != SCALE:
        SCALE = int(args.scale)
        SOURCE_DATA_DESCRIPTION[source]["frames"] = SOURCE_DATA_DESCRIPTION[source]["frames"] / str(args.scale)
        return

    size = os.get_terminal_size()

    width = size.columns
    height = size.lines

    if width < 1:
        SOURCE_DATA_DESCRIPTION[source]["frames"] = SOURCE_DATA_DESCRIPTION[source]["frames"] / str(SCALE)
        return

    scale_width: int = math.ceil(
        SOURCE_DATA_DESCRIPTION[source]["resolution_multiplier"] * SOURCE_DATA_DESCRIPTION[source]["resolution"][
            0] / width)
    scale_height: int = math.ceil(SOURCE_DATA_DESCRIPTION[source]["resolution"][1] / height)
    total_downscale: int = max(scale_height, scale_width)

    if total_downscale > SCALE:
        print(
            "Terminal size doesn't allow default configuration, both sizes should be higher tha needed:"
        )
        print(
            f"Width: actual - {width}, needed - {int(SOURCE_DATA_DESCRIPTION[source]['resolution_multiplier'] * SOURCE_DATA_DESCRIPTION[source]['resolution'][0] / 33)}"
        )
        print(f"Height: actual - {height}, needed - {int(SOURCE_DATA_DESCRIPTION[source]['resolution'][1] / 33)}")

        SCALE = total_downscale
        SOURCE_DATA_DESCRIPTION[source]["frames"] = SOURCE_DATA_DESCRIPTION[source]["frames"] / str(total_downscale)

        print(f"Your total downscale is {total_downscale}")
    else:
        SOURCE_DATA_DESCRIPTION[source]["frames"] = SOURCE_DATA_DESCRIPTION[source]["frames"] / str(SCALE)


def get_timer(source: str = "chipi-chipi") -> FPSTimer:
    info: vid_info = vid_info(str(SOURCE_DATA_DESCRIPTION[source]["video"]))
    framerate: int = info.get_framerate()
    timer = FPSTimer(framerate)
    return timer


def save_audio(source: str = "chipi-chipi") -> None:
    SOURCE_DATA_DESCRIPTION[source]["audio"].parent.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(SOURCE_DATA_DESCRIPTION[source]["video"], "mp4")
    audio.export(SOURCE_DATA_DESCRIPTION[source]["audio"], format="mp3")


def save_frames(source: str = "chipi-chipi") -> None:
    with Progress() as progress:
        generating = progress.add_task(
            "[red]Generating custom scale frames: ", total=SOURCE_DATA_DESCRIPTION[source]["total_frames"]
        )

        SOURCE_DATA_DESCRIPTION[source]["video"].parent.mkdir(parents=True, exist_ok=True)
        frame_info: vid_info = vid_info(str(SOURCE_DATA_DESCRIPTION[source]["video"]))

        rendered_result: list[str] = []

        for frame_number in range(SOURCE_DATA_DESCRIPTION[source]["total_frames"]):
            image = frame_info.get_frame(frame_number)
            frame: to_ascii = to_ascii(
                image, SCALE, width_multiplication=SOURCE_DATA_DESCRIPTION[source]["resolution_multiplier"]
            )

            frame_colored: str = frame.asciify_colored()
            rendered_result.append(frame_colored)
            progress.update(generating, advance=1)

        SOURCE_DATA_DESCRIPTION[source]["frames"].mkdir(parents=True, exist_ok=True)
        for index, frame_colored in enumerate(rendered_result):
            with open(SOURCE_DATA_DESCRIPTION[source]["frames"] / f"{index}.txt", "w") as f:
                f.write(frame_colored)


def load_frames(source: str = "chipi-chipi") -> list[str]:
    frames: list[str] = []
    for index in range(SOURCE_DATA_DESCRIPTION[source]["total_frames"]):
        with open(SOURCE_DATA_DESCRIPTION[source]["frames"] / f"{index}.txt", "r") as f:
            frame = f.read()
        frames.append(frame)
    return frames


def play(frames: list[str], source: str = "chipi-chipi") -> None:
    timer: FPSTimer = get_timer()
    print(CLEAR_TERMINAL)

    playsound(SOURCE_DATA_DESCRIPTION[source]["audio"], block=False)
    for frame in frames:
        print(RESET_CURSOR + frame + RESET_PRINT)
        timer.sleep()


def run_animation(source: str) -> None:
    customize_frames()

    if os.name == "nt":
        os.system("cls")

    if not SOURCE_DATA_DESCRIPTION[source]["audio"].exists():
        save_audio()

    if not SOURCE_DATA_DESCRIPTION[source]["frames"].exists():
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


def chipi_chipi() -> None:
    run_animation("chipi-chipi")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-a", "--animation", type=str, default="chipi-chipi")
    args = arg_parser.parse_args()

    match args.animation:
        case "chipi-chipi":
            chipi_chipi()
        case _:
            exit("WTF!?")

