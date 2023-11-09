//Arduino Serial Test
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("You sent me: ");
    Serial.println(data);
    digitalWrite(LED_BUILTIN, LOW);
  }
}
