import argparse
import json
import os
import sys

from cursor import cursor
from fpstimer import FPSTimer

try:
    from run_animation.animation import Animation, DIR
except ImportError:
    from animation import Animation, DIR

RED = "\u001b[31m"
GREEN = "\u001b[32m"
CYAN = "\u001b[36m"

RESET_PRINT = "\u001b[m"
RESET_CURSOR = "\u001b[H"
CLEAR_TERMINAL = "\u001b[2J"


class Runner:
    source: Animation
    frames: list[str]

    def __init__(self, source: Animation):
        self.source = source

    def play(self) -> None:
        timer: FPSTimer = self.source.get_timer()
        print(CLEAR_TERMINAL)

        self.source.play_music()
        for frame in self.frames:
            print(RESET_CURSOR + frame + RESET_PRINT)
            timer.sleep()

    def run_animation(self) -> None:
        size = os.get_terminal_size()
        self.source.customize_frames(size)

        if os.name == "nt":
            os.system("cls")

        if not self.source.audio_path.exists():
            self.source.save_audio()

        if not self.source.frames_path.exists():
            self.source.save_frames()

        try:
            self.frames = self.source.load_frames()
            cursor.hide()

            while True:
                self.play()
        except KeyboardInterrupt:
            cursor.show()
            print(CLEAR_TERMINAL + RESET_CURSOR + RESET_PRINT)
            print("UwU :3")


def prepare_data(to_prepare: dict[str, Animation]) -> None:
    for source in to_prepare.values():
        if not source.audio_path.exists():
            source.save_audio()
        source.frames_path = source.frames_path / str(source.scale)
        if not source.frames_path.exists():
            source.save_frames()
    print("READY!!!!")


def load_configuration() -> dict[str, Animation]:
    with open(DIR / "data_description.json", "r") as f:
        data: list[dict] = json.load(f)

    animations: dict[str, Animation] = {
        description["name"]: Animation(description["name"], description["resolution"], description["scale"])
        for description in data
    }
    return animations


def chipi_chipi() -> None:
    animations = load_configuration()
    args = sys.argv
    if len(args) > 1:
        animations["chipi-chipi"].chosen_scale = int(args[1])
    runner = Runner(animations["chipi-chipi"])
    runner.run_animation()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--prepare", help='Prepare package for build', action='store_true')
    arg_parser.add_argument("-a", "--animation", type=str, help='Animation', default="chipi_chipi")
    arg_parser.add_argument("-s", "--scale", help='Downscale value - don\'t use if not familiar with code', type=int,
                            default=-1)
    args = arg_parser.parse_args()

    animation_descriptions = load_configuration()
    if args.prepare:
        prepare_data(animation_descriptions)
        exit()

    animation_name = args.animation
    if animation_name not in animation_descriptions.keys():
        print(f"You chose wrong animation >:3")
        exit()

    animation = animation_descriptions[animation_name]
    if args.scale != -1:
        animation.chosen_scale = args.scale
    else:
        animation.chosen_scale = animation.scale

    runner = Runner(animation)
    runner.run_animation()


if __name__ == "__main__":
    main()
