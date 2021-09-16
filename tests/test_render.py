from decimal import Decimal
from struct import pack
import wave

from tonescript.audio import render
from tonescript.model import CadScript
from tonescript.model import CadenceSection
from tonescript.model import FreqScript
from tonescript.model import FrequencyComponent
from tonescript.model import ToneScript
from tonescript.model import ToneSegment


def test_dial_tone():
    ts = ToneScript(
        FreqScript([
            FrequencyComponent(350, Decimal("-13")),
            FrequencyComponent(440, Decimal("-13"))
        ]),
        CadScript([
            CadenceSection(Decimal("10"), [
                ToneSegment(Decimal("inf"), Decimal("0"), [1, 2])
            ])
        ])
    )

    sample_rate = 44100
    float_samples = render(ts, sample_rate)
    int_samples = [int(s * 32767) for s in float_samples]
    audio_bytes = pack("<%dh" % len(int_samples), *int_samples)

    with wave.open("./tone.wav", "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_bytes)
