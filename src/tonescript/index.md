## What is ToneScript?

According to [Wikipedia](https://en.wikipedia.org/wiki/ToneScript):

> ToneScript is a description syntax for the characteristics of call-progress tones.
>
> A call progress tone is a pattern of audible tones played to the caller in a telephone call, conveying the status of the call. ToneScript describes the pattern of frequency, cadence, and level of the signal. Many Internet telephony devices support configuration options for users to customize the tones, but standard patterns are provided for various telephone administrations. ToneScript is used in Sipura, Linksys and Cisco family of IP telephony products.

## Syntax

### ToneScript

```text
350@-13,440@-13;10(*/0/1+2)
```

* `350@-13,440@-13`: FreqScript
* `10(*/0/1+2)`: CadScript

<!-- .. math::
ToneScript \Leftarrow FreqScript \; ; \; CadScript \\
\; \\
FreqScript \Leftarrow FreqComp_1 \; [ \; , \; FreqComp_2 \; [ \; , \; FreqComp_3 \; [ \; , \; FreqComp_4 \; [ \; , \; FreqComp_5 \; [ \; , \; FreqComp_6 \; ] \; ] \; ] \; ] \; ] \\
FreqComp \Leftarrow frequency \; @ \; level \\
\; \\
CadScript \Leftarrow CadSection_1 \; [ \; ; \; CadSection_2 \; ] \\
CadSection \Leftarrow duration \; ( \; ToneSegment_1 \; [ \; , \; ToneSegment_2 \; [ \; , \; ToneSegment_3 \; [ \; , \; ToneSegment_4 \; [ \; , \; ToneSegment_5 \; [ \; , \; ToneSegment_6 \; ] \; ] \; ] \; ] \; ] \; ) \\
ToneSegment \Leftarrow duration_{on} \; / \; duration_{off} \; / \; FreqCompNums \\
FreqCompNums \Leftarrow \; num_1 \; [ \; + \; num_2 \; [ \; + \; num_3 \; [ \; + \; num_4 \; [ \; + \; num_5 \; [ \; + \; num_6 \; ] \; ] \; ] \; ] \; ] -->

### FreqScript

```text
350@-13,440@-13
```

* `350@-13`, `440@19`: frequency components (separated by `,`)
    * `350`: frequency in hertz (Hz)
    * `-13`: level in decibel-millivolts (dBm)

### CadScript

```text
10(*/0/1+2)
```

* `10(*/0/1+2)`: cadence sections (separated by `;`)
    * `10`: duration in seconds
    * `*/0/1+2`: segments (separated by `,`)
        * `*`: on duration in seconds (or `*` for infinite)
        * `0`: off duration in seconds
        * `1+2`: list of frequency numbers to use (separated by `+`)

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

TODO

## Contributing

TODO

## License

This library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/MIT/).
