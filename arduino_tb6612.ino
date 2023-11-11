//Arduino Serial Test

#include <SparkFun_TB6612.h>

#define Ain1 8
#define Ain2 9
#define Bin1 10
#define Bin2 11

#define Ain3 12
#define Ain4 13
#define Bin3 3
#define Bin4 2

#define Ain5 14
#define Ain6 15
#define Bin5 16
#define Bin6 17

#define PWMA 5
#define PWMB 6
#define STBY 7

int delay_time_short = 500;
int delay_time_long = 2000;

const int offsetA = 1;
const int offsetB = 1;

bool COUNTERCLOCKWISE = true;

//10k ohm resistor b/w STBY and VCC
//motor1 for front left wheel, motor 2 for front right wheel
Motor motor1 = Motor(Ain1, Ain2, PWMA, offsetA, STBY);
Motor motor2 = Motor(Bin1, Bin2, PWMB, offsetB, STBY);
//motor3 for back left wheel, motor 4 for back right wheel
Motor motor3 = Motor(Ain3, Ain4, PWMA, offsetA, STBY);
Motor motor4 = Motor(Bin3, Bin4, PWMB, offsetB, STBY);
//motor 5 for robotic arm
Motor motor5 = Motor(Ain5, Ain6, PWMA, offsetA, STBY);
//motor 6 for robotic claw
Motor motor6 = Motor(Bin5, Bin6, PWMB, offsetB, STBY);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(Ain1, OUTPUT);
  pinMode(Ain2, OUTPUT);
  pinMode(Bin1, OUTPUT);
  pinMode(Bin2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("You sent me: ");
    Serial.println(data);
    digitalWrite(LED_BUILTIN, LOW);
    if(data =="1"){
        motor1.drive(255, 500);
        motor2.drive(255, 500);
        motor1.brake();
        motor2.brake();
        delay(500);
    }
  }
}
