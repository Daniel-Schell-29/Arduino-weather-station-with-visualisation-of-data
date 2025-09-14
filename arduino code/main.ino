#include <DHT.h>
#include <DHT_U.h>

//Initialise DHT11 Sensor(temp and humidity)
#define DHT_PIN 2
#define DHT_TYPE DHT11
DHT dht(DHT_PIN,DHT_TYPE);

static const int LDR_PIN= A0;
//Values
int LDR_value= 0;
float temp=0.0, hum =0.0;

void setup(){
  Serial.begin(9600);
  dht.begin();
}

void loop(){
  delay(1000);
  //Read Sensors
  LDR_value= analogRead(LDR_PIN);

  temp=dht.readTemperature();
  hum= dht.readHumidity();

  //Check if DHT Sensor works correct
  if(isnan(temp)||isnan(hum)){
    Serial.println("Error: DHT VALUE NAN");
    return();
  }
  //Serial Output in CSV format
  Serial.print(LDR_value);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.println(hum);

}
