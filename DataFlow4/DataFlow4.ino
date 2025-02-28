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
//      * Add code to handle the real time clock on the Teensy.  I need to have a message from the computer at startup that 
//        sends the current time in the seconds from 1970 format.
//    DataFlow 4 is changing from 3 by:
//      * Rewriting the code to match some of the suggestions from https://forum.arduino.cc/t/serial-input-basics-updated/382007
//
// Feb 17, 2025 - Converting arrays from ints to bytes (uint8_t) - no change (none expected, I just didn't want to break anything)
//              - Turning off the SD card writes - that seemed to help.  I am still getting some checksum failures on Beam, but 
//                       collection rates seem correct (every second I get data from the channels)
// Feb 18, 2025 - Increasing the size of the read buffers for each of the serial ports to 256 bytes (longer than the longest message),
//                       and writing to the SD card only once a second.
// Feb 19, 2025 - Trying to fix empty space in my files by resetting the time delay after writing to the SD card
// Feb 25, 2025 - Fixing some minor typos and adding code to check for a dropped serial port
// Feb 27, 2025 - Moving the serial ports around, adding in Serial (USB) and giving up on SerialTransfer code

// constants won't change. Used here to set a pin number:
const int ledPin = LED_BUILTIN;       // the number of the builtin LED pin (13)
const int led1PinDose = 33;           // the number of the LED pin for Dose
const int led2PinAMU  = 37;           // the number of the LED pin for AMU
const int led3PinBeam = 38;           // the number of the LED pin for Beam
const int led4PinVac  = 39;           // the number of the LED pin for Vac
const int led5PinES   = 13;           // the number of the LED pin for ES... whoops, this the same as the builtin.  Good thing ES doesn't work?  TBD: Fix in next rev

// Increased sized buffers
const int bufferSize = 256;
uint8_t serial1Buffer[bufferSize];
uint8_t serial2Buffer[bufferSize];
uint8_t serial3Buffer[bufferSize];
uint8_t serial4Buffer[bufferSize];
uint8_t serial5Buffer[bufferSize];
uint8_t serial6Buffer[bufferSize];
uint8_t serial7Buffer[bufferSize];
uint8_t serial8Buffer[bufferSize];

// Timer variable for the hearbeat
unsigned long previousMillis = 0;
int ledState = LOW;

// These includes are for the SD card on the Teensy
#include <SD.h>
#include <SPI.h>

// This include is for keeping track of real time
#include <TimeLib.h>

const int numberOfMessages = 9;          // Let's try and get all of the messages between the controllers (AMU, Dose, Beam, Vac. Not Endstation for now - no more channels)
                                         // I am rolling in the data from Serial (USB) into these buffers as well
const int buffer_size = 255;             // Size of the data buffers.  I have no idea, so setting them big to start with
unsigned char in_char, out_char;         // Do I need to trim the parity bit off like I did with earlier 7 bit data?

int rows = 0;                            // Used while debugging to limit the number of rows that get printed to the serial monitor

// Buffers to hold the information coming into each of the channels (UARTS)
uint8_t chanBuffers[numberOfMessages][buffer_size];

// Keep track of where we are in each of the buffers
int chanIndex[numberOfMessages];

// How many characters are left in the message?
int chanBytesRemaining[numberOfMessages];

// Are we waiting for a message or are we in the message?
bool chanInMessage[numberOfMessages];

// Location of the SD card
const int chipSelect = BUILTIN_SDCARD;    // BUILTIN_SDCARD
String SDdataString;
unsigned long SDcardDelay;

void writeToSD(String dataString) {
  // When I write to the SD card multiple times, I seem to be losing serial
  // messages.  The delay with writing to the SD card seems to be a function
  // of how many times I write, not the size of the data that I write.  The
  // plan is to create a concatenated string, and then dump it out when 
  // there is no serial communication.  For now, just build  up the 
  // string.
  SDdataString += dataString;
}

void writeToSD_delayed() {
  // open the file.
  File dataFile = SD.open("dataFlowLog4.txt", FILE_WRITE);

  // For some reason I am getting a lot of empty lines (CR/LF).  Only write out data
  // if the data string is not empty.
  if(SDdataString.length() > 2) {

    // if the file is available, write to it:
    if (dataFile) {
      dataFile.println(SDdataString);
      dataFile.close();
      // print to the serial port too:
      // Serial.println(dataString);
    } else {
      // if the file isn't open, pop up an error:
      Serial.println("error opening dataFlowLog4.txt");
    }
  }

  // Clear out the data string
  SDdataString = "";
}

