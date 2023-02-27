#POCKET GEIGER - M4
#+V-5V
#GND-GND
#SIG-D5
#NS-D6

import time
import board
import pulseio
import digitalio

# Set up the pulse input pin
pulse_in = pulseio.PulseIn(board.D5, maxlen=100, idle_state=True)

# Set up the NS input pin
ns_pin = digitalio.DigitalInOut(board.D6)
ns_pin.direction = digitalio.Direction.INPUT

# Define a function to convert pulse frequency to radiation level
def pulse_to_radiation(pulses_per_second):
    CPM = pulses_per_second * 60
    radiation_level = CPM / 334
    return radiation_level

# Main loop
while True:
    # Read the pulse input and calculate the frequency
    pulse_in.clear()
    time.sleep(1)
    pulses_per_second = len(pulse_in) / 1.0

    # Convert the pulse frequency to radiation level
    radiation_level = pulse_to_radiation(pulses_per_second)

    # Read the NS pin and print the background radiation level
    if ns_pin.value:
        print("Background radiation detected")
    else:
        print("No background radiation detected")

    # Print the radiation level
    print("Radiation level: {:.2f} uSv/h".format(radiation_level))

    # Wait for 1 second before taking the next measurement
    time.sleep(1)
