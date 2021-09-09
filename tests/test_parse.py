def test_1():
    # 350@-19,440@-19;10(*/0/1+2)
    # Contains 2 frequency components
    # Frequency component 1 is 350 Hz at -19 dBm
    # Frequency component 2 is 440 Hz at -19 dBm
    # There is 1 Cadence Section
    # In this section, The duration is 10 seconds and the tone has only 1 subsections
    # In the only subsection the tone is always on, off for 0 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)
    pass

def test_2():
    # 350@-19,440@-19;2(.2/.2/1+2);10(*/0/1+2)
    # Contains 2 frequency components
    # Frequency component 1 is 350 Hz at -19 dBm
    # Frequency component 2 is 440 Hz at -19 dBm
    # There are two Cadence Sections
    # In the first Cadence Section, The duration is 2 seconds and the tone has only 1 subsections
    # In the only subsection the tone is on for 0.2 seconds, off for 0.2 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)
    # In the second Cadence Section, The duration is 10 seconds and again the tone has only 1 subsections
    # In the only subsection the tone is always on, off for 0 seconds, and composed of both the Frequency components 1 and 2 (350 Hz and 440 Hz)
    pass

def test_3():
    # 349@-21,392@-21,440@-21,466@-21,523@-24,540@-24;2.1(.6/0/3,.2/0/2,.7/0/1,.2/0/2,.2/0/3,.3/0/4);30(*/0/5+6)
    # Christmas theme dialtone (seven notes of ′The First Noel′ then continuous dialtone for 30 seconds)
    # Contains 6 frequency components
    # Frequency components are 349, 392, 440, 466, 523 and 540 Hz (five musical notes) plus a beat frequency tone mix to give a warble dialtone beat thereafter.
    # There are two Cadence Sections
    # In the first Cadence Section, the total duration is 2.1 seconds and the tone has 6 subsections with timing set for music.
    # The tones are turned on and off to give the ′notes′ of the familiar Christmas carol.
    # In the second Cadence Section, the duration is 30 seconds. It combines tones 5 and 6 to give the last note and the familiar 17 Hz beat of dialtone.
    pass

def test_4():
    # 392@-19,440@-19,494@-19,294@-19,457@-19;3.5(.7/0/4,.8/0/1,.6/0/1,.5/0/3,.7/0/2,.2/0/1);30(*/0/2+5)
    # New Year theme dialtone (four notes of ′Auld Lang Syne′ then continuous dialtone for 30 seconds)
    # Contains 5 frequency components
    # Frequency components are 392, 440, 494, 292 and 457 Hz (four musical notes) plus a beat frequency tone mix to give a warble dialtone beat thereafter.
    # There are two Cadence Sections
    # In the first Cadence Section, the total duration is 3.5 seconds and the tone has 6 subsections with timing set for music.
    # The tones are turned on and off to give the ′notes′ of the familiar New Year's Eve tune.
    # In the second Cadence Section, the duration is 30 seconds. It combines tones 4 and 5 to give the last note in the familiar 17 Hz beat of dialtone.
    pass