int addCharToMessage(uint8_t charReceived, int channel) {
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

String buildChannelSDoutput(int channel, uint8_t* channel_buffer, int msgLength) {
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
  dataString += "\n";

  return(dataString);
}

void writeToSerial_debugging(int channel, uint8_t* channel_buffer, int msgLength) {
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

void writeToSerial(int channel, uint8_t* channel_buffer, int msgLength) {
  for(int i = 0; i < msgLength; i++) {
    Serial.write(channel_buffer[i]);
  }
}

void setupSerial() {
  // This initializes all of the serial ports
    // Setup the serial ports
  long speed = 9600;                // 9600, 19200
  // long config = SERIAL_8E1;
  long config = SERIAL_8E1_RXINV_TXINV;

  Serial.begin(9600);              // USB port - I tried a faster speed, 155200, it didn't help
  
  //Wait for the serial port to initialize
  // If you put this code in, the arduino will freeze here on startup if there is no computer connected
  // while(!Serial) {
  //   ;
  // }
  Serial.println("Program starting...");
  Serial1.begin(speed, config);   // Serial 1 port
  Serial2.begin(speed, config);   // Serial 2 port
  Serial3.begin(speed, config);   // Serial 3 port
  Serial4.begin(speed, config);   // Serial 4 port
  Serial5.begin(speed, config);   // Serial 5 port
  Serial6.begin(speed, config);   // Serial 6 port
  Serial7.begin(speed, config);   // Serial 7 port
  Serial8.begin(speed, config);   // Serial 8 port

  // Increasing the size of the buffers for each of the serial ports.
  // I did this to try and fix a partiy issue that was not real.  I don't
  // think this helped, but it didn't hurt.  
  Serial1.addMemoryForRead(&serial1Buffer, sizeof(serial1Buffer));
  Serial2.addMemoryForRead(&serial2Buffer, sizeof(serial2Buffer));
  Serial3.addMemoryForRead(&serial3Buffer, sizeof(serial3Buffer));
  Serial4.addMemoryForRead(&serial4Buffer, sizeof(serial4Buffer));
  Serial5.addMemoryForRead(&serial5Buffer, sizeof(serial5Buffer));
  Serial6.addMemoryForRead(&serial6Buffer, sizeof(serial6Buffer));
  Serial7.addMemoryForRead(&serial7Buffer, sizeof(serial7Buffer));
  Serial8.addMemoryForRead(&serial8Buffer, sizeof(serial8Buffer));

  // Just out of curiousity, what do the RX pins read with no connection vs with a connection?
  Serial.print("RX1 : ");
  Serial.println(digitalRead(0));
  Serial.print("RX2 : ");
  Serial.println(digitalRead(7));
  Serial.print("RX3 : ");
  Serial.println(digitalRead(15));
  Serial.print("RX4 : ");
  Serial.println(digitalRead(16));
  Serial.print("RX5 : ");
  Serial.println(digitalRead(21));
  Serial.print("RX6 : ");
  Serial.println(digitalRead(25));
  Serial.print("RX7 : ");
  Serial.println(digitalRead(28));
  Serial.print("RX9 : ");
  Serial.println(digitalRead(34));
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
  writeToSD("Program starting - DataFlow 4 - uint8_t data type, longer buffers, delayed SD card, extra line feed, remove extra lines\n");

  // Write out file header
  // Right now the format will be the time (millis), followed by the channel (1 and 2, 3 and 4, or 5 and 6)
  // and a set of bytes for the first channel and a set for the second channel 
  String dataString = "Millis\tChannel\tMsgLen\tLen\t"; 
  for(int i = 0; i < buffer_size; i++) {
    dataString += "Byte ";
    dataString += String(i);
    dataString += "\t";
  }
  dataString += "\n";
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
  
  writeToSD("Request sent for time sync.\n");
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
          writeToSD("Failed to get a response to set RTC.\n");
        }
      } 
    }
  }
}

