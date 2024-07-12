import argparse
import math
import os
import shutil
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


try:
    from run_animation.sources import DATA_DESCRIPTION
except:
    from sources import DATA_DESCRIPTION

RED = "\u001b[31m"
GREEN = "\u001b[32m"
CYAN = "\u001b[36m"

RESET_PRINT = "\u001b[m"
RESET_CURSOR = "\u001b[H"
CLEAR_TERMINAL = "\u001b[2J"

ANIMATIONS_DESCRIPTIONS = DATA_DESCRIPTION.copy()


def customize_frames(source: str) -> None:
    global ANIMATIONS_DESCRIPTIONS
    if ANIMATIONS_DESCRIPTIONS[source]["chosen_scale"] != ANIMATIONS_DESCRIPTIONS[source]["base_scale"]:
        print(f"Chosen downscale: {ANIMATIONS_DESCRIPTIONS[source]['chosen_scale']}")
        ANIMATIONS_DESCRIPTIONS[source]["frames"] = ANIMATIONS_DESCRIPTIONS[source]["frames"] / str(
            ANIMATIONS_DESCRIPTIONS[source]['chosen_scale'])
        return

    size = os.get_terminal_size()

    width = size.columns
    height = size.lines

    if width < 1:
        ANIMATIONS_DESCRIPTIONS[source]["frames"] = ANIMATIONS_DESCRIPTIONS[source]["frames"] / str(
            ANIMATIONS_DESCRIPTIONS[source]["base_scale"])
        ANIMATIONS_DESCRIPTIONS[source]['chosen_scale'] = ANIMATIONS_DESCRIPTIONS[source]['base_scale']
        return

    scale_width: int = math.ceil(
        ANIMATIONS_DESCRIPTIONS[source]["resolution_multiplier"] * ANIMATIONS_DESCRIPTIONS[source]["resolution"][
            0] / width)
    scale_height: int = math.ceil(ANIMATIONS_DESCRIPTIONS[source]["resolution"][1] / height)
    total_downscale: int = max(scale_height, scale_width)

    if total_downscale > ANIMATIONS_DESCRIPTIONS[source]["base_scale"]:
        print(
            "Terminal size doesn't allow default configuration, both sizes should be higher tha needed:"
        )
        print(
            f"Width: actual - {width}, needed - {int(ANIMATIONS_DESCRIPTIONS[source]['resolution_multiplier'] * ANIMATIONS_DESCRIPTIONS[source]['resolution'][0] / 33)}"
        )
        print(f"Height: actual - {height}, needed - {int(ANIMATIONS_DESCRIPTIONS[source]['resolution'][1] / 33)}")

        ANIMATIONS_DESCRIPTIONS[source]["frames"] = ANIMATIONS_DESCRIPTIONS[source]["frames"] / str(total_downscale)
        ANIMATIONS_DESCRIPTIONS[source]['chosen_scale'] = total_downscale

        print(f"Your total downscale is {total_downscale}")
    else:
        ANIMATIONS_DESCRIPTIONS[source]["frames"] = ANIMATIONS_DESCRIPTIONS[source]["frames"] / str(
            ANIMATIONS_DESCRIPTIONS[source]['base_scale'])

    return


def get_timer(source: str) -> FPSTimer:
    info: vid_info = vid_info(str(ANIMATIONS_DESCRIPTIONS[source]["video"]))
    framerate: int = info.get_framerate()
    timer = FPSTimer(framerate)
    return timer


def save_audio(source: str) -> None:
    ANIMATIONS_DESCRIPTIONS[source]["audio"].parent.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(ANIMATIONS_DESCRIPTIONS[source]["video"], "mp4")
    audio.export(ANIMATIONS_DESCRIPTIONS[source]["audio"], format="mp3")


