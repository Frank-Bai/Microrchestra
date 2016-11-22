import microbit
import radio
import random
from microbit import compass, accelerometer, button_a, button_b, display, Image, sleep, pin0

slave = "1"
lightValue = 5
contValue = True
flash = [Image().invert()*(i/9) for i in range(9, -1, -1)]

def lightOn(x):
    microbit.display.clear()
    if x == 1:
        microbit.display.set_pixel(0, 2, lightValue)
    elif x == 2:
        microbit.display.set_pixel(2, 2, lightValue)
    elif x == 3:
        microbit.display.set_pixel(4, 2, lightValue)
    elif x == (1, 2):
        microbit.display.set_pixel(0, 2, lightValue)
        microbit.display.set_pixel(2, 2, lightValue)
    elif x == (2, 3):
        microbit.display.set_pixel(2, 2, lightValue)
        microbit.display.set_pixel(4, 2, lightValue)
    else: 
        pass
    sleep(500)

# The radio won't work unless it's switched on.
# A unique configuration for the master micro bit.
radio.config(address = 0x1337b33f)
radio.on()

compass.calibrate()
# Event loop.
while contValue == True:
    reading = accelerometer.get_x()
    if reading < -450:
        slave = "1"
        lightOn(1)
    elif reading >= -450 and reading < -150:
        slave = "12"
        lightOn((1, 2))
    elif reading >= -150 and reading < 150:
        slave = "2"
        lightOn(2)
    elif reading >= 150 and reading < 450:
        slave = "23"
        lightOn((2, 3))
    elif reading >= 450:
        slave = "3"
        lightOn(3)
    
    a = button_a.was_pressed()
    b = button_b.was_pressed()
    if a == True and b == True:
        display.show(flash, delay=100, wait=False)
        sleep(random.randint(50, 350))
        microbit.display.clear()
        contValue = False
        
        
    elif a == True:
        display.show(flash, delay=100, wait=False)
        sleep(random.randint(50, 350))
        radio.send("allIn")
        while True:
            direction = compass.heading()
            soundPlay = False
            if button_a.was_pressed():
                display.show(flash, delay=100, wait=False)
                sleep(random.randint(50, 350))
                radio.send("end")
                break
            if pin0.is_touched():
                
                display.show(flash, delay=100, wait=False)
                sleep(random.randint(50, 350))
                soundPlay = True
            if soundPlay:
                choice = "1"
            else:
                choice = "0"
            radio.send(choice + "," + str(accelerometer.get_y()) + "," + str(direction))
            sleep(50)
            
    elif b is True:
        radio.send(slave)
        while True:
            direction = compass.heading()
            soundPlay = False
            if button_b.was_pressed():
                radio.send("end")
                break
            if pin0.is_touched():
                soundPlay = True
            if soundPlay:
                choice = "1"
            else:
                choice = "0"
            radio.send(choice + "," + str(accelerometer.get_y()) + "," + str(direction))
            sleep(50)  