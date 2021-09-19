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

### Building HTML documentation

#### For development

```shell
poetry run pdoc --template-dir docs_template --http : tonescript
```

#### For distribution or deployment

```shell
poetry run pdoc --template-dir docs_template --html tonescript
```

## License

This library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
