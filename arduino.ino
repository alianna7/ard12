#include <Servo.h> 
#include<SoftwareSerial.h>
#define RX 10
#define TX 11
SoftwareSerial BlueT(RX,TX);

 
Servo middle, left, right, claw ; 
int data[1];
int d;
int i;
int f;


void setup() 
{ 
  
  Serial.begin(9600);
  delay(500);
  Serial.println("Bonjour-PretpourlescommandesAT");
  BlueT.begin(9600);
  delay(500);
  middle.attach(3);  
  left.attach(2);  
  right.attach(9);  
  claw.attach(7);
  for (int a=0;a<=85;a++){ 
  left.write(a);
  middle.write(a);}
  claw.write(10);
  

   
}
  void loop() {
int a=1;




while (BlueT.available()){
  if (char(BlueT.read())== 'O'){
     while (a==1){;
      for(int i=0;i<=180;i+=2){
         middle.write(i);
         delay(2000);

          
          d=Serial.read();
          if (d=='S'){
            pencher(70);
            for(int i=0;i<=180;i++){
            claw.write(i);
            delay(10);}
            for(int a =180;a>=0;a--){
            claw.write(a);
            delay(10);}
       //attraper
            a=0;}
          
            }  
          }
         }
        }

  
}
  


void pencher(int p){
  for(i=100;i>=25;i--){
  left.write(i);
  //right.write(i);
  delay(p);}  
  
 
  
  delay(p);
}