def save_frames(source: str) -> None:
    with Progress() as progress:

        ANIMATIONS_DESCRIPTIONS[source]["video"].parent.mkdir(parents=True, exist_ok=True)
        frame_info: vid_info = vid_info(str(ANIMATIONS_DESCRIPTIONS[source]["video"]))

        ANIMATIONS_DESCRIPTIONS[source]["total_frames"] = int(frame_info.get_framecount())

        generating = progress.add_task(
            "[red]Generating custom scale frames: ", total=int(frame_info.get_framecount())
        )
        ANIMATIONS_DESCRIPTIONS[source]["frames"].mkdir(parents=True, exist_ok=True)
        try:
            for frame_number in range(int(frame_info.get_framecount())):
                image = frame_info.get_frame(frame_number)
                frame: to_ascii = to_ascii(
                    image, ANIMATIONS_DESCRIPTIONS[source]["chosen_scale"],
                    width_multiplication=ANIMATIONS_DESCRIPTIONS[source]["resolution_multiplier"]
                )

                frame_colored: str = frame.asciify_colored()
                progress.update(generating, advance=1)
                with open(ANIMATIONS_DESCRIPTIONS[source]["frames"] / f"{frame_number}.txt", "w") as f:
                    f.write(frame_colored)
        except KeyError as e:
            shutil.rmtree(ANIMATIONS_DESCRIPTIONS[source]["frames"])

def prepare_package():
    for source in ANIMATIONS_DESCRIPTIONS.keys():
        if not ANIMATIONS_DESCRIPTIONS[source]["audio"].exists():
            save_audio(source)
        ANIMATIONS_DESCRIPTIONS[source]["frames"] = ANIMATIONS_DESCRIPTIONS[source]["frames"] / str(
            ANIMATIONS_DESCRIPTIONS[source]["base_scale"])
        if not ANIMATIONS_DESCRIPTIONS[source]["frames"].exists():
            ANIMATIONS_DESCRIPTIONS[source]["frames"].mkdir(parents=True, exist_ok=True)
            save_frames(source)

    print("READY!!!!")

def load_frames(source: str) -> list[str]:
    frames: list[str] = []
    for index in range(ANIMATIONS_DESCRIPTIONS[source]["total_frames"]):
        with open(ANIMATIONS_DESCRIPTIONS[source]["frames"] / f"{index}.txt", "r") as f:
            frame = f.read()
        frames.append(frame)
    return frames


def play(frames: list[str], source: str) -> None:
    timer: FPSTimer = get_timer(source)
    print(CLEAR_TERMINAL)

    playsound(ANIMATIONS_DESCRIPTIONS[source]["audio"], block=False)
    for frame in frames:
        print(RESET_CURSOR + frame + RESET_PRINT)
        timer.sleep()


def run_animation(source: str) -> None:
    customize_frames(source)

    if os.name == "nt":
        os.system("cls")

    if not ANIMATIONS_DESCRIPTIONS[source]["audio"].exists():
        save_audio(source)

    if not ANIMATIONS_DESCRIPTIONS[source]["frames"].exists():
        save_frames(source)

    try:
        frames: list[str] = load_frames(source)
        cursor.hide()

        while True:
            play(frames, source)
    except KeyboardInterrupt:
        cursor.show()
        print(CLEAR_TERMINAL + RESET_CURSOR + RESET_PRINT)
        print("UwU :3")


def chipi_chipi() -> None:
    args = sys.argv
    if len(args) > 1:
        ANIMATIONS_DESCRIPTIONS["chipi-chipi"]["chosen_scale"] = int(args[1])
    run_animation("chipi-chipi")


if __name__ == "__main__":

    translator = {
        "chipi": "chipi-chipi",
        "shikonoko": "shikonoko",
        "02": "02",
        "catcher": "shigure-catcher",
        "loli": "shigure-loli",
        "kiss": "kiss-me",
    }

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--prepare", help='Prepare package for build', action='store_true')
    arg_parser.add_argument("-a", "--animation", type=str, help='Animation', default="chipi")
    arg_parser.add_argument("-s", "--scale", help='Downscale value - don\'t use if not familiar with code', type=int,
                            default=-1)
    args = arg_parser.parse_args()

    if args.prepare:
        prepare_package()
        exit()

    animation_name = translator.get(args.animation)

    if animation_name is None:
        print(f"You chose wrong animation >:3")
        exit()

    if args.scale != -1:
        ANIMATIONS_DESCRIPTIONS[animation_name]["chosen_scale"] = args.scale
    else:
        ANIMATIONS_DESCRIPTIONS[animation_name]["chosen_scale"] = ANIMATIONS_DESCRIPTIONS[animation_name]["base_scale"]

    run_animation(animation_name)
