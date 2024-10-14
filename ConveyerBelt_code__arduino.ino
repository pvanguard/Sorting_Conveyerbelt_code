#include <Servo.h>

char receivedChar;

const int ledPinBlack = 9;
const int ledPinBlue = 10;
const int ledPinWhite = 11; 
 
Servo servoBlue;
Servo servoWhite; 

unsigned long lastMoveTimeBlue = 0;
unsigned long lastMoveTimeWhite = 0;
const unsigned long delayTime = 10000; 
bool blueServoActive = false; 
bool whiteServoActive = false; 

void setup() {
  Serial.begin(9600);

  pinMode(ledPinBlack, OUTPUT);
  pinMode(ledPinBlue, OUTPUT);
  pinMode(ledPinWhite, OUTPUT);

  digitalWrite(ledPinBlack, LOW);
  digitalWrite(ledPinBlue, LOW);
  digitalWrite(ledPinWhite, LOW);

  servoBlue.attach(3);
  servoWhite.attach(4);

  servoBlue.write(0);
  servoWhite.write(180);
}

void loop() {
  if (Serial.available() > 0) {

    receivedChar = Serial.read();
 
    Serial.print("Received from Python: ");
    Serial.println(receivedChar);
 
    if (receivedChar == 'k') {
      Serial.println("Detected: Black");

      digitalWrite(ledPinBlack, HIGH);
      digitalWrite(ledPinBlue, LOW);
      digitalWrite(ledPinWhite, LOW);
    } 
    else if (receivedChar == 'b') {
      Serial.println("Detected: Blue");

      digitalWrite(ledPinBlack, LOW);
      digitalWrite(ledPinBlue, HIGH);
      digitalWrite(ledPinWhite, LOW);

      servoBlue.write(35);
      lastMoveTimeBlue = millis();
      blueServoActive = true;
    } 
    else if (receivedChar == 'w') {
      Serial.println("Detected: White");

      digitalWrite(ledPinBlack, LOW);
      digitalWrite(ledPinBlue, LOW);
      digitalWrite(ledPinWhite, HIGH);

      servoWhite.write(140);
      lastMoveTimeWhite = millis();
      whiteServoActive = true;
    }
  }


  if (blueServoActive && millis() - lastMoveTimeBlue >= delayTime) {
    servoBlue.write(0);
    blueServoActive = false; 

  if (whiteServoActive && millis() - lastMoveTimeWhite >= delayTime) {
    servoWhite.write(180);
    whiteServoActive = false;
  }
}