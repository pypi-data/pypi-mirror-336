# AutoLRC

AutoLRC is a command-line that generates lyric files (.lrc) for your music locally using OpenAI's [Whisper](https://github.com/openai/whisper) model.

## Installation

Install AutoLRC with pip

```bash
pip install auto-lrc
```

AutoLRC depends on [FFmpeg](https://ffmpeg.org/) to be installed

## Usage

### CLI

```
AutoLRC --help
```

**Note:** the CLI may be slow to start as it has to import big packages.

### Options

- `--music-dir`: Path to the directory containing your music files.
- `--model`: Whisper model to use for transcription (default: `turbo`).
- `--device`: Device to run the transcription on (`cpu`, `cuda`, or default: `auto`).

## GPU Support

- Currently GPU support is only available Nvidia GPUs.
- CUDA 12.6 installed. (Other versions may work fine)

## Development

AutoLRC is built with [UV](https://docs.astral.sh/uv/)

1. Clone the repository:

```bash
git clone https://github.com/HeavyLvy/auto-lrc
```

2. Setup project:

```bash
uv sync
```
