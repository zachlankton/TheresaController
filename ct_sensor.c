int ct_channel[16] = {A14, A15, A16, A17,    A18, A19, A20, A21,    A2, A3, A4, A5,    A6, A7, A8, A9};

unsigned long startT;
unsigned long endT;
float voltsPerStep = 3.3 / 4096;


void setup() {
  Serial.begin(9600);
  analogReadResolution(12);
  
  delay(2000);
  

}

void loop() {
 delay(739);
 startT = millis();

  String values = "";
  for (int i=0; i<16; i++){
    float value = readCT(ct_channel[i]);
    values += (String)value + " ";
  }
  
  endT = millis();
  Serial.println(values);
  Serial.print("Milliseconds to calc: ");
  Serial.println(endT - startT);
  
  

}

float readCT(int pin){
  
  // Read 32 samples, each every 500us
  int reads[32];
  for (int i=0; i<32; i++){
      delayMicroseconds(500);
      reads[i] = analogRead(pin);
  }


  // Calculate the center of the waveform
  int maxN = 0; // Roughly Center
  int minN = 4096; 
  for (int i=0; i<32; i++){
      if (reads[i] > maxN) {maxN = reads[i];}
      if (reads[i] < minN) {minN = reads[i];}
  }
  int center = ((maxN - minN) / 2) + minN;
  
  // Calculate the RMS of the waveform
  float sum = 0;
  for (int i=0; i<32; i++){
      
      float mv = (reads[i]-center)*voltsPerStep;
      sum += (mv * mv);
  }
  
  return(sqrt(sum/32)*30);
}
