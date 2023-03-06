//M4-Pocket geiger
//5V-+V
//GND-GND
//SIG-D2
//NS-3

#include "RadiationWatch.h"

RadiationWatch radiationWatch;

void onRadiation()
{
  Serial.println("A wild gamma ray appeared");
  Serial.print(radiationWatch.uSvh());
  Serial.print(" uSv/h +/- ");
  Serial.println(radiationWatch.uSvhError());
}

void onNoise()
{
  Serial.println("Argh, noise, please stop moving");
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Started");
  radiationWatch.setup();
  // Register the callbacks.
  radiationWatch.registerRadiationCallback(&onRadiation);
  radiationWatch.registerNoiseCallback(&onNoise);
}

void loop()
{
  radiationWatch.loop();
}
