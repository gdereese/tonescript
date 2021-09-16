## What is ToneScript?

According to [Wikipedia](https://en.wikipedia.org/wiki/ToneScript):

> ToneScript is a description syntax for the characteristics of call-progress tones.
>
> A call progress tone is a pattern of audible tones played to the caller in a telephone call, conveying the status of the call. ToneScript describes the pattern of frequency, cadence, and level of the signal. Many Internet telephony devices support configuration options for users to customize the tones, but standard patterns are provided for various telephone administrations. ToneScript is used in Sipura, Linksys and Cisco family of IP telephony products.

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

TODO

## Contributing

TODO

## License

This library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/MIT/).
