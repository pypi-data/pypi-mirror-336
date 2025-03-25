"""
cli_v2.py
CLI v2 for AutoLRC.
"""

import os
from typing import Literal

import click
import torch
import whisper

from . import lrc

VALID_WHISPER_MODELS: whisper.List[str] = whisper.available_models()

DEFAULT_MODEL: str = "turbo"

CUDA_AVAILABLE: bool = torch.cuda.is_available()
DEFAULT_TORCH_DEVICE: Literal["cuda"] | Literal["cpu"] = "cuda" if CUDA_AVAILABLE else "cpu"

if DEFAULT_MODEL not in VALID_WHISPER_MODELS:
    raise ValueError(f"Whisper model: '{DEFAULT_MODEL}' is not in {VALID_WHISPER_MODELS}")


@click.command()
@click.option(
    "--model",
    default=DEFAULT_MODEL,
    help=f"""
    The whisper model to use for Audio To Text. Default = {DEFAULT_MODEL}.
    List of available modes are {VALID_WHISPER_MODELS}.
    Learn more here https://github.com/openai/whisper""".strip(),
)
@click.option("--music-dir", prompt="Music file or Album folder")
@click.option(
    "--device",
    default="auto",
    help=f"""
    Device to run whisper on.
    Devices:
    ✔: cpu
    {"✔" if CUDA_AVAILABLE else "✖"}: cuda {"(Cuda not found)" if not CUDA_AVAILABLE else ""}
    ✔: auto (auto set to {DEFAULT_TORCH_DEVICE})
    """,
)
def cli(model: str, music_dir: str, device: str):
    if model not in VALID_WHISPER_MODELS:
        raise click.exceptions.BadParameter(f"'{model}' is not a valid model.")
    if device not in ["cpu", "cuda", "auto"]:
        raise click.exceptions.BadParameter(f"'{device}' is not a valid device.")
    if not os.path.exists(music_dir):
        raise click.exceptions.BadParameter(f"Could not find path '{music_dir}'")

    if device == "auto":
        device = DEFAULT_TORCH_DEVICE

    loaded_model: whisper.Whisper = whisper.load_model(name=model, device=device)

    lrc.generate_lrc_for_album(music_dir, loaded_model)


if __name__ == "__main__":
    cli()
