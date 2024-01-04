# CHIPI CHIPI 
Small fun project.

# Install 
```bash
pip install chipi-chipi
```

# Run
```bash
chipi-chipi
```

## Windows users 
Sowwy guys I couldn't make it work on windows :'(

## Known issues
* Failed to build pycairo:
    ```bash
    apt install libcairo2-dev
    ```
* No package 'gobject-introspection-1.0' found:
    ```bash
    apt install libgirepository1.0-dev
    ```
* ImportError: libGL.so.1:
    ```bash
    apt install libgl1
    ```
* ValueError: Namespace Gst not available:
    ```bash
    apt install libgstreamer1.0-dev libgstreamer1.0-0 ffmpeg

    ```

# Acknowledgement
Package is based on digitPixelz's [terminal-video-player-py](https://pypi.org/project/terminal-video-player-py/). Thank your for your work!