// DataFlow 2
//   This is an attempt to capture data that is going in between an NV10 and the DataFlow computer.  So far it looks like DataFlow
//    queries the implanter (because we don't see a constant stream of data coming out of the implanter through the interface
//    box).  It also looks like the communication is 9600 baud, 8 data bits, and even parity.  I want to start off by looking 
//    at what is coming from DataFlow to the implanter (query command?) to see if it is always the same.  Then I want to look 
//    at the data coming back from the implanter and see if we can parse out how the data is formated.

// These includes are for the SD card on the Teensy
#include <SD.h>
#include <SPI.h>

// This include is for keeping track of real time
#include <TimeLib.h>

const int numberOfMessages = 8;          // Let's try and get all of the messages between the controllers (AMU, Dose, Beam, Vac. Not Endstation for now - no more channels)
const int buffer_size = 255;             // Size of the data buffers.  I have no idea, so setting them big to start with
unsigned char in_char, out_char;         // Do I need to trim the parity bit off like I did with earlier 7 bit data?
unsigned long lastCharTime[numberOfMessages];     // Timer counter to look for a break in the data.  Signifies a new set of data.
int rows = 0;

// Serial in buffer - capture things coming in from Serial in.  When you get all of the bytes, do something with it.
char serialBuffer[255];
int serialBufferIndex = 0;               // Where we are in the buffer

// Location of the SD card
const int chipSelect = BUILTIN_SDCARD;    // BUILTIN_SDCARD

// Buffers to hold the information coming into each of the channels (UARTS)
int chanBuffers[numberOfMessages][buffer_size];

// Buffers to hold what previously came into the channel
// This can be used to check what changed.
int chanLastBuffers[numberOfMessages][buffer_size];

// Keep track of where we are in each of the buffers
int chanIndex[numberOfMessages];

// Keep track if the buffers have updated.  If so, we will write out the channel data
int channelChanged[numberOfMessages];

void writeToSD(String dataString) {
  // open the file.
  File dataFile = SD.open("dataFlowLog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    // Serial.println(dataString);
  } else {
    // if the file isn't open, pop up an error:
    Serial.println("error opening dataFlowLog.txt");
  }
}

String buildChannelSDoutput(int channel, int* channel_buffer, int msgLength) {
  String dataString = String(millis());
  dataString += "\tChan";
  dataString += String(channel);
  dataString += "\t";

  for(int i = 0; i < msgLength; i++) {
    dataString += String(channel_buffer[i]);
    dataString += "\t";
  }

  return(dataString);
}

void writeToSerial_debugging(int channel, int* channel_buffer, int msgLength) {
    if(rows < 20) {
      Serial.print(millis());
      Serial.print(" - Ch - ");
      Serial.print(byte(channel));
      Serial.print(" - ");
      // Serial.write(byte(len(channel_buffer)));
      for(int i = 0; i < msgLength; i++) {
        Serial.print(int(channel_buffer[i]));
        Serial.print(", ");
       }
      Serial.println();
      rows++;
    }
}

void writeToSerial(int channel, int* channel_buffer, int msgLength) {
  for(int i = 0; i < msgLength; i++) {
    Serial.write(char(channel_buffer[i]));
  }
}

void setupSerial() {
  // This initializes all of the serial ports
    // Setup the serial ports
  long speed = 9600;                // 9600, 19200
  // long config = SERIAL_8E1;
  long config = SERIAL_8E1_RXINV_TXINV;

  Serial.begin(9600);              // USB port

  //Wait for the serial port to initialize
  while(!Serial) {
    ;
  }
  Serial.println("Program starting...");
  Serial1.begin(speed, config);   // Serial 1 port
  Serial2.begin(speed, config);   // Serial 2 port
  Serial3.begin(speed, config);   // Serial 3 port
  Serial4.begin(speed, config);   // Serial 4 port
  Serial5.begin(speed, config);   // Serial 5 port
  Serial6.begin(speed, config);   // Serial 6 port
  Serial7.begin(speed, config);   // Serial 7 port
  Serial8.begin(speed, config);   // Serial 8 port
 }

void setupSD() {
  // Pre SD card greetings (in case SD card isn't working)
  Serial.println("Pre SD card greeting...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");

  // Greetings Message
  writeToSD("Program starting - DataFlow 2");

  // Write out file header
  // Right now the format will be the time (millis), followed by the channel (1 and 2, 3 and 4, or 5 and 6)
  // and a set of bytes for the first channel and a set for the second channel 
  String dataString = "Millis\tChannel\t"; 
  for(int i = 0; i < buffer_size; i++) {
    dataString += "Byte ";
    dataString += String(i);
    dataString += "\t";
  }
  writeToSD(dataString);
}

void setupBuffers() {
  // Initialize the buffers
  for(int i = 0; i < numberOfMessages; i++) {
    chanIndex[i] = 0;         // Initialize the index for each message
    channelChanged[i] = 0;    // Initialize the buffer change flags

    for(int j = 0; j < buffer_size; j++) {
      chanBuffers[i][j] = 0;        // Set the buffer and last buffer to zero
      chanLastBuffers[i][j] = 0;
    }
  }

  // Start the clock on the last time something was updated
  for(int i = 0; i < numberOfMessages; i++) {
    lastCharTime[i] = millis();
  }
}

boolean msgChanged(int* msg1, int* msg2) {
// This compares two messages.  The message that just came in and the previous message.
// If the two messages are not the same, it returns true.  It returns false if the messages
// are the same.  It also updates the previous message with the current message.
    
boolean changed = false;

    for(int i = 0; i < buffer_size; i++) {          // 33 for 180A & 180B.  17 for 180D?

        // Check if anything has changed
        // Update the buffer for the next message
        if(chanBuffers[0][i] != chanLastBuffers[0][i]) {
          changed = true;
          msg2[i] = msg1[i];
        }
      }
  return(changed);
}

