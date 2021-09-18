from decimal import Decimal

from tonescript import render
from tonescript.model import CadScript
from tonescript.model import CadenceSection
from tonescript.model import FreqScript
from tonescript.model import FrequencyComponent
from tonescript.model import ToneScript
from tonescript.model import ToneSegment


def test_8000_8():
    _render(8000, 1)


def test_8000_16():
    _render(8000, 2)


def test_44100_8():
    _render(44100, 1)


def test_44100_16():
    _render(44100, 2)


def _render(sample_rate: int, sample_width: int):
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

    path = f"./tone_{sample_rate}_{sample_width}.wav"
    render(ts, path, sample_rate, sample_width)
