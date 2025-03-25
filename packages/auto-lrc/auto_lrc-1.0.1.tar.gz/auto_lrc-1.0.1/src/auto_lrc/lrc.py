"""
lrc.py
Generates lrc files for songs using OpenAI's Whisper model.

Credits:
https://github.com/openai/whisper
https://openai.com/index/whisper/
Thanks the for inspiration:
https://www.lrcgenerator.com/
https://github.com/openai/whisper
"""

import os

import whisper
from rich.console import Console

console = Console()


def seconds_to_lrc_timestamp(seconds: float) -> str:
    """
    Converts seconds to a valid lrc timestamp.
    The format is `mm:ss:ms`.

    Args:
        seconds (float): The number of seconds.

    Examples:
        >>> seconds_to_lrc_timestamp(84)
        01:24:00
        >>> seconds_to_lrc_timestamp(583.78)
        09:43.78
        >>> seconds_to_lrc_timestamp(84.123)
        01:24.12
    """
    minutes, seconds = divmod(seconds, 60)
    milliseconds = int(round((seconds - int(seconds)) * 100))
    return f"{int(minutes):02}:{int(seconds):02}.{milliseconds:02}"


def generate_lrc(audio_path: str, model: whisper.Whisper) -> str:
    """
    Converts audio to `lrc` format.

    Args:
        audio_path (str): The path of the audio file.
        model (whisper.Whisper): The openai whisper model to be used to process the audio to text.
    """
    result = model.transcribe(audio_path)

    segments = result.get("segments")

    if not isinstance(segments, list):
        raise TypeError(
            "Expected result to have segments, try using a different model or use a different version of whisper"
        )

    lrc_result: list[str] = []

    for segment in segments:
        lrc_timestamp: str = seconds_to_lrc_timestamp(segment["start"])
        text: str = segment["text"]
        text = text.strip()

        lrc_result.append(f"[{lrc_timestamp}]{text}")

    return "\n".join(lrc_result)


def get_music_files(music_path: str) -> list[str]:
    """
    Returns a list of valid music file paths found within a directory and its subdirectories.

    Args:
        music_path (str): The file path of the directory to search.

    Returns:
        List of strings that contain file paths of valid music files.
    """
    valid_files: list[str] = []
    valid_audio_extensions: list[str] = [".mp3", ".wav"]

    for root, _, files in os.walk(music_path):
        for file in files:
            extension: str = os.path.splitext(file)[-1].lower()

            if extension in valid_audio_extensions:
                full_path: str = os.path.join(root, file)
                valid_files.append(full_path)

    return valid_files


def get_filename_without_extension(path: str) -> str:
    """
    Take a filepath and returns the name of the file without its extension.

    Args:
        path (str): Path where the file is

    Returns:
        The filename without its extension
    """
    parts: tuple[str, str] = os.path.split(path)
    last_path: str = parts[-1]
    name: str = os.path.splitext(last_path)[0]
    return name


def generate_lrc_for_album(album_path: str, model: whisper.Whisper) -> None:
    """
    Generates `lrc` files for each song in a album. (The lrc files go into the album folder)
    The `lrc` file is the same name as the songs file name with its extension replaced with `lrc`.

    Args:
        album_path (str): The file path of the album.
        model (whisper.Whisper): The openai whisper model to be used to process the audio to text.

    Raises:
        FileNotFoundError: If the path to the album doesn't exist.
    """

    if not os.path.exists(album_path):
        raise FileNotFoundError(f"No file called '{album_path}' exists.")

    status_message = "[bold green]Generating lrc files {}/{} ..."

    music_file_paths: list[str] = get_music_files(album_path)
    total_files: int = len(music_file_paths)

    console.log(f"Found {total_files} songs!")

    with console.status(status_message.format(0, total_files)) as status:
        for file_num, file in enumerate(music_file_paths, 1):
            song_name = get_filename_without_extension(file)
            lrc_path = os.path.splitext(file)[0] + "." + "lrc"

            if os.path.exists(lrc_path):
                console.log(
                    f"[bold yellow]Skipping song: [blue]{song_name}[bold yellow], cause a lrc file already exists."
                )
            else:
                console.log(f"Processing song: [blue]{song_name}")
                lrc_data: str = generate_lrc(file, model)

                with open(lrc_path, "w", encoding="utf8") as f:
                    f.write(lrc_data)

            status.update(status_message.format(file_num, total_files))
