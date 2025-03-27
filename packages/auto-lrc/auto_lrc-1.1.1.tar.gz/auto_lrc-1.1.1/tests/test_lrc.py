"""
Tests for AutoLRC
"""

import os
import tempfile

import whisper

from auto_lrc import lrc


class TestSecondsToLrcTimestamp:
    def test_seconds(self):
        assert lrc.seconds_to_lrc_timestamp(32) == "00:32.00"
        assert lrc.seconds_to_lrc_timestamp(1) == "00:01.00"
        assert lrc.seconds_to_lrc_timestamp(15) == "00:15.00"

    def test_seconds_milliseconds(self):
        assert lrc.seconds_to_lrc_timestamp(54.3) == "00:54.30"
        assert lrc.seconds_to_lrc_timestamp(1.54) == "00:01.54"
        assert lrc.seconds_to_lrc_timestamp(seconds=59.99) == "00:59.99"

    def test_milliseconds(self):
        assert lrc.seconds_to_lrc_timestamp(0.01) == "00:00.01"
        assert lrc.seconds_to_lrc_timestamp(0.99) == "00:00.99"
        assert lrc.seconds_to_lrc_timestamp(0.5) == "00:00.50"

    def test_minutes(self):
        assert lrc.seconds_to_lrc_timestamp(60) == "01:00.00"
        assert lrc.seconds_to_lrc_timestamp(120) == "02:00.00"
        assert lrc.seconds_to_lrc_timestamp(600) == "10:00.00"

    def test_minutes_seconds(self):
        assert lrc.seconds_to_lrc_timestamp(90) == "01:30.00"
        assert lrc.seconds_to_lrc_timestamp(150.75) == "02:30.75"
        assert lrc.seconds_to_lrc_timestamp(3599.99) == "59:59.99"


def test_generate_lrc():
    model: whisper.Whisper = whisper.load_model("tiny")

    result: str = lrc.generate_lrc("tests/audio.flac", model)
    
    # Expected format "[00:00.00]"
    #                  0123456789
    for line in result.splitlines():
        assert line[0] == '['
        assert line[1:3].isnumeric()
        assert line[3] == ':'
        assert line[4:6].isnumeric()
        assert line[6] ==  '.'
        assert line[7:9].isnumeric()
        assert line[9] == ']'


def test_get_music_files():
    with tempfile.TemporaryDirectory() as tempdirname:

        def create_file(name: str):
            with open(os.path.join(tempdirname, name), mode="wb") as f:
                f.write(bytes())

        def create_files(file_paths: list[str]):
            for file_path in file_paths:
                create_file(file_path)

        files = ["thing.mp3", "thing-2.mp3", "invalid.format"]

        create_files(files)

        result: list[str] = lrc.get_music_files(tempdirname)

        assert isinstance(result, list)

        for file in result:
            assert isinstance(file, str)

        assert "invalid.format" not in result
