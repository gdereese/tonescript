"""
Used for generating audio data from parsed ToneScript input.
"""

from decimal import Decimal
from functools import lru_cache
from itertools import chain
from itertools import cycle
from itertools import islice
from itertools import repeat
from math import ceil
from math import pi
from math import sin
from typing import Iterable
from typing import Sequence

from .model import CadenceSection
from .model import FrequencyComponent
from .model import ToneScript
from .model import ToneSegment


def generate(ts: ToneScript, sample_rate: int) -> Iterable[float]:
    """
    Generates the audio data for a ToneScript.

    Returns a iterable of audio samples represented as `float` values, ranging from `-1.0` to
    `1.0`. The tone can be produced by playing back the audio samples at the rate specified by
    the `sample_rate` argument.
    """

    return _expand_cadence(ts, sample_rate)


def _expand_cadence(ts: ToneScript, sample_rate: int) -> Iterable[float]:
    tone_secs = (
        _expand_sec(sec, ts.freqscript.components, sample_rate)
        for sec
        in ts.cadscript.sections
    )

    return chain(*tone_secs)


def _expand_sec(sec: CadenceSection, comps: Sequence[FrequencyComponent], sample_rate: int) -> Iterable[float]:
    if sec.duration.is_infinite():
        sec_duration = sum(s.duration_on + s.duration_off for s in sec.segments)
    else:
        sec_duration = sec.duration
    sec_sample_count = ceil(sec_duration * sample_rate)

    tone_segs = (
        _expand_seg(seg, comps, sec_sample_count, sample_rate)
        for seg
        in sec.segments
    )

    return chain(*tone_segs)


def _expand_seg(seg: ToneSegment, comps: Sequence[FrequencyComponent], max_len: int, sample_rate: int) -> Iterable[float]:
    # get list of frequency components used by this segment
    seg_comps = [comps[n - 1] for n in seg.freq_nums if n > 0]

    # get sine wave generators for each component
    wave_comps = (cycle(_freq_comp(comp.frequency, comp.level, sample_rate)) for comp in seg_comps)

    # combine sine waves to get tone waveform
    wave = map(sum, zip(*wave_comps))

    if seg.duration_on.is_infinite():
        on_sample_count = max_len
    else:
        on_sample_count = min(ceil(seg.duration_on * sample_rate), max_len)
    tone_on = islice(wave, on_sample_count)

    if seg.duration_off.is_infinite():
        off_sample_count = max_len
    else:
        off_sample_count = min(ceil(seg.duration_off * sample_rate), max_len)
    tone_off = repeat(0, off_sample_count)

    return chain(tone_on, tone_off)


@lru_cache
def _freq_comp(frequency: int, level: Decimal, sample_rate: int) -> Sequence[float]:
    # convert level in dBm (decibel-millivolt) to amplitude/power in mW (milliwatt)
    #   mW = 10 ^ (dBm / 10)
    # 1 mW = 0 dBm
    amplitude = 10 ** (float(level) / 10)

    period = ceil(sample_rate / frequency)

    return [
        amplitude * sin(2 * pi * frequency * ((x % period) / sample_rate))
        for x
        in range(period)
    ]
