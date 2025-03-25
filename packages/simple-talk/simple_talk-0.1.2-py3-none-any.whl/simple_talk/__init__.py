from __future__ import annotations

import sys
from enum import StrEnum
from pathlib import Path
from subprocess import run
from typing import Any

try:
    import boto3
    polly_client: Any = boto3.client("polly")
except ImportError:
    polly_client = None


class Synthesizer(StrEnum):
    AMAZON_POLLY = "AMAZON_POLLY"
    ESPEAK_NG = "ESPEAK_NG"
    MAC_OS = "MAC_OS"


class SimpleTalk:
    def __init__(
        self,
        *,
        voice: str | None = None,
        synthesizer: Synthesizer = Synthesizer.MAC_OS,
        engine: str | None = None,
    ) -> None:
        if synthesizer == Synthesizer.MAC_OS and sys.platform != "darwin":
            msg = "You must run the specified synthesizer on macOS."
            raise ValueError(msg)

        if synthesizer == Synthesizer.AMAZON_POLLY:
            if not polly_client:
                msg = "You must install this package with extra for Amazon Polly."
                raise ValueError(msg)

            if not voice or not engine:
                msg = "You must specify engine and voice for Amazon Polly."
                raise ValueError(msg)

        self.__voice: str | None = voice
        self.__synthesizer: Synthesizer = synthesizer

    def talk(
        self,
        text: str,
        filename: str,
    ) -> str:
        match self.__synthesizer:
            case Synthesizer.MAC_OS:
                return self.__talk_macos(text, filename)
            case Synthesizer.ESPEAK_NG:
                return self.__talk_espeak(text, filename)
            case Synthesizer.AMAZON_POLLY:
                return self.__talk_polly(text, filename)
            case _:
                msg = "The specified synthesizer is not implemented yet."
                raise NotImplementedError(msg)

    def __talk_macos(
        self,
        text: str,
        filename: str,
    ) -> str:
        run(
            args=[
                "say",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "--file-format=mp4f",
                "-o",
                filename + ".mp4",
            ],
            check=True,
        )

        return filename + ".mp4"

    def __talk_espeak(
        self,
        text: str,
        filename: str,
    ) -> str:
        run(
            args=[
                "espeak-ng",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "-w",
                filename + ".wav",
            ],
            check=True,
        )

        return filename + ".wav"

    def __talk_polly(
        self,
        text: str,
        filename: str,
    ) -> str:
        response: dict[str, Any] = polly_client.synthesize_speech(
            OutputFormat="mp3",
            Text=text,
            VoiceId=self.__voice,
        )

        Path(filename + ".mp3").write_bytes(response["AudioStream"].read())

        return filename + ".mp3"
