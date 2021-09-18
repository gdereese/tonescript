"""
Object model for representing the structure and properties of ToneScripts and their components.
"""

from decimal import Decimal
from typing import Iterable
from typing import Sequence


class ToneSegment:
    """
    Segment of a tone with its own on/off pattern and frequency components.
    """

    def __init__(self, duration_on: Decimal = None, duration_off: Decimal = None, freq_nums: Iterable[int] = None):
        self.duration_off = duration_off
        """
        Duration of silence for the tone segment (in seconds).
        """

        self.duration_on = duration_on
        """
        Duration of sound for the tone segment (in seconds).
        """

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
        """
        List of frequency component ordinals (numbers) to use for the building the sound for this
        tone segment. The numbers used should correspond to their sequence in an associated
        FreqScript object. `1` corresponds to the first defined frequency component, and
        so on.
        """

        return self._freq_nums


class CadenceSection:
    """
    Section of a CadScript that defines a grouped sequence of tone segments.

    Segments within a section are sounded for a specified duration, looping the segments if
    necessary, before proceeding to the next section.
    """

    def __init__(self, duration: Decimal = None, segments: Iterable[ToneSegment] = None):
        self.duration = duration
        """
        Duration of the cadence section (in seconds). If the value is infinite, the section will
        play/loop indefinitely.
        """

        self.segments = list(segments)
        """
        Sequence of tone segments for this section.
        """

    def __str__(self):
        if self.duration.is_infinite():
            duration = "*"
        else:
            duration = f"{self.duration:.3g}s"

        return f"<{self.__class__.__name__} duration={duration} segments={len(self.segments)}>"


class CadScript:
    """
    Defines the cadence of a call progress tone, which is the pattern of frequencies and duration
    of any sound or silence.
    """

    def __init__(self, sections: Iterable[CadenceSection] = None):
        self.sections = list(sections)
        """
        Sequence of individual cadence sections.
        """

    def __str__(self):
        return f"<{self.__class__.__name__} sections={len(self.sections)}>"


class FrequencyComponent:
    """
    Component used in building all or part of a tone's audio waveform.

    The tone can use one or more different frequency and sound level values.
    """

    def __init__(self, frequency: int = None, level: Decimal = None):
        self.frequency = frequency
        """
        Frequency, in hertz (Hz).
        """

        self.level = level
        """
        Level of audio, in decibel-millivolts (dBm). Values are typically 0 (maximum level) and less.
        """

    def __str__(self):
        return f"<{self.__class__.__name__} frequency={self.frequency}Hz level={self.level:.1g}dBm>"


class FreqScript:
    """
    Defines the frequency components of a call progress tone.
    """

    def __init__(self, components: Iterable[FrequencyComponent] = None):
        self.components = list(components)
        """
        Sequence of frequency components. These components are referenced by sections of
        a CadScript.
        """

    def __str__(self):
        return f"<{self.__class__.__name__} components={len(self.components)}>"


class ToneScript:
    """
    Defines the complete frequency and cadence characteristics of a call progress tone.
    """

    def __init__(self, freqscript: FreqScript = None, cadscript: CadScript = None):
        self.cadscript = cadscript or CadScript()
        """
        Cadence of the tone.
        """

        self.freqscript = freqscript or FreqScript()
        """
        Frequency components of the tone.
        """

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
