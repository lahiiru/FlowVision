
#define flasher1Pin 13
#define flasher2Pin 12
#define flasher3Pin 11

void setup() {
  pinMode(flasher1Pin, OUTPUT);
  pinMode(flasher2Pin, OUTPUT);
  pinMode(flasher3Pin, OUTPUT);
  
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly: 
  PulseTwo();
}

void PulseOne(){
  digitalWrite(flasher1Pin, HIGH);
  delayMicroseconds(800);
  
  digitalWrite(flasher1Pin, LOW);
  delayMicroseconds(16250);
  
  digitalWrite(flasher1Pin, HIGH);
  delayMicroseconds(800);
  
  digitalWrite(flasher1Pin, LOW);
  delay(100);
}

void Sync(){
  if(Serial.available()){
    char c = Serial.read();
    switch(c){
      case 'R':
        digitalWrite(flasher1Pin, HIGH); break;
      case 'r':
        digitalWrite(flasher1Pin, LOW); break;
      case 'B':
        digitalWrite(flasher2Pin, HIGH); break;
      case 'b':
        digitalWrite(flasher2Pin, LOW); break;
    }
  }
}

void MultiPulse(){
  for(int i=0; i<=1; i++){
    digitalWrite(flasher1Pin, HIGH);
    delayMicroseconds(500);
    digitalWrite(flasher1Pin, LOW);
    delay(10);
  } 
  delay(100);
}

void PulseTwo(){
  digitalWrite(flasher1Pin, HIGH);
  delayMicroseconds(500);
  digitalWrite(flasher1Pin, LOW);
  delay(10);
  digitalWrite(flasher2Pin, HIGH);
  delayMicroseconds(500);
  digitalWrite(flasher2Pin, LOW);
  delay(100);
}

void ShortLongPulse(){
  digitalWrite(flasher1Pin, HIGH);digitalWrite(flasher2Pin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(flasher1Pin, LOW);
  delay(10);
  digitalWrite(flasher2Pin, LOW);
  delay(100);
}
