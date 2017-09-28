#define red_pin 13
#define blue_pin 12
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(red_pin, OUTPUT);
  pinMode(blue_pin, OUTPUT);
  Serial.begin(115200);
}

// the loop function runs over and over again forever
void loop() {
  // PulseOne();
  // PulseTwo();
  // Sync();
  // ShortLongPulse();
  MultiPulse();
}

void PulseOne(){
  digitalWrite(red_pin, HIGH);
  delay(1);
  digitalWrite(red_pin, LOW);
  delay(1000);
}

void Sync(){
  if(Serial.available()){
    char c = Serial.read();
    switch(c){
      case 'R':
        digitalWrite(red_pin, HIGH); break;
      case 'r':
        digitalWrite(red_pin, LOW); break;
      case 'B':
        digitalWrite(blue_pin, HIGH); break;
      case 'b':
        digitalWrite(blue_pin, LOW); break;
    }
  }
}

void MultiPulse(){
  for(int i=0; i<=1; i++){
    digitalWrite(red_pin, HIGH);
    delayMicroseconds(500);
    digitalWrite(red_pin, LOW);
    delay(10);
  } 
  delay(100);
}

void PulseTwo(){
  digitalWrite(red_pin, HIGH);
  delayMicroseconds(500);
  digitalWrite(red_pin, LOW);
  delay(10);
  digitalWrite(blue_pin, HIGH);
  delayMicroseconds(500);
  digitalWrite(blue_pin, LOW);
  delay(100);
}

void ShortLongPulse(){
  digitalWrite(red_pin, HIGH);digitalWrite(blue_pin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(red_pin, LOW);
  delay(10);
  digitalWrite(blue_pin, LOW);
  delay(100);
}