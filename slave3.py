# slave 3
import radio
from microbit import *
import music

radio.config(address = 0x1337b33f)
radio.on()
def play(toneSig): 
    try:
        strArray = toneSig.split(',')
        pentatonic(int(strArray[1]), int(strArray[2]), 2, int(strArray[0]))
    except: 
        pass
        
def pentatonic(tilt, direction, part, play1):
    # converts an input value between -150 and +150 to a note on an A blues scale
    #determine note
    duration = 5
    spectrum = 500 #range of the tilt to look at 
    
    #determine octave
    if direction < 120:
        octave = (4, 3, 3)
    elif direction < 240:
        octave = (5, 4, 4)
    else:
        octave = (6, 5, 5)
        
    #alternate the ascending and descending of octaves
    if octave[0]%2 == 0:
        if tilt < -spectrum:
            note = ("C{}:{}", "E{}:{}", "G{}:{}")
        elif tilt < (-spectrum + (2*spectrum/5)):
            note = ("D{}:{}", "G{}:{}", "B{}:{}")
        elif tilt < (-spectrum + 2*(2*spectrum/5)):
            note = ("E{}:{}", "G{}:{}", "C{}:{}")
        elif tilt < (-spectrum + 3*(2*spectrum/5)):
            note = ("G{}:{}", "D{}:{}", "B{}:{}")
        else:
            note = ("A{}:{}", "E{}:{}", "C{}:{}")
    else:
        if tilt > spectrum:
            note = ("C{}:{}", "E{}:{}", "G{}:{}")
        elif tilt > -(-spectrum + (2*spectrum/5)):
            note = ("D{}:{}", "G{}:{}", "B{}:{}")
        elif tilt > -(-spectrum + 2*(2*spectrum/5)):
            note = ("E{}:{}", "G{}:{}", "C{}:{}")
        elif tilt > -(-spectrum + 3*(2*spectrum/5)):
            note = ("G{}:{}", "D{}:{}", "B{}:{}")
        else:
            note = ("A{}:{}", "E{}:{}", "C{}:{}")
       
    pitch = note[part]
    display.show(pitch[0])
    if play1 == 1:
        music.play(note[part].format(octave[part], duration), wait=False)
           
while True: 
    sig = ''
    try: 
        sig = radio.receive()
    except: 
        continue
    if (sig == 'allIn' or sig == '3') or sig == '23':
        toneSig = ''
        while toneSig != 'end':
            sleep(10)
            try: 
                toneSig = radio.receive()
            except: 
                pass
            if not (toneSig == '' or toneSig == 'end'):
                play(toneSig)
        display.clear()