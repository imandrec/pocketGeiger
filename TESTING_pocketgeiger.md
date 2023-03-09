<img width="241" alt="image" src="https://user-images.githubusercontent.com/54920275/224120424-75ff1a0f-569e-451c-8a1c-c1bdb629c1da.png">


To test the pocket Geiger we need to connect the pocket geiger to our M4:
# SIG - A0
# +V - 5V
#GND - GND

copy this code into the code.py file in the M4:


import time
import board
import analogio

sensor_pin = analogio.AnalogIn(board.A0) # analog input pin connected to the SEN-14209

while True:
    reading = sensor_pin.value # read the raw ADC value
    voltage = reading * 5 / 65535 # convert to voltage 
    cpm = voltage / 0.0057 # convert voltage to CPM using the SEN-14209's conversion factor
    print("CPM: {0:.2f}".format(cpm))

    time.sleep(1) # wait for 1 second before taking the next reading


#When expose to a radioactive material the CPM must reduce 
