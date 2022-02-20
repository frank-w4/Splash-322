const int trig = 9;
const int echo = 10;

float uS, cm, inches;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trig, LOW);
  # delay(1000); /* realisticially, the delays would cause
                  a reading every 10 minutes */
  delay(200000);
  digitalWrite(trig, HIGH);
  # delay(1000); /* For testing */
  delay(200000);
  digitalWrite(trig, LOW);
  uS = pulseIn(echo, HIGH);
  sendData(uS, millis());
  # delay(1000); /* For testing */
  delay(200000);
}

void sendData(double reading, long t) {
  Serial.print(String(reading));
  Serial.print(",");
  Serial.print(String(t));
  Serial.println();
  delay(1);
}
