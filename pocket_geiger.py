import time
import board
import analogio
import digitalio

sensor_pin = analogio.AnalogIn(board.A0) # analog input pin connected to the SEN-14209
ns_pin = digitalio.DigitalInOut(board.D0) # digital input pin connected to the NS pin of the SEN-14209
ns_pin.switch_to_input(pull=digitalio.Pull.DOWN) # set the NS pin as an input with a pull-down resistor

history = [0] * 6  # initialize history array to store counts for the last 6 seconds
history_index = 0  # initialize history index variable
count = 0  # initialize count variable

K_ALPHA = 53.032

start_time = time.monotonic()  # initialize start time
cpm_avg = 0  # initialize average CPM variable
avg_timer = time.monotonic()  # initialize timer for updating average CPM

while True:
    if ns_pin.value == 0: # if NS pin is low (no noise detected)
        reading = sensor_pin.value # read the raw ADC value
        voltage = reading * 5 / 65535 # convert to voltage
        cpm = voltage / 0.0057 # convert voltage to CPM using the SEN-14209's conversion factor

        if cpm < 20:
            count += 1  # increment count if cpm is less than 20

        history[history_index] = count  # store count in history array
        history_index = (history_index + 1) % len(history)  # increment history index, wrapping around if necessary
        count = 0  # reset count

        if time.monotonic() - avg_timer >= 1.0:  # if 1 second has elapsed since last update
            cpm_avg = sum(history) / len(history)  # calculate average CPM over the last 6 seconds
            avg_timer = time.monotonic()  # reset timer for updating average CPM

        uSv_h = cpm_avg * K_ALPHA / 60.0

        print("uSv/h: {0:.2f}".format(uSv_h))  # print0 radiation value and CPM average

        start_time = time.monotonic()  # reset start time

    time.sleep(0.16) # wait for 160ms before taking the next reading

