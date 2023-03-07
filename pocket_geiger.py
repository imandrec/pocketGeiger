import time
import board
import digitalio

#　Digital I/O PIN Settings　///

#PIN setting for Radiation Pulse
Rad = digitalio.DigitalInOut(board.D2); #//Radiation Pulse 
Rad.direction = digitalio.Direction.OUTPUT #Vibration Noise Pulse 

#PIN setting for Noise Pulse
Noise = digitalio.DigitalInOut(board.D3);
Noise.direction.OUTPUT

alpha = 53.032 # cpm = uSv x alpha

index = 0; # Number of loops

signCount = 0; #//Counter for Radiation Pulse
noiseCount = 0; #//Counter for Noise Pulse

sON = 0; #//Lock flag for Radiation Pulse
nON = 0; #//Lock flag for Noise Puls

cpm = 0; #//Count rate [cpm] of current
cpmHistory= []; #//History of count rates
cpmIndex = 0; #//Position of current count rate on cpmHistory[]
cpmIndexPrev = 0; #//Flag to prevent duplicative counting

#Timing Settings for Loop Interval
prevTime = 0;
currTime = 0;

totalSec = 0; #Elapsed time of measurement [sec]
totalHour = 0; #Elapsed time of measurement [hour]

#Time settings for CPM calcuaration
cpmTimeMSec = 0;
cpmTimeSec = 0;
cpmTimeMin = 0;

#String buffers of float values for serial output
#unlimited empty buffer 
cpmBuff = []
uSvBuff = []
uSvdBuff = []

#CSV-formatting for serial output (substitute , for _)
print("hour[h]_sec[s]_count_cpm_uSv/h_uSv/hError");

#Initialize cpmHistory[]
#for i in range(200):
#    cpmHistory[i] = 0;
cpmHistory = [0] * 200

#Get start time of a loop
prevTime = time.time();

while True:

  #Raw data of Radiation Pulse: Not-detected -> High, Detected -> Low
  sign = Rad.value

  #Raw data of Noise Pulse: Not-detected -> Low, Detected -> High
  noise = Noise.value

  #Radiation Pulse normally keeps low for about 100[usec]
  if sign == 0 and sON == 0:
   #//Deactivate Radiation Pulse counting for a while
    sON = 1
    signCount=+1
  elif sign == 1 and sON == 1:
    sON = 0;


  #Noise Pulse normally keeps high for about 100[usec]
  if noise == 1 and nON == 0:
   #Deactivate Noise Pulse counting for a while
    nON = 1
    noiseCount=+1
  elif noise == 0 and nON == 1:
    nON = 0


  #Output readings to serial port, after 10000 loops
  if index == 10000:#//About 160-170 msec in Arduino Nano(ATmega328)

    #Get current time
    currTime = time.time()

    #No noise detected in 10000 loops
    if noiseCount == 0:

      #Shift an array for counting log for each 6 sec.
      if totalSec % 6 == 0 and cpmIndexPrev and not totalSec:

        cpmIndexPrev = totalSec
        cpmIndex=+1

        if cpmIndex >= 200:

          cpmIndex = 0


        if cpmHistory[cpmIndex] > 0:

          cpm -= cpmHistory[cpmIndex]

        cpmHistory[cpmIndex] = 0


      #Store count log
      cpmHistory[cpmIndex] += signCount;
      #Add number of counts
      cpm += signCount;

      #Get ready time for 10000 loops
      cpmTimeMSec += abs(currTime - prevTime);
      #Transform from msec. to sec. (to prevent overflow)
      if cpmTimeMSec >= 1000:

        cpmTimeMSec -= 1000
        #Add measurement time to calcurate cpm readings (max=20min.)
        if cpmTimeSec >= 20 * 60:

          cpmTimeSec = 20 * 60;
        else:
          cpmTimeSec+=1


        #Total measurement time
        totalSec=+1
        #Transform from sec. to hour. (to prevent overflow)
        if totalSec >= 3600:

          totalSec -= 3600
          totalHour+=1

      min = cpmTimeSec / 60.0

      if min != 0:
    # Calculate cpm, uSv/h and error of uSv/h
        cpmBuff = "{:.3f}".format(cpm / min)
        uSvBuff = "{:.3f}".format(cpm / min / alpha)
        uSvdBuff = "{:.3f}".format(math.sqrt(cpm) / min / alpha)

      else:
    # Division by zero
        cpmBuff = "0.000"
        uSvBuff = "0.000"
        uSvdBuff = "0.000"


    print("%d,%d.%03d,%d,%s,%s,%s" % (
          totalHour, totalSec, cpmTimeMSec, signCount,
          cpmBuff, uSvBuff, uSvdBuff
        )
     )


    #Initialization for next 10000 loops
    prevTime = currTime;
    signCount = 0;
    noiseCount = 0;
    index = 0;

  index+=1;
