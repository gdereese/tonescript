# tonescript

Python package for working with ToneScript, a syntax for describing the characteristics of the call progress tones used in telephony. It is the primary method for configuring tones in Sipura, Linksys, and Cisco VoIP systems.

## Features

* Parses ToneScript into its components: frequencies, cadence sections, and tone segments
* Constructs ToneScript from component objects
* Generates tone audio from ToneScript objects

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
        1) Always on, using frequencies 1, 2
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

### Generating tone audio from ToneScript objects

```python
import tonescript as ts
import tonescript.audio as ts_audio

# standard North American dial tone
tone = ts.parse("350@-13,440@-13;10(*/0/1+2)")

# render audio as samples (32-bit float values)
sample_rate = 44100
float_samples = ts_audio.render(tone, sample_rate)

# convert float samples to 16-bit integers (PCM)
int_samples = [int(s * 32767) for s in float_samples]

# pack integer samples into byte array
audio_bytes = pack("<%dh" % len(int_samples), *int_samples)

# write audio into WAV file (Mono, 16-bit PCM, 8 kHz sample rate)
with wave.open("./tone.wav", "w") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_bytes)

```

## Support

TODO: use GitHub issues

## Contributing

### Installing for development

```shell
poetry install
```

### Linting source files

```shell
poetry run pylint src tests
```

### Running tests

```shell
poetry run pytest
```

TODO: workflow for branching and versioning

## License

This library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/MIT/).
