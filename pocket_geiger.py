import radiation
import time

while True:
    total_uSv_h = radiation.get_total_radiation()
    print("Total uSv/h: {0:.2f}".format(total_uSv_h))  # print total radiation value in microsieverts
    time.sleep(1)