void handleSerial() {
  
  if (Serial.available()) {        // If anything comes in Serial - USB from the computer
    
    char in_char = Serial.read();
    int channel = 0;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      
      // Now we need to figure out what to do with the data.  Depending on the channel
      // id in the message, send the message to the write location
      int messageChannel = chanBuffers[channel][3];
      if(messageChannel == 0) {
        // This is going to be used for control, heartbeat, setting the real time clock, ...
        // Do nothing for now...
      }
      else if(messageChannel < 5) {
        // This is data from the CPU that we need to route to the right controller
        // (AMU, Beam, Dose, Vac, and End Station in the future)
        // Unfortunately the channel doesn't necessarily correspond to Arduino's channels
        // so I need some routing.
        // Dose - channel 1 - is sent to Serial3
        // Vac  - channel 2 - is sent to Serial2
        // ES   - channel 3 - Not currently hooked up
        // AMU  - channel 4 - is sent to Serial4
        // Beam - channel 5 - is sent to Serial1
        if(messageChannel == 1) {
          Serial3.write(chanBuffers[channel], msgLength);
        }
        else if(messageChannel == 2) {
          Serial2.write(chanBuffers[channel], msgLength);
        }
        else if(messageChannel == 3) {
          // Not implemented yet.  Leave it hear in case I hook up the ES controller
        }
        else if(messageChannel == 4) {
          Serial4.write(chanBuffers[channel], msgLength);
        }
        else if(messageChannel == 5) {
          Serial1.write(chanBuffers[channel], msgLength);
        }
        
      }
      
      // Turn on an LED - I need another LED
      // digitalWrite(led3PinBeam, HIGH);
    }
  }  // End of channel 0 (USB)
}

void handleSerial1() {
  
  if (Serial1.available()) {        // If anything comes in Serial1 - Beam from implanter
    
    char in_char = Serial1.read();
    int channel = 1;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }

      // Turn on the Beam LED
      digitalWrite(led3PinBeam, HIGH);
    }
  }  // End of channel 1
}

void handleSerial2() {
  if (Serial2.available()) {        // If anything comes in Serial2 - Vac from implanter
    
    char in_char = Serial2.read();
    int channel = 2;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }

      // Turn on the Vac LED
      digitalWrite(led4PinVac, HIGH);
    }
  }  // End of channel 2
}

void handleSerial3() {
  if (Serial3.available()) {        // If anything comes in Serial3 - Dose from Implanter
    
    char in_char = Serial3.read();
    int channel = 3;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }

      // Turn on the Dose LED
      digitalWrite(led1PinDose, HIGH);
    }
  }  // End of channel 3  
}

void handleSerial4() {
  if (Serial4.available()) {        // If anything comes in Serial4 - AMU from Implanter
    
    char in_char = Serial4.read();
    int channel = 4;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }

      // Turn on the AMU LED
      digitalWrite(led2PinAMU, HIGH);
    }
  }  // End of channel 4  
}

void handleSerial5() {
  if (Serial5.available()) {        // If anything comes in Serial5 - Beam from DataFlow
    
    char in_char = Serial5.read();
    int channel = 5;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }
    }
  }  // End of channel 5  
}

void handleSerial6() {
  if (Serial6.available()) {        // If anything comes in Serial6 - Vac from DataFlow
    
    char in_char = Serial6.read();
    int channel = 6;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }
    }
  }  // End of channel 6  
}

void handleSerial7() {
  if (Serial7.available()) {        // If anything comes in Serial7 - Dose from DataFlow
    
    char in_char = Serial7.read();
    int channel = 7;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }
    }
  }  // End of channel 7  
}

void handleSerial8() {
  if (Serial8.available()) {        // If anything comes in Serial8 - AMU from DataFlow
    
    char in_char = Serial8.read();
    int channel = 8;

    // Add the character to the buffer and see if the buffer is complete
    int msgLength = addCharToMessage(in_char, channel);
    if(msgLength > 0) {
      // The message is complete
      // Write all of the data to the SD card
      writeToSD(buildChannelSDoutput(channel, chanBuffers[channel], msgLength));
      // Send only the long messages to the python code
      if(msgLength > 8) {
        writeToSerial(channel, chanBuffers[channel], msgLength);
      }
      else {
        // If the message is less than 8, this is a short message asking for data.
        // Set the SDcardDelay and copy the data to the SDcard in 500 msec.
        SDcardDelay = millis();
      }
    }
  }  // End of channel 8  
}

