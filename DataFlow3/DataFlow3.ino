// DataFlow 3
//   This is an attempt to capture data that is going in between an NV10 and the DataFlow computer.  So far it looks like DataFlow
//    queries the implanter (because we don't see a constant stream of data coming out of the implanter through the interface
//    box).  It also looks like the communication is 9600 baud, 8 data bits, and even parity.  I want to start off by looking 
//    at what is coming from DataFlow to the implanter (query command?) to see if it is always the same.  Then I want to look 
//    at the data coming back from the implanter and see if we can parse out how the data is formated.
//
//    DataFlow 3 is changing from 2 by:
//      * Changing the way that the beginning and end of messages are sensed.  I noticed that messages from the implanter can 
//        can have pauses in them.  We need to look for the message start (Three 22's followed by the channel number and number
//        of remaining bytes.
//      * Add code to handlet the real time clock on the Teensy.  I need to have a message from the computer at startup that 
//        sends the current time in the seconds from 1970 format.

// These includes are for the SD card on the Teensy
#include <SD.h>
#include <SPI.h>

// This include is for keeping track of real time
#include <TimeLib.h>

const int numberOfMessages = 8;          // Let's try and get all of the messages between the controllers (AMU, Dose, Beam, Vac. Not Endstation for now - no more channels)
const int buffer_size = 255;             // Size of the data buffers.  I have no idea, so setting them big to start with
unsigned char in_char, out_char;         // Do I need to trim the parity bit off like I did with earlier 7 bit data?

int rows = 0;                            // Used while debugging to limit the number of rows that get printed to the serial monitor

// Serial in buffer - capture things coming in from Serial in.  When you get all of the bytes, do something with it.
char serialBuffer[255];
int serialBufferIndex = 0;               // Where we are in the buffer

// Location of the SD card
const int chipSelect = BUILTIN_SDCARD;    // BUILTIN_SDCARD

// Buffers to hold the information coming into each of the channels (UARTS)
int chanBuffers[numberOfMessages][buffer_size];

// Keep track of where we are in each of the buffers
int chanIndex[numberOfMessages];

// How many characters are left in the message?
int chanBytesRemaining[numberOfMessages];

// Are we waiting for a message or are we in the message?
bool chanInMessage[numberOfMessages];

void writeToSD(String dataString) {
  // open the file.
  File dataFile = SD.open("dataFlowLog3.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    // Serial.println(dataString);
  } else {
    // if the file isn't open, pop up an error:
    Serial.println("error opening dataFlowLog3.txt");
  }
}

int addCharToMessage(byte charReceived, int channel) {
// This handles taking a new character and adding to to the message
// If we aren't in a message yet (inMessage is false), then wait for three 22's to arrive
// this will be followed by the channel number and then the number of bytes left in the 
// message.  The last byte should be 255.  Once the message is done, return the message length.

  if (chanInMessage[channel]) {
    // We are already in the message
    chanBuffers[channel][chanIndex[channel]++] = charReceived;
    chanBytesRemaining[channel]--;
    if (chanBytesRemaining[channel] < 1) {
      // We are done with this message
      chanInMessage[channel] = false;
      int msgLength = chanIndex[channel];
      chanIndex[channel] = 0;
      return(msgLength);
    }
  }
  else {
    // We are waiting for the message to start
    // Look for the leading 22's
    if(chanIndex[channel] == 0) {
      if(charReceived == 22) {
        chanBuffers[channel][chanIndex[channel]++] = charReceived;
      }
    }
    else if(chanIndex[channel] == 1) {
      if(charReceived == 22) {
        chanBuffers[channel][chanIndex[channel]++] = charReceived;
      }
      else {
        // Back to the beginning
        chanIndex[channel] = 0;
      }
    }
    else if(chanIndex[channel] == 2) {
      if(charReceived == 22) {
        chanBuffers[channel][chanIndex[channel]++] = charReceived;
      }
      else {
        // Back to the beginning
        chanIndex[channel] = 0;
      }
    }
    else if(chanIndex[channel] == 3) {
      // This is the channel id.  
      if(charReceived < 10) {
        chanBuffers[channel][chanIndex[channel]++] = charReceived;
      }
      else {
        // Back to the beginning
        chanIndex[channel] = 0;
      }
    }
    else if(chanIndex[channel] == 4) {
      // This is how many bytes are left in the message.  We are now "in the message".
      chanBuffers[channel][chanIndex[channel]++] = charReceived;
      chanBytesRemaining[channel] = charReceived;
      chanInMessage[channel] = true;
    }
  }
  return(0);
}

String buildChannelSDoutput(int channel, int* channel_buffer, int msgLength) {
  String dataString = String(millis());
  dataString += "\tChan";
  dataString += String(channel);
  dataString += "\tMsgLg\t";
  dataString += String(msgLength);
  dataString += "\t";

  for(int i = 0; i < msgLength; i++) {
    dataString += String(channel_buffer[i]);
    dataString += "\t";
  }

  return(dataString);
}

