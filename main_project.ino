/*

*/

//hcsr505
#define HCSR505_PIN 2
bool motion_sensor(){
  if(digitalRead(HCSR505_PIN) == HIGH)
    return true;
  else
    return false;
}

//dht11
#include <DFRobot_DHT11.h>
DFRobot_DHT11 DHT;
#define DHT11_PIN 3

//a function that returns the temperature read by DHT11
float temp_sensor(){
  //DHT.read(DHT11_PIN);
  return DHT.temperature;
}

//a function that returns the humidity read by DHT11
float humid_sensor(){
  //DHT.read(DHT11_PIN);
  return DHT.humidity;
}

//servo motor
#include <Servo.h> 
#include <string.h>
Servo myservo; 
int MG995_PIN = 9;
int n;

//bulb
int BULB_PIN = 8;

//a function that spins the servo moto according to the parameter given
//with 1.5 delay each spin
void servo_cycle(int count){

  int current = count;
  while(current != 0){
    myservo.attach(MG995_PIN);
    myservo.write(0);
    delay(1500);
    myservo.detach();
    current -= 1;
  }
}

void setup(){
  //ensures the output string does not contain any residual values
  String output = "";

  //begins the serial connection to/from the arduino board
  Serial.begin(9600);

  //initializes the pins used by the motion sensor
  pinMode(HCSR505_PIN, INPUT);
  digitalWrite(HCSR505_PIN, LOW);
  
  //initializes the digital pin used by the DC switch to output mode
  pinMode(BULB_PIN, OUTPUT);
}

//main program
void loop() { 
  //cleans the contain of the output string during each traverse
  String output = "";

  //allows the arduinto receive serial innput from the raspberry pi
  //in which, the code "123$" will invoke the servo_cycle function
  if (Serial.available() > 0){
    String data = Serial.readStringUntil("$");
    if(data.equals("123")){
      servo_cycle(4);
    } 
  }
  
  //hcsr505
  //adds "1" or "0" depending on the motion sensor's reading
  if(motion_sensor()){
    output += "1";
  }
  else{
    output += "0";
  }

  //dht11
  //receives the current reading from DHT11
  DHT.read(DHT11_PIN);
  float currentTemp = temp_sensor();
  float currentHumid = humid_sensor();

//add the received values onto the output string
  output = output + "," + currentHumid;
  output = output + "," + currentTemp;

  //print the completed output, containing the motion, humidity
  //and temperature reading
  Serial.println(output);

  //evalutes the temperature reading, if it is below
  //37, the code within this if clause is executed
  float temp, duration = 0;
  if(currentTemp < 37){
    //when the temperature is below 37
    output = "111";
    Serial.println(output);

    //signals the DC switch to turn on the bulb
    //to increase the temperature
    digitalWrite(BULB_PIN, LOW);

    //this loops goes on as long as the temperature
    //is below 41 or 255, inw which 255 is the normal
    //error values given by the DHT11 
    do{
      DHT.read(DHT11_PIN);
      temp = DHT.temperature;
      delay(10000);
    }while(DHT.temperature < 41 || DHT.temperature==255);

    //when the temperature is regulated, signals the DC to
    //turn off the bulb
    digitalWrite(BULB_PIN, HIGH);

    //this read is done to re-regulate the DHT11 sensors
    DHT.read(DHT11_PIN);
    currentTemp = temp_sensor();

  }

  //re-regulating the sensor again,
  //(for the cycles that does not go within the if-clause)
  DHT.read(DHT11_PIN);
  //delay each omplete cycle
  delay(5000);
}