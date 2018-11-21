#include <Servo.h>

Servo myservo; 

void setup() 
{
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(90);  // center the servo
}

void loop() 
{
  if (Serial.available()>0) 
  {
    char option = Serial.read();
    if (option == 'I') 
    {
      myservo.write(myservo.read()-1); // Moves left
    }
    if (option == 'D')
    {
      myservo.write(myservo.read()+1); // moves right
    }
  }
}





