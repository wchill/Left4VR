void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  Serial1.begin(115200);
}

void loop() {
  Serial1.print(analogRead(A0), HEX);
  Serial1.print(' ');
  Serial1.print(analogRead(A1), HEX);
  Serial1.print(' ');
  Serial1.println(analogRead(A2), HEX);
  delay(16);
}
