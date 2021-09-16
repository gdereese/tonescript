"""
Object model for representing the structure and properties of ToneScripts and their components.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence


@dataclass
class ToneSegment:
    duration_on: Decimal
    duration_off: Decimal
    freq_nums: Sequence[int]

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


@dataclass
class CadenceSection:
    duration: Decimal
    segments: Sequence[ToneSegment]

    def __str__(self):
        if self.duration.is_infinite():
            duration = "*"
        else:
            duration = f"{self.duration:.3g}s"

        return f"<{self.__class__.__name__} duration={duration} segments={len(self.segments)}>"


@dataclass
class CadScript:
    sections: Sequence[CadenceSection]

    def __str__(self):
        return f"<{self.__class__.__name__} sections={len(self.sections)}>"


@dataclass
class FrequencyComponent:
    frequency: int
    level: Decimal

    def __str__(self):
        return f"<{self.__class__.__name__} frequency={self.frequency}Hz level={self.level:.1g}dBm>"


@dataclass
class FreqScript:
    components: Sequence[FrequencyComponent]

    def __str__(self):
        return f"<{self.__class__.__name__} components={len(self.components)}>"


@dataclass
class ToneScript:
    freqscript: FreqScript
    cadscript: CadScript

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
