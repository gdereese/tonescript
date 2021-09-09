from decimal import Decimal
from typing import MutableSequence
from typing import Sequence


class CadScriptSegment:
    def __init__(self,
        duration_on: Decimal = None,
        duration_off: Decimal = None,
        freq_nums: Sequence[int] = None
    ):
        self._freq_nums = list(freq_nums)

        self.duration_off = duration_off
        self.duration_on = duration_on

    def __str__(self) -> str:
        return f"{self.duration_on:.4g}/{self.duration_off:.4g}/{'+'.join(map(str, self.freq_nums))}"

    @property
    def freq_nums(self) -> MutableSequence[int]:
        return self._freq_nums


class CadScriptSection:
    def __init__(self,
        duration: Decimal = None,
        segments: Sequence[CadScriptSegment] = None
    ):
        self._segments = list(segments)

        self.duration = duration

    def __str__(self) -> str:
        return f"{self.duration:.4g}({','.join(map(str, self.segments))})"

    @property
    def audio_duration(self):
        if self.duration.is_infinite():
            return sum(s.duration_on + s.duration_off for s in self.segments)
        return self.duration

    @property
    def segments(self) -> MutableSequence[CadScriptSegment]:
        return self._segments


class CadScript:
    def __init__(self,
        sections: Sequence[CadScriptSection] = None
    ):
        self._sections = list(sections)

    def __str__(self) -> str:
        return ";".join(map(str, self.sections))

    @property
    def audio_duration(self):
        return sum(s.audio_duration for s in self.sections)

    @property
    def sections(self) -> MutableSequence[CadScriptSection]:
        return self._sections


class FreqScriptComponent:
    def __init__(self,
        frequency: int = None,
        level: Decimal = None
    ):
        self.frequency = frequency
        self.level = level

    def __str__(self) -> str:
        return f"{self.frequency}@{self.level:.2g}"


class FreqScript:
    def __init__(self,
        components: Sequence[FreqScriptComponent] = None
    ):
        self._components = list(components)

    def __str__(self) -> str:
        return ";".join(map(str, self.components))

    def components(self) -> MutableSequence[FreqScriptComponent]:
        return self._components


class ToneScript:
    def __init__(self,
        freqscript: FreqScript = None,
        cadscript: CadScript = None
    ):
        self._freqscript = freqscript or FreqScript()

        self.cadscript = cadscript

    def __str__(self) -> str:
        return f"{self.freqscript!s};{self.cadscript!s}"

    @property
    def freqscript(self) -> FreqScript:
        return self._freqscript
