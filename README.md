# tonescript

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/tonescript/CI/main?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/tonescript?style=for-the-badge)

Python package for working with ToneScript, a syntax for describing the characteristics of the call progress tones used in telephony. It is the primary method for configuring tones in Sipura, Linksys, and Cisco VoIP systems.

## Features

* Parses ToneScript into its components: frequencies, cadence sections, and tone segments
* Constructs ToneScript from component objects
* Renders ToneScript objects into WAV audio files

## Installation

```shell
pip install tonescript
```

## Overview of ToneScript syntax

For example, the **ToneScript** that defines the standard North American dial tone is as follows:

```text
350@-13,440@-13;10(*/0/1+2)
```

`350@-13,440@-13` is the **FreqScript** portion, which describes the frequency components used to make up the sound heard in the tone. The audio frequency (in Hz) and level (in dBm) are specified for each component, and each component is separated by a comma (`,`).

This FreqScript defines 2 frequency components:

1. 350 Hz @ -13 dBm
2. 440 Hz @ -13 dBm

`10(*/0/1+2)` is the **CadScript** portion, which describes the cadence of the tone, or the rhythm of its defined frequency components and silence.

The tone is divided into sections, each of which has its own sequence of tone segments.

A tone segment plays using one or more of the frequency components defined in the FreqScript for a specified duration (in seconds), followed by an optional period of silence.

A cadence section can also have its own duration; the tone segments within it are played and looped as needed until the section duration has elapsed.

When specifying duration values, an asterisk (`*`) indicates that the duration is continuous.

The above CadScript defines a single section which plays for 10 seconds. The section has a single tone segment:

* `*` = Plays continuously
* `0` = No silence
* `1+2` = Uses the first and second frequency components in the list

## Usage

### Parsing a ToneScript

```python
import tonescript as ts

# standard North American dial tone
script = "350@-13,440@-13;10(*/0/1+2)"

tone = ts.parse(script)

print(str(tone))
```

**Output:**

```shell
Frequency components:
    1) 350 Hz @ -13 dBm
    2) 440 Hz @ -13 dBm
Cadence sections:
    1) For 10 s:
        1) Always on, frequencies 1, 2
```

### Constructing a ToneScript

```python
from decimal import Decimal

import tonescript as ts
import tonescript.model as ts_model

# standard North American dial tone
tone = ts_model.ToneScript(
    ts_model.FreqScript([
        ts_model.FrequencyComponent(350, Decimal("-13")),
        ts_model.FrequencyComponent(440, Decimal("-13"))
    ]),
    ts_model.CadScript([
        ts_model.CadenceSection(Decimal("10"), [
            ts_model.ToneSegment(Decimal("inf"), Decimal("0"), [1, 2])
        ])
    ])
)

script = ts.unparse(tone)

print(script)
```

**Output:**

```shell
350@-13,440@-13;10(*/0/1+2)
```

### Rendering a ToneScript into a WAV audio file

```python
import tonescript as ts

# standard North American dial tone
tone = ts.parse("350@-13,440@-13;10(*/0/1+2)")

# 16-bit PCM, 44.1 kHz sample rate
ts.render(tone, "./dial_tone.wav", 44100, 2)
```

## Support

Please use the project's [Issues page](https://github.com/gdereese/tonescript/issues) to report any issues.

## Contributing

### Installing for development

```shell
poetry install
```

### Linting source files

```shell
poetry run pylint --rcfile .pylintrc src/tonescript
```

### Running tests

```shell
poetry run pytest
```

## License

This library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