void setup() {
  // put your setup code here, to run once
  //Setup the LED
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);           // Turn on the LED - just show we are doing something

  rows = 0;

  // Setup the serial ports
  setupSerial();
  
  // Setup the SD card
  setupSD();
  
  // Initialize the buffers
  setupBuffers();
  
  delay(500);
  digitalWrite(13, LOW);          // Setup is done
}

void loop() {
  /* All this code does is wait for input from serial port 1 (channel 1).  If there was a big enough pause
   * from the last byte, then we are in a new message.  Send out the last message and start a new message.
   */

  // If anything comes in on the USB serial port, this is me typing a diagnostics message.
  // When we get to the return, build a string and spit it out.
   if(Serial.available()) {
      in_char = Serial.read();
      if(in_char == 10) {
        String dataString = String(millis());
        dataString += "\t";
        for(int i = 0; i < serialBufferIndex; i++) {
          dataString += serialBuffer[i];
        }
        // Serial.println(dataString);
        serialBufferIndex = 0;
        writeToSD(dataString);
      }
      else {
        serialBuffer[serialBufferIndex++] = in_char;
      }
   }
   
  if (Serial1.available()) {        // If anything comes in Serial1
    
    in_char = Serial1.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;

    // Is this a new block of data?
    if((millis() - lastCharTime[0]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 1");
      writeToSerial(1, chanBuffers[0], chanIndex[0]);
      writeToSD(buildChannelSDoutput(1, chanBuffers[0], chanIndex[0]));

      // Reset the message indexes to the beginning
      chanIndex[0] = 0;
      
    }
    
    // Buffer the results for next time
    chanBuffers[0][chanIndex[0]++] = out_char;
    
    lastCharTime[0] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 1

  if (Serial2.available()) {        // If anything comes in Serial2
    in_char = Serial2.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[1]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 2");
      writeToSerial(2, chanBuffers[1], chanIndex[1]);
      writeToSD(buildChannelSDoutput(2, chanBuffers[1], chanIndex[1]));

      // Reset the message indexes to the beginning
      chanIndex[1] = 0;
    }

    // Buffer the results for next time
    chanBuffers[1][chanIndex[1]++] = out_char;
    
    lastCharTime[1] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 2

  if (Serial3.available()) {        // If anything comes in Serial3
    in_char = Serial3.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[2]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 3");
      writeToSerial(3, chanBuffers[2], chanIndex[2]);
      writeToSD(buildChannelSDoutput(3, chanBuffers[2], chanIndex[2]));

      // Reset the message indexes to the beginning
      chanIndex[2] = 0;
    }

    // Buffer the results for next time
    chanBuffers[2][chanIndex[2]++] = out_char;
    
    lastCharTime[2] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 3


  if (Serial4.available()) {        // If anything comes in Serial4
    in_char = Serial4.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[3]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 4");
      writeToSerial(4, chanBuffers[3], chanIndex[3]);
      writeToSD(buildChannelSDoutput(4, chanBuffers[3], chanIndex[3]));

      // Reset the message indexes to the beginning
      chanIndex[3] = 0;
    }
    
    // Buffer the results for next time
    chanBuffers[3][chanIndex[3]++] = out_char;
    
    lastCharTime[3] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 4


  if (Serial5.available()) {        // If anything comes in Serial5
    in_char = Serial5.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[4]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 5");
      writeToSerial(5, chanBuffers[4], chanIndex[4]);
      writeToSD(buildChannelSDoutput(5, chanBuffers[4], chanIndex[4]));

      // Reset the message indexes to the beginning
      chanIndex[4] = 0;
    }

    // Buffer the results for next time
    chanBuffers[4][chanIndex[4]++] = out_char;
    
    lastCharTime[4] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 5


  if (Serial6.available()) {        // If anything comes in Serial6
    in_char = Serial6.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[5]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 6");
      writeToSerial(6, chanBuffers[5], chanIndex[5]);
      writeToSD(buildChannelSDoutput(6, chanBuffers[5], chanIndex[5]));

      // Reset the message indexes to the beginning
      chanIndex[5] = 0;
    }
    
    // Buffer the results for next time
    chanBuffers[5][chanIndex[5]++] = out_char;
    
    lastCharTime[5] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 6


  if (Serial7.available()) {        // If anything comes in Serial7
    in_char = Serial7.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[6]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 7");
      writeToSerial(7, chanBuffers[6], chanIndex[6]);
      writeToSD(buildChannelSDoutput(7, chanBuffers[6], chanIndex[6]));

      // Reset the message indexes to the beginning
      chanIndex[6] = 0;
    }

    // Buffer the results for next time
    chanBuffers[6][chanIndex[6]++] = out_char;
    
    lastCharTime[6] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 7

  if (Serial8.available()) {        // If anything comes in Serial8
    in_char = Serial8.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    
    // Is this a new block of data?
    if((millis() - lastCharTime[7]) > 20) {
      // This signifies the beginning of a new message, so we need to handle some things:
      // Serial.println("channel 8");
      writeToSerial(8, chanBuffers[7], chanIndex[7]);
      writeToSD(buildChannelSDoutput(8, chanBuffers[7], chanIndex[7]));

      // Reset the message indexes to the beginning
      chanIndex[7] = 0;
    }
    
    // Buffer the results for next time
    chanBuffers[7][chanIndex[7]++] = out_char;
    
    lastCharTime[7] = millis();
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 8

}
