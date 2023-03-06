# The SIG pin provides an analog voltage output that is proportional to the radiation level being measured, NS pin is used to detect 
#individual radiation events and is typically used for applications where the number of events or the dose rate needs to be measured
# We dont really need the NS pin to detect radiation levels


import time
import board
import analogio

analog_in = analogio.AnalogIn(board.A1)

reference_voltage = 5 # voltage supplied must be 5V
conversion_factor = 0.0082 # SEN-14209 model, the conversion factor is given as 0.0082 µSv/hr/V.

while True:
    analog_input_value = analog_in.value
    voltage = (analog_input_value / 65535) * reference_voltage #CircuitPython reads analog input values as a 16-bit unsigned integer, which has a range of 0 to 65535.
    radiation_level = voltage * conversion_factor

    print("Radiation level:", radiation_level, "µSv/hr")
    time.sleep(1)