void setupLEDs() {
  // In the second version of the board, I added 5 leds to act as indicators
  // for communication with the different modules: Dose, AMU, Beam, Vac, and ES
  // These are connected as follows (to match labels on the board) - note, don't use
  // the numbering in KiCad.  It doesn't match the helter skelter Teensy4.1 numbering
  // Diode 1 - Dose - Pin 33
  // Diode 2 - AMU  - Pin 37
  // Diode 3 - Beam - Pin 38
  // Diode 4 - Vac  - Pin 39
  // Diode 5 - ES   - Pin 13 (mistake - wired to the builtin LED - skip for now - Diode 5 will always be the opposite state as the builtin LED)
  // The extra LEDs are on with a LOW and off with a HIGH

  pinMode(led1PinDose, OUTPUT);
  pinMode(led2PinAMU, OUTPUT);
  pinMode(led3PinBeam, OUTPUT);
  pinMode(led4PinVac, OUTPUT);
  pinMode(led5PinES, OUTPUT);
  
  // Of course the LED for the Teensy4.1 is pin 13
  pinMode(ledPin, OUTPUT);

  // Let's test to make sure the LEDs are lighting and in the right order
  digitalWrite(ledPin, HIGH);
  digitalWrite(led1PinDose, LOW);
  digitalWrite(led2PinAMU, LOW);
  digitalWrite(led3PinBeam, LOW);
  digitalWrite(led4PinVac, LOW);
  // digitalWrite(led5PinES, LOW);

  delay(500);
  digitalWrite(ledPin, LOW);
  digitalWrite(led1PinDose, HIGH);
  digitalWrite(led2PinAMU, HIGH);
  digitalWrite(led3PinBeam, HIGH);
  digitalWrite(led4PinVac, HIGH);
  // digitalWrite(led5PinES, HIGH);

  delay(500);
  digitalWrite(led1PinDose, LOW);
  delay(500);
  digitalWrite(led1PinDose, HIGH);
  digitalWrite(led2PinAMU, LOW);
  delay(500);
  digitalWrite(led2PinAMU, HIGH);
  digitalWrite(led3PinBeam, LOW);
  delay(500);
  digitalWrite(led3PinBeam, HIGH);
  digitalWrite(led4PinVac, LOW);
  delay(500);
  digitalWrite(led4PinVac, HIGH);
  // digitalWrite(led5PinES, HIGH);
  delay(500);
  // digitalWrite(led5PinES, HIGH);
}
void setup() {
  // put your setup code here, to run once
  //Setup the LED
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);

  rows = 0;

  // Setup the serial ports
  setupSerial();
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);
  
  // Setup the SD card
  setupSD();
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);

  // Setup real time clock
  // setSyncProvider(requestSync);   // set function to call when sync required
  // setSyncInterval(60);            // set the interval to request an updated time to every minute for testing
  // setInitialTime();               // Attempt to set the initial time
  
  // Initialize the buffers
  setupBuffers();
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, HIGH);           // Blink the LED - just show we are doing something
  delay(500);
  digitalWrite(13, LOW);           // Blink the LED - just show we are doing something
  delay(500);

  // Setup and test LEDS
  setupLEDs();
  
  delay(500);
  digitalWrite(13, LOW);          // Setup is done
}


void loop() {
  // All this code does is wait for look for input from the serial ports.
  
unsigned long currentMillis;
const long interval = 1000;

   // Handle each of the serial ports
   handleSerial();
   handleSerial1();
   handleSerial2();
   handleSerial3();
   handleSerial4();
   handleSerial5();
   handleSerial6();
   handleSerial7();
   handleSerial8();

   // Write out the data to the SD card.  Only do this when there should be 
   // no serial data (about 500 msec after the request for data messages are
   // sent).
   currentMillis = millis();
   if ((currentMillis - SDcardDelay) > 500) {
      // Set the SDcardDelay to a "big" number so this won't be called again
      // until we get the next round of requests.
      SDcardDelay = currentMillis + 1000;

      // Now write out the data to the SD card
      writeToSD_delayed();
   }
    
   // Hearbeat - just so I know the code is running
   currentMillis = millis();
   if ((currentMillis - previousMillis) > interval) {
      // I had an issue this week when the computer and python script couldn't
      // connect to the arduino (no valid com port).  I had to boot the arduino 
      // to get it to come back.  This would suck if this happened occassionally 
      // when monitoring implants.  Check to see if the serial port is not available,
      // and then reset it.
      if(!Serial) {
        Serial.end();
        Serial.begin(9600);
      }
    
    // save the last time you blinked the LED
    // Serial.println("Heartbeat");
    previousMillis = currentMillis;

    // if the LED is off turn it on and vice-versa:
    ledState =! ledState;
    digitalWrite(13, ledState);

    // Turn off the status LEDs
    digitalWrite(led1PinDose, LOW);
    digitalWrite(led2PinAMU, LOW);
    digitalWrite(led3PinBeam, LOW);
    digitalWrite(led4PinVac, LOW);
  }
}
