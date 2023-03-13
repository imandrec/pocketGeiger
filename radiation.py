import time
import board
import analogio
import digitalio

# Define constants for radiation sensor and history buffer
K_BETA = 0.0875  # conversion factor for SEN-14209 radiation sensor, in uSv/h per count per second
BUFFER_LENGTH = 60  # maximum number of radiation values that can be stored in the buffer
BUFFER_UNIT = 1  # interval of time between buffer updates, in seconds
NO_RAD_THRESHOLD = 3  # time in seconds before count is set to 0 when no radiation is detected

# Initialize sensor pin and NS pin
sensor_pin = analogio.AnalogIn(board.A0)
ns_pin = digitalio.DigitalInOut(board.D7)
ns_pin.switch_to_input(pull=digitalio.Pull.DOWN)

# Initialize variables for radiation readings and buffer
total_uSv_h = 0.0
count = 0
buffer = [0] * BUFFER_LENGTH
bufferIndex = 0
previousBufferTime = int(time.monotonic() * 1000)
noRadTime = int(time.monotonic())

def get_total_radiation():
    global total_uSv_h, count, buffer, bufferIndex, previousBufferTime, noRadTime

    if ns_pin.value == 0: # if NS pin is low (no noise detected)
        reading = sensor_pin.value # read the raw ADC value
        voltage = reading * 5 / 65535 # convert to voltage
        cpm = voltage / 0.0057 # convert voltage to CPM using the SEN-14209's conversion factor

        if cpm < 20:  # Only update total radiation value and buffer if cpm is greater than or equal to 20
            count += 1
            uSv_h = count * K_BETA / 60.0  # calculate uSv/h with the conversion factor in microsieverts
            total_uSv_h += uSv_h

            # Update buffer if enough time has passed
            currentTime = int(time.monotonic() * 1000)
            if (currentTime - previousBufferTime >= BUFFER_UNIT * 1000):
                previousBufferTime += BUFFER_UNIT * 1000
                bufferIndex = (bufferIndex + 1) % BUFFER_LENGTH
                buffer[bufferIndex] = uSv_h

            noRadTime = int(time.monotonic())
        elif (int(time.monotonic()) - noRadTime >= NO_RAD_THRESHOLD):
            total_uSv_h = 0

    return total_uSv_h
