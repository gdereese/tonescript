# pylint: disable=missing-module-docstring

import wave
from struct import pack

from .audio import generate
from .model import ToneScript


def render(tone: ToneScript, path: str, sample_rate: int, sample_width: int) -> None:
    """
    Writes the audio data for a ToneScript to a WAV file.

    WAV files written by this function will be single-channel (mono).
    """

    float_samples = generate(tone, sample_rate)

    int_samples = list(_float_to_pcm(f, sample_width) for f in float_samples)
    if sample_width == 1:
        buffer = pack(f"<{len(int_samples)}B", *int_samples)
    elif sample_width == 2:
        buffer = pack(f"<{len(int_samples)}h", *int_samples)
    else:
        raise ValueError(f"sample width not supported: {sample_width}")

    with wave.open(path, "wb") as file:
        file: wave.Wave_write
        file.setnchannels(1)
        file.setsampwidth(sample_width)
        file.setframerate(sample_rate)
        file.writeframes(buffer)


def _float_to_pcm(val: float, size: int) -> int:
    # based on formula for linear interpolation:
    # y_0 + (val - x_0) * ((y_1 - y_0) / (x_1 - x_0))
    # for each possible sample size, formula was simplified

    if size == 1:
        return round((val + 1.0) * 127.5)
    if size == 2:
        return round(-32768.0 + (val + 1.0) * 32767.5)
    raise ValueError(f"unable to convert 32-bit float to {size}-byte PCM value")