void writeToSerial_debugging(int channel, int* channel_buffer, int msgLength) {
    if(rows < 100) {
      Serial.print(millis());
      Serial.print(" - Ch - ");
      Serial.print(byte(channel));
      Serial.print(" - MsgLg - ");
      Serial.print(byte(msgLength));
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
  writeToSD("Program starting - DataFlow 3");

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
    chanInMessage[i] = false; // Set in message to false
    chanBytesRemaining[i] = 0;// Set the remaining bytes to zero.  Probably not necessary.
    
    for(int j = 0; j < buffer_size; j++) {
      chanBuffers[i][j] = 0;        // Set the buffer and last buffer to zero
    }
  }
}

// Copied from TimeRTCSet

void requestSync() {
  int message[8];
  
  // Send a request for a time sync
  // Create a message that looks similar to the DataFlow messages, 
  // but set the "channel" (fourth byte) to zero.
  message[0] = 22;
  message[1] = 22;
  message[2] = 22;
  message[3] = 0;   // Channel
  message[4] = 3;   // Probably not needed, but let's make it complete
  message[5] = 20;
  message[6] = 23;
  message[7] = 255;
  for(int i = 0; i < 8; i++) {
    Serial.write(message[i]);
  }
  
  writeToSD("Request sent for time sync.");
}

/*  code to process time sync messages from the serial port   */
#define TIME_HEADER  "T"   // Header tag for serial time sync message

unsigned long processSyncMessage() {
  unsigned long pctime = 0L;
  const unsigned long DEFAULT_TIME = 1357041600; // Jan 1 2013 

  if(Serial.find(TIME_HEADER)) {
     pctime = Serial.parseInt();

     if( pctime < DEFAULT_TIME) { // check the value is a valid time (greater than Jan 1 2013)
       pctime = 0L; // return 0 to indicate that the time is not valid
     }
  }
  return pctime;
}

void setInitialTime() {
  // This will attempt to set the real time clock during setup
int retries = 0;      // Current number of retry attempts
int maxRetries = 5;   // Max retries, duh.
int delayTime = 1000; // Time between retries in millisecs
bool done = false;    
unsigned long pcTime;

  while(!done) {
    requestSync();
    delay(delayTime);
    if(Serial.find("T")) {
      // We found a time message
      pcTime = Serial.parseInt();

      // Check to make sure the pcTime is "valid" (greater than Jan 1, 2013)
      if(pcTime > 1357041600) {
        // RTC.set(pcTime);
        done = true;
        writeToSD("Setting RTC to: ");
        writeToSD(pcTime);
      }
      else {
        retries++;
        if(retries > maxRetries) {
          // Error - we didn't get a valid response
          done = true;
          writeToSD("Failed to get a response to set RTC.");
        }
      } 
    }
  }
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

  // Setup real time clock
  // setSyncProvider(requestSync);   // set function to call when sync required
  // setSyncInterval(60);            // set the interval to request an updated time to every minute for testing
  // setInitialTime();               // Attempt to set the initial time
  
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
        // We have received the end of the message.  
        // Do something with it.
        serialBuffer[serialBufferIndex++] = in_char;
        
        // Look at the first character to see what to do with it
        // if(serialBuffer[0] == "T") {
          // We are setting the real time clock (RTC)
          
        }
        // else if(serialBuffer[0] == "F") {
          // We are fetching the current real time clock setting
        //  DateTime now = RTC.now();
          
        // }
        else {
          // Error condition?
        }
        serialBufferIndex = 0;
        // writeToSD(dataString);
      // }
      // else {
        // serialBuffer[serialBufferIndex++] = in_char;
      // }
   }
   
  if (Serial1.available()) {        // If anything comes in Serial1
    
    in_char = Serial1.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 0;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 1

  if (Serial2.available()) {        // If anything comes in Serial2
    in_char = Serial2.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 1;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 2

  if (Serial3.available()) {        // If anything comes in Serial3
    in_char = Serial3.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 2;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 3


  if (Serial4.available()) {        // If anything comes in Serial4
    in_char = Serial4.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 3;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 4


  if (Serial5.available()) {        // If anything comes in Serial5
    in_char = Serial5.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 4;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 5


  if (Serial6.available()) {        // If anything comes in Serial6
    in_char = Serial6.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 5;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 6


  if (Serial7.available()) {        // If anything comes in Serial7
    in_char = Serial7.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 6;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 7

  if (Serial8.available()) {        // If anything comes in Serial8
    in_char = Serial8.read();
    // out_char = in_char & 0b01111111;   // Get rid of the top bit (partiy bit)
    out_char = in_char;
    int channel = 7;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(out_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel + 1, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
    }
    
    digitalWrite(13, !digitalRead(13));
  }  // End of channel 8

}
