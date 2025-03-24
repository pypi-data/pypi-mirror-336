from __future__ import annotations

import sys
from enum import StrEnum
from subprocess import run


class Synthesizer(StrEnum):
    AMAZON_POLLY = "AMAZON_POLLY"
    ESPEAK_NG = "ESPEAK_NG"
    MAC_OS = "MAC_OS"


class SimpleTalk:
    def __init__(
        self,
        voice: str | None = None,
        synthesizer: Synthesizer = Synthesizer.MAC_OS,
    ) -> None:
        if synthesizer == Synthesizer.MAC_OS and sys.platform != "darwin":
            msg = "You must run the specified synthesizer on macOS."
            raise ValueError(msg)

        self.__voice: str | None = voice
        self.__synthesizer: Synthesizer = synthesizer

    def talk(
        self,
        text: str,
        filename: str,
    ) -> None:
        if self.__synthesizer == Synthesizer.MAC_OS:
            run(args=[
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
            ], check=True)
        elif self.__synthesizer == Synthesizer.ESPEAK_NG:
            run(args=[
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
            ], check=True)
        else:
            msg = "The specified synthesizer is not implemented yet."
            raise NotImplementedError(msg)
