#include <SparkFun_TB6612_4.h>

//Arduino Serial Test


#define Ain1 4
#define Ain2 2
#define Bin1 6
#define Bin2 7

#define Ain3 9
#define Ain4 8
#define Bin3 12
#define Bin4 13

#define Ain5 14
#define Ain6 15
#define Bin5 16
#define Bin6 17

#define PWMA1 3
#define PWMB1 5
#define PWMA2 10
#define PWMB2 11

#define PWMA3 3
#define PWMB3 5
//#define STBY 7

int delay_time_short = 500;
int delay_time_long = 2000;

const int offsetA = 1;
const int offsetB = 1;

bool COUNTERCLOCKWISE = true;

//10k ohm resistor b/w STBY and VCC
//motor1 for front left wheel, motor 2 for front right wheel
//Motor motor1 = Motor(Ain1, Ain2, PWMA1, offsetA, STBY);
//Motor motor2 = Motor(Bin1, Bin2, PWMB1, offsetB, STBY);

Motor motor1 = Motor(Ain1, Ain2, PWMA1, offsetA);
Motor motor2 = Motor(Bin1, Bin2, PWMB1, offsetB);
//motor3 for back left wheel, motor 4 for back right wheel
Motor motor3 = Motor(Ain3, Ain4, PWMA2, offsetA);
Motor motor4 = Motor(Bin3, Bin4, PWMB2, offsetB);
//motor 5 for robotic arm
Motor motor5 = Motor(Ain5, Ain6, PWMA3, offsetA);
//motor 6 for robotic claw
Motor motor6 = Motor(Bin5, Bin6, PWMB3, offsetB);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
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
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("mcu receive from pi: ");
    Serial.println(data);
    digitalWrite(LED_BUILTIN, LOW);
    int state = data.toInt();
//    Serial.println(state);

//        motor3.drive(155, 300);
//        motor4.drive(155, 300);
//        motor1.drive(155, 300);
//        motor2.drive(155, 300);
//        forward(motor1, motor2, 155);
//        delay(500);
//        forward(motor3, motor4, 155);

    
//        motor1.drive(155, 300); right back
//        motor2.drive(155, 300); left back
//        motor3.drive(155, 300); right front
//        motor4.drive(155, 300); left front

    switch(state){
      
      case 0: //brake
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        delay(500);
        break;
        
      case 1: //forward
        motor1.drive(255);
        motor2.drive(255);
        motor4.drive(255);
        motor3.drive(255);
        delay(500);
        
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;
        
      case 2: //backward
        motor1.drive(-255);
        motor2.drive(-255);
        motor4.drive(-255);
        motor3.drive(-255);
        delay(500);
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;
        
      case 3: //forward left
        motor1.drive(255);
        motor2.drive(-155);
        motor3.drive(255);
        motor4.drive(-155);
        delay(500);
        
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;
        
      case 4: //forward right
        motor1.drive(-155);
        motor2.drive(255);
        motor3.drive(-155);
        motor4.drive(255);
        delay(500);
        
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;
        
      case 5://backward left
        motor1.drive(-255);
        motor2.drive(155);
        motor3.drive(-255);
        motor4.drive(155);
        delay(500);
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;

        
      case 6://backward right
        motor1.drive(155);
        motor2.drive(-255);
        motor3.drive(155);
        motor4.drive(-255);
        delay(500);
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
//        delay(300);
        break;
        
        
      case 7: //qianzi 
        motor3.drive(255);
        delay(1000);
        motor3.brake();
//        delay(500);
        break;
        
      case 8: //qianzi
        motor3.drive(-255);
        delay(1000);
        motor3.brake();
//        delay(500);
        break;
         
      case 9: //arm down
        motor4.drive(120);
        delay(500);
        motor4.brake();
//        delay(500);
        break;
        
      case 10: //arm up
        motor4.drive(-255);
        delay(500);
        motor4.brake();
//        delay(500);
        break;

      default:
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        delay(500);
        break;
        
    }
  }
}
