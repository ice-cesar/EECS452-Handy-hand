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

int delay_time_short = 2000;
int delay_time_long = 500;

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
  pinMode(Ain1, OUTPUT);
  pinMode(Ain2, OUTPUT);
  pinMode(Bin1, OUTPUT);
  pinMode(Bin2, OUTPUT);

  pinMode(Ain3, OUTPUT);
  pinMode(Ain4, OUTPUT);
  pinMode(Bin3, OUTPUT);
  pinMode(Bin4, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  //if (COUNTERCLOCKWISE == 1)
  /*digitalWrite(Ain3, HIGH);
  digitalWrite(Ain4, LOW);
  delay(delay_time_short);
  digitalWrite(Ain3, LOW);
  digitalWrite(Ain4, HIGH);
  delay(delay_time_short);*/
  //(150,500) or (255, 200)
  /*motor3.drive(255, 200);
  motor3.brake();
  delay(1000);
  motor3.drive(-255, 200);
  motor3.brake();
  delay(1000);*/

  switch(state){
    case 0:
    //break
      motor1.drive(0, 200);
      motor2.drive(0, 200);
      motor3.drive(0, 200);
      motor4.drive(0, 200);
      break;
    case 1:
    //forward
      motor1.drive(255, 200);
      motor2.drive(255, 200);
      motor3.drive(255, 200);
      motor4.drive(255, 200);
      break;
    case 2:
    //backward
      motor1.drive(-255, 200);
      motor2.drive(-255, 200);
      motor3.drive(-255, 200);
      motor4.drive(-255, 200);
      break;
    case 3:
    //foward turn left
      motor1.drive(150, 200);
      motor2.drive(255, 200);
      motor3.drive(0, 200);
      motor4.drive(150, 200);
      break;
    case 4:
    //forward turn right
      motor1.drive(255, 200);
      motor2.drive(150, 200);
      motor3.drive(150, 200);
      motor4.drive(0, 200);
      break;
    case 5:
    //lower the robotic arm
      motor5.drive(-150, 500);
      break;
    case 6:
    //lift the robotic arm
      motor5.drive(150, 500);
      break;
    case 7:
    //open the robotic claw
      motor6.drive(255, 200);
      break;
    case 8:
    //close the robotic claw
      motor6.drive(-255, 200);
      break;
    
}
