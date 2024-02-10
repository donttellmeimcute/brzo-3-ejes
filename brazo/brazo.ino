#include <Servo.h>

Servo servo_x; 
Servo servo_y;
Servo servo_z;

void setup() {
  Serial.begin(115200); 
  servo_x.attach(3);  
  servo_y.attach(5);
  servo_z.attach(6); 
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); 
    char coordinate;
    int value;
    sscanf(command.c_str(), "%c%d", &coordinate, &value); 

    switch (coordinate) {
      case 'X': 
        servo_x.write(value); 
        break;
      case 'Y': 
        servo_y.write(value); 
        break;
      case 'Z': 
        servo_z.write(value);
        break;
    }
    Serial.println(command);
  }
}
