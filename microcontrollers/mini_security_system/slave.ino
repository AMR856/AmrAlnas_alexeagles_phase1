#include <Servo.h>

const byte door_servo_pin = 3;
const byte password_length = 5;
Servo door_servo;
char recieved_password[password_length + 1];

void setup()
{
  Serial.begin(9600);
  door_servo.attach(door_servo_pin);
  door_servo.write(0);
  delay(1000);
}

void loop()
{
  door_servo.write(0);
  char buffer[3];
  if(Serial.available() > 0)
  {
    size_t bytesRead = Serial.readBytes(buffer, 2);
    buffer[bytesRead] = '\0';
    if (!strcmp(buffer, "OK")){
      door_servo.write(180);
      delay(5000);
    }
  }
}
