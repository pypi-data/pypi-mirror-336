"""
cli.py
CLI for AutoLRC.
"""

import argparse
import os
import sys

import torch
import torch.cuda
import whisper

from . import lrc

VALID_WHISPER_MODELS: whisper.List[str] = whisper.available_models()


def verify_args(args_to_verify: argparse.Namespace) -> None:
    """
    Verifies arguments for the AutoLRC CLI.

    Args:
        args_to_verify (argparse.Namespace): Arguments to be verified.
    """
    if args_to_verify.model not in VALID_WHISPER_MODELS:
        raise ValueError(f"Model: '{args_to_verify.model}' is not a valid model.")
    if not os.path.exists(args_to_verify.music_dir):
        raise ValueError(f"No directory called '{args_to_verify.music_dir}' could be found.")


def initialize_parser() -> argparse.ArgumentParser:
    """
    Initializes the parser for the AutoLRC CLI.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate LRC files for your music."
    )
    parser.add_argument(
        "music_dir",
        type=str,
        help="The directory where the music you want to generate LRC files is located.",
    )

    arg_model_help: str = f"""
    The whisper model to use for Audio To Text. Default = turbo.
    List of available modes are {VALID_WHISPER_MODELS}.
    Learn more here https://github.com/openai/whisper
    """.strip()
    parser.add_argument("--model", help=arg_model_help, default="turbo")

    return parser


def main() -> None:
    """
    Main entry point of the AutoLRC CLI.
    """

    parser: argparse.ArgumentParser = initialize_parser()
    args: argparse.Namespace = parser.parse_args()

    try:
        verify_args(args)
    except ValueError as error:
        sys.exit(str(object=error))

    model_name: str = args.model
    music_dir: str = args.music_dir

    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    model: whisper.Whisper = whisper.load_model(model_name, device)

    lrc.generate_lrc_for_album(music_dir, model)


if __name__ == "__main__":
    main()
