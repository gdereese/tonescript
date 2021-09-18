from decimal import Decimal
from typing import Sequence

from tonescript import unparse
from tonescript.model import CadenceSection
from tonescript.model import CadScript
from tonescript.model import FreqScript
from tonescript.model import FrequencyComponent
from tonescript.model import ToneScript
from tonescript.model import ToneSegment


class TestUnparse:
    def test_unparse_script_1(self):
        # Contains 2 frequency components
        # Frequency component 1 is 350 Hz at -19 dBm
        # Frequency component 2 is 440 Hz at -19 dBm
        # There is 1 Cadence Section
        # In this section, The duration is 10 seconds and the tone has only 1 subsections
        # In the only subsection the tone is always on, off for 0 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)

        self.given_component(350, Decimal("-19"))
        self.given_component(440, Decimal("-19"))
        self.given_section(Decimal("10"))
        self.given_segment(0, Decimal("inf"), Decimal("0"), [1, 2])
        self.when_unparsed()
        self.then_result_is("350@-19,440@-19;10(*/0/1+2)")

    def test_unparse_script_2(self):
        # Contains 2 frequency components
        # Frequency component 1 is 350 Hz at -19 dBm
        # Frequency component 2 is 440 Hz at -19 dBm
        # There are two Cadence Sections
        # In the first Cadence Section, The duration is 2 seconds and the tone has only 1 subsections
        # In the only subsection the tone is on for 0.2 seconds, off for 0.2 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)
        # In the second Cadence Section, The duration is 10 seconds and again the tone has only 1 subsections
        # In the only subsection the tone is always on, off for 0 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)

        self.given_component(350, Decimal("-19"))
        self.given_component(440, Decimal("-19"))
        self.given_section(Decimal("2"))
        self.given_segment(0, Decimal("0.2"), Decimal("0.2"), [1, 2])
        self.given_section(Decimal("10"))
        self.given_segment(1, Decimal("inf"), Decimal("0"), [1, 2])
        self.when_unparsed()
        self.then_result_is("350@-19,440@-19;2(.2/.2/1+2);10(*/0/1+2)")

    def test_unparse_script_3(self):
        # Christmas theme dialtone (seven notes of ′The First Noel′ then continuous dialtone for 30 seconds)
        # Contains 6 frequency components
        # Frequency components are 349, 392, 440, 466, 523 and 540 Hz (five musical notes) plus a beat frequency tone mix to give a warble dialtone beat thereafter.
        # There are two Cadence Sections
        # In the first Cadence Section, the total duration is 2.1 seconds and the tone has 6 subsections with timing set for music.
        # The tones are turned on and off to give the ′notes′ of the familiar Christmas carol.
        # In the second Cadence Section, the duration is 30 seconds. It combines tones 5 and 6 to give the last note and the familiar 17 Hz beat of dialtone.

        self.given_component(349, Decimal("-21"))
        self.given_component(392, Decimal("-21"))
        self.given_component(440, Decimal("-21"))
        self.given_component(466, Decimal("-21"))
        self.given_component(523, Decimal("-24"))
        self.given_component(540, Decimal("-24"))
        self.given_section(Decimal("2.1"))
        self.given_segment(0, Decimal("0.6"), Decimal("0"), [3])
        self.given_segment(0, Decimal("0.2"), Decimal("0"), [2])
        self.given_segment(0, Decimal("0.7"), Decimal("0"), [1])
        self.given_segment(0, Decimal("0.2"), Decimal("0"), [2])
        self.given_segment(0, Decimal("0.2"), Decimal("0"), [3])
        self.given_segment(0, Decimal("0.3"), Decimal("0"), [4])
        self.given_section(Decimal("30"))
        self.given_segment(1, Decimal("inf"), Decimal("0"), [5, 6])
        self.when_unparsed()
        self.then_result_is("349@-21,392@-21,440@-21,466@-21,523@-24,540@-24;2.1(.6/0/3,.2/0/2,.7/0/1,.2/0/2,.2/0/3,.3/0/4);30(*/0/5+6)")

    def test_unparse_script_4(self):
        # New Year theme dialtone (four notes of ′Auld Lang Syne′ then continuous dialtone for 30 seconds)
        # Contains 5 frequency components
        # Frequency components are 392, 440, 494, 292 and 457 Hz (four musical notes) plus a beat frequency tone mix to give a warble dialtone beat thereafter.
        # There are two Cadence Sections
        # In the first Cadence Section, the total duration is 3.5 seconds and the tone has 6 subsections with timing set for music.
        # The tones are turned on and off to give the ′notes′ of the familiar New Year's Eve tune.
        # In the second Cadence Section, the duration is 30 seconds. It combines tones 4 and 5 to give the last note in the familiar 17 Hz beat of dialtone.

        self.given_component(392, Decimal("-19"))
        self.given_component(440, Decimal("-19"))
        self.given_component(494, Decimal("-19"))
        self.given_component(294, Decimal("-19"))
        self.given_component(457, Decimal("-19"))
        self.given_section(Decimal("3.5"))
        self.given_segment(0, Decimal("0.7"), Decimal("0"), [4])
        self.given_segment(0, Decimal("0.8"), Decimal("0"), [1])
        self.given_segment(0, Decimal("0.6"), Decimal("0"), [1])
        self.given_segment(0, Decimal("0.5"), Decimal("0"), [3])
        self.given_segment(0, Decimal("0.7"), Decimal("0"), [2])
        self.given_segment(0, Decimal("0.2"), Decimal("0"), [1])
        self.given_section(Decimal("30"))
        self.given_segment(1, Decimal("inf"), Decimal("0"), [2, 5])
        self.when_unparsed()
        self.then_result_is("392@-19,440@-19,494@-19,294@-19,457@-19;3.5(.7/0/4,.8/0/1,.6/0/1,.5/0/3,.7/0/2,.2/0/1);30(*/0/2+5)")

    def given_component(self, frequency: int, level: Decimal):
        if not "_components" in dir(self):
            self._components = []
        self._components.append((frequency, level))

    def given_section(self, duration: Decimal):
        if not "_sections" in dir(self):
            self._sections = []
        self._sections.append((duration, []))

    def given_segment(self, section_idx: int, duration_on: Decimal, duration_off: Decimal, freq_nums: Sequence[int]):
        self._sections[section_idx][1].append((duration_on, duration_off, freq_nums))

    def when_unparsed(self):
        self._tone = ToneScript(
            FreqScript([
                FrequencyComponent(frequency, level)
                for frequency, level
                in self._components
            ]),
            CadScript([
                CadenceSection(duration, [
                    ToneSegment(duration_on, duration_off, freq_nums)
                    for duration_on, duration_off, freq_nums
                    in segments
                ])
                for duration, segments
                in self._sections
            ])
        )

        self._result = unparse(self._tone)

    def then_result_is(self, script: str):
        assert self._result == script
