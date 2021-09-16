from decimal import Decimal

from lark import Lark
from lark import Token
from lark import v_args
from lark.visitors import Transformer

from .model import CadenceSection
from .model import CadScript
from .model import FreqScript
from .model import FrequencyComponent
from .model import ToneScript
from .model import ToneSegment


@v_args(inline=True)
class _TransformToModel(Transformer):
    def start(self, freqscript: FreqScript, cadscript: CadScript) -> ToneScript:
        return ToneScript(freqscript, cadscript)

    def freqscript(self, *components: FrequencyComponent) -> FreqScript:
        return FreqScript(components)

    def freq_comp(self, frequency: int, level: Decimal) -> FrequencyComponent:
        return FrequencyComponent(frequency, level)

    def cadscript(self, *sections: CadenceSection) -> CadScript:
        return CadScript(sections)

    def section(self, duration: int, *segments: ToneSegment) -> CadenceSection:
        return CadenceSection(duration, segments)

    def segment(self, duration_on: Decimal, duration_off: Decimal, *freq_nums: int) -> ToneSegment:
        return ToneSegment(duration_on, duration_off, freq_nums)

    def DURATION(self, token: Token) -> Decimal:
        if token.value == "*":
            return Decimal("inf")
        return Decimal(token.value)

    def LEVEL(self, token: Token) -> Decimal:
        return Decimal(token.value)

    def INT(self, token: Token) -> int:
        return int(token.value)


def parse(script: str) -> ToneScript:
    """
    Parses a ToneScript string into an equivalent object representation.
    """

    parser = Lark.open("tonescript.lark", rel_to=__file__)
    ast = parser.parse(script)

    model = _TransformToModel().transform(ast)

    return model


def unparse(obj: ToneScript) -> str:
    """
    Returns the equivalent script for a ToneScript object.
    """

    return _unparse_tonescript(obj)


def _duration_str(val: Decimal) -> str:
    if val.is_infinite():
        return "*"
    if 0 < val < 1:
        return f"{val:.4g}".lstrip('0')
    return f"{val:.4g}"


def _unparse_tone_segment(obj: ToneSegment) -> str:
    return f"{_duration_str(obj.duration_on)}/{_duration_str(obj.duration_off)}/{'+'.join(map(str, obj.freq_nums))}"


def _unparse_cadence_section(obj: CadenceSection) -> str:
    return f"{_duration_str(obj.duration)}({','.join(map(_unparse_tone_segment, obj.segments))})"


def _unparse_cadscript(obj: CadScript) -> str:
    return ";".join(map(_unparse_cadence_section, obj.sections))


def _unparse_freq_component(obj: FrequencyComponent) -> str:
    return f"{obj.frequency}@{obj.level:.3g}"


def _unparse_freqscript(obj: FreqScript) -> str:
    return ",".join(map(_unparse_freq_component, obj.components))


def _unparse_tonescript(obj: ToneScript) -> str:
    return f"{_unparse_freqscript(obj.freqscript)};{_unparse_cadscript(obj.cadscript)}"
