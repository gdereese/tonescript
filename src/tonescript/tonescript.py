import dataclasses
import decimal
import itertools
import typing

import lark.visitors
import lark
import numpy




@lark.v_args(inline=True)
class TransformToObject(lark.visitors.Transformer):
    def start(self, freqscript, cadscript):
        return ToneScript(
            freqscript,
            cadscript
        )

    def freqscript(self, *components):
        return FreqScript(
            components=list(components)
        )

    def freq_comp(self, frequency, level):
        return FreqScriptComponent(
            frequency=frequency,
            level=level
        )

    def cadscript(self, *sections):
        return CadScript(
            sections=sections
        )

    def section(self, duration, *segments):
        return CadScriptSection(
            duration=duration,
            segments=list(segments)
        )

    def segment(self, dur_on, dur_off, *freq_nums):
        return CadScriptSegment(
            duration_on=dur_on,
            duration_off=dur_off,
            freq_nums=list(freq_nums)
        )

    def DURATION(self, token):
        if token.value == "*":
            return decimal.Decimal("inf")
        return decimal.Decimal(token.value)

    def LEVEL(self, token):
        return decimal.Decimal(token.value)

    def INT(self, token):
        return int(token.value)


class ToneScriptParser:
    _lark: lark.Lark = None

    @classmethod
    def get(cls) -> lark.Lark:
        if not cls._lark:
            cls._lark = lark.Lark.open("tonescript.lark", rel_to=__file__)
        return cls._lark


def parse(script: str) -> ToneScript:
    """
    Parses a ToneScript string into an equivalent object representation.
    """

    ast = ToneScriptParser.get().parse(script)

    return TransformToObject().transform(ast)


def as_audio(ts: ToneScript, sample_rate: float, dtype=None) -> numpy.array:
    result = numpy.array([], dtype=dtype)

    for duration, freqs in _expand(ts):
        sample_count = int(numpy.ceil(float(duration) * sample_rate))
        segment = numpy.zeros(sample_count, dtype=dtype)

        if freqs:
            amp = 1 / len(freqs)
            for freq in freqs:
                x = numpy.linspace(0, float(duration), num=sample_count, dtype=dtype)
                segment += amp * numpy.sin(2 * numpy.pi * freq * x)
        result = numpy.append(result, segment)

    return result


def _expand(ts: ToneScript) -> typing.Iterable[typing.Tuple[float, typing.Sequence[int]]]:
    for section in ts.cadscript.sections:
        duration_remain = section.audio_duration

        for segment in itertools.takewhile(lambda _: duration_remain > 0, itertools.cycle(section.segments)):
            duration_on = max(0, min(duration_remain, segment.duration_on))
            if duration_on > 0:
                freqs = [ts.freqscript.components[n - 1].frequency for n in segment.freq_nums if n > 0]
                yield (duration_on, freqs)
                duration_remain -= duration_on

            duration_off = max(0, min(duration_remain, segment.duration_off))
            if duration_off > 0:
                yield (duration_off, None)
                duration_remain -= duration_off
