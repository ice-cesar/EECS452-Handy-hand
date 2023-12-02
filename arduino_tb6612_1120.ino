#include <SparkFun_TB6612_4.h>

//Arduino Serial Test

#define Ain1 32
#define Ain2 33
#define Bin1 26
#define Bin2 27

#define Ain3 23
#define Ain4 22
#define Bin3 19
#define Bin4 18

#define Ain5 17
#define Ain6 16
#define Bin5 0
#define Bin6 2

#define PWMA1 25
#define PWMB1 14
#define PWMA2 13
#define PWMB2 5
#define PWMA3 4
#define PWMB3 15
//#define STBY 7

int delay_time_short = 500;
int delay_time_long = 2000;

int speed = 255;
int mid_speed = 155;
int flag = 0;

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
  Serial.begin(115200);
  pinMode(Ain1, OUTPUT);
  pinMode(Ain2, OUTPUT);
  pinMode(Bin1, OUTPUT);
  pinMode(Bin2, OUTPUT);
  
  pinMode(Ain3, OUTPUT);
  pinMode(Ain4, OUTPUT);
  pinMode(Bin3, OUTPUT);
  pinMode(Bin4, OUTPUT);
  
  pinMode(Ain5, OUTPUT);
  pinMode(Ain6, OUTPUT);
  pinMode(Bin5, OUTPUT);
  pinMode(Bin6, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("mcu receive from pi: ");
    Serial.println(data);
    //digitalWrite(LED_BUILTIN, LOW);
    int state = data.toInt();

//    void car_brake(){
//        motor1.brake();
//        motor2.brake();
//        motor3.brake();
//        motor4.brake();
//    }

//    void car_forward(int speed){
//        motor1.drive(speed);
//        motor2.drive(speed);
//        motor3.drive(speed);
//        motor4.drive(speed);
//    }
    
//     void turn(int speed1, int speed2){
//         motor1.drive(speed1);
//         motor2.drive(speed2);
//         motor3.drive(speed1);
//         motor4.drive(speed2);
//     }

    switch(state){
      case 0: //brake
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();
         // delay(500);
         
        break;
        
      case 1: //forward
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();

//        car_forward(speed);

        motor1.drive(speed);
        motor2.drive(speed);
        motor3.drive(speed);
        motor4.drive(speed);
        // delay(500);
        
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }
        
        break;
        
      case 2: //backward
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();

//        car_forward(-speed);

        motor1.drive(-speed);
        motor2.drive(-speed);
        motor3.drive(-speed);
        motor4.drive(-speed);
        // delay(500);
        
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }
        break;
        
      case 3: //forward left
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();

         motor1.drive(255);
         motor3.drive(255);
         motor2.drive(-155);
         motor4.drive(-155);

//        motor1.drive(speed);
//        motor2.drive(-mid_speed);
//        motor3.drive(speed);
//        motor4.drive(-mid_speed);
        
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }
        
        // turn(speed, -mid_speed);
        // delay(500);
        
        break;
        
      case 4: //forward right
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();
        
         motor2.drive(255);
         motor4.drive(255);
         motor1.drive(-155);
         motor3.drive(-155);
//        motor1.drive(-mid_speed);
//        motor2.drive(speed);
//        motor3.drive(-mid_speed);
//        motor4.drive(speed);
        
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }

        // turn(-mid_speed, speed);
        // delay(500);
        
        break;
        
      case 5://backward left
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();
        
         motor1.drive(-255);
         motor3.drive(-255);
         motor2.drive(155);
         motor4.drive(155);
//        motor1.drive(-speed);
//        motor2.drive(mid_speed);
//        motor3.drive(-speed);
//        motor4.drive(mid_speed);
        
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }
        // turn(-speed, mid_speed);
        // delay(500);
        break;

        
      case 6://backward right
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();
        
        motor3.drive(255);
        motor1.drive(255);
        motor4.drive(-255);
        motor2.drive(-255);
//        motor1.drive(mid_speed);
//        motor2.drive(-speed);
//        motor3.drive(mid_speed);
//        motor4.drive(-speed);
        if (flag == 1){
          delay(100);
          motor1.brake();
          motor2.brake();
          motor3.brake();
          motor4.brake();
          delay(100);
        }
        // turn(mid_speed, -speed);
        // delay(500);
        break;
        
        
      case 7: //qianzi 
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        
        motor5.brake();
        motor6.brake();
        motor5.drive(200);
        // delay(1000);
        break;
        
      case 8: //qianzi
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        
        motor5.brake();
        motor6.brake();
        motor5.drive(-200);
        // delay(1000);
        break;
         
      case 9: //arm down
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        
        motor6.brake();
        motor6.drive(50);
//        delay(500);
        break;
        
      case 10: //arm up
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        
        motor6.brake();
        motor6.drive(-200);
//        delay(500);
        break;

      case 11: //speed up
        speed = 200;
//        mid_speed = 100;
        flag = 0;        
//        delay(500);
        break;

      case 12: //speed down
        speed = 150;
//        mid_speed = 50;
        flag = 1;
//        delay(500);
        break;

      default:
        motor1.brake();
        motor2.brake();
        motor3.brake();
        motor4.brake();
        motor5.brake();
        motor6.brake();
        // delay(500);
        break;
        
    }
  }
}
