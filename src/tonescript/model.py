"""
Object model for representing the structure and properties of ToneScripts and their components.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable
from typing import Sequence


@dataclass
class ToneSegment:
    def __init__(self, duration_on: Decimal = None, duration_off: Decimal = None, freq_nums: Iterable[int] = None):
        self.duration_off = duration_off
        self.duration_on = duration_on
        self._freq_nums = list(freq_nums)

    def __str__(self):
        if self.duration_on.is_infinite():
            duration_on = "*"
        else:
            duration_on = f"{self.duration_on:.3g}s"

        if self.duration_off.is_infinite():
            duration_off = "*"
        else:
            duration_off = f"{self.duration_off:.3g}s"

        return f"{self.__class__.__name__} on={duration_on} off={duration_off} frequencies={self.freq_nums}>"

    @property
    def freq_nums(self) -> Sequence[int]:

        return self._freq_nums


class CadenceSection:
    def __init__(self, duration: Decimal = None, segments: Iterable[ToneSegment] = None):
        self.duration = duration
        self.segments = list(segments)

    def __str__(self):
        if self.duration.is_infinite():
            duration = "*"
        else:
            duration = f"{self.duration:.3g}s"

        return f"<{self.__class__.__name__} duration={duration} segments={len(self.segments)}>"


@dataclass
class CadScript:
    def __init__(self, sections: Iterable[CadenceSection] = None):
        self.sections = list(sections)

    def __str__(self):
        return f"<{self.__class__.__name__} sections={len(self.sections)}>"


@dataclass
class FrequencyComponent:
    def __init__(self, frequency: int = None, level: Decimal = None):
        self.frequency = frequency
        self.level = level

    def __str__(self):
        return f"<{self.__class__.__name__} frequency={self.frequency}Hz level={self.level:.1g}dBm>"


@dataclass
class FreqScript:
    def __init__(self, components: Iterable[FrequencyComponent] = None):
        self.components = list(components)

    def __str__(self):
        return f"<{self.__class__.__name__} components={len(self.components)}>"


@dataclass
class ToneScript:
    def __init__(self, freqscript: FreqScript = None, cadscript: CadScript = None):
        self.cadscript = cadscript or CadScript()
        self.freqscript = freqscript or FreqScript()

    def __str__(self):
        lines = []

        lines.append("Frequency components:")
        for comp_idx, comp in enumerate(self.freqscript.components):
            lines.append(f"    {comp_idx + 1}) {comp.frequency} Hz @ {int(comp.level):.3g} dBm")

        lines.append("Cadence sections:")
        for sec_idx, sec in enumerate(self.cadscript.sections):
            lines.append(f"    {sec_idx + 1}) For {sec.duration:.4g} s:")
            for seg_idx, seg in enumerate(sec.segments):
                duration_parts = []
                if seg.duration_on.is_infinite():
                    duration_parts.append("Always on")
                else:
                    duration_parts.append("On for {seg.duration_on:.4g} s")
                if seg.duration_off.is_infinite():
                    duration_parts.append("Always off")
                elif seg.duration_off != 0:
                    duration_parts.append(f"Off for {seg.duration_off:.4g} s")
                duration = ", ".join(duration_parts)
                lines.append(f"        {seg_idx + 1}) {duration}, using frequencies {', '.join(map(str, seg.freq_nums))}")

        return "\n".join(lines)
