unsigned long parseint(char *message) {
  unsigned long result = 0L;
  unsigned int i = 0;
  unsigned arrayLen = 12;

  Serial.print("Sizeof message : ");
  Serial.println(sizeof(message));

  // Skip over any non numbers
  while((i < arrayLen) && ((message[i] < 48) || (message[i] > 57))) {
    i++;
    Serial.print("Skipping : ");
    Serial.println(i);
  }

  // Parse the number
  while((i < arrayLen) && ((message[i] > 47) && (message[i] < 58))) {
    result = result * 10 + (message[i] - 48);
    
    Serial.print("Tabulating : ");
    Serial.print(i);
    Serial.print(" : Value : ");
    Serial.print(message[i]);
    Serial.print(" : Conv : ");
    Serial.print(message[i] - 48);
    Serial.print(" : Result : ");
    Serial.println(result);
    i++;
  }
  
  return(result);
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial) {}
  
  char message[12] = "T1357041600";
  message[11] = '\n';
  Serial.println(sizeof(message));
  
  for(unsigned int i = 0; i < sizeof(message); i++) {
    Serial.print(message[i]);
  }
  Serial.println();
  

  unsigned long result;

  result = parseint(message);
  Serial.println("Decoded value");
  Serial.println(result);
  Serial.println("Done");

}

void loop() {
  // put your main code here, to run repeatedly:

}
