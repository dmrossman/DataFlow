 #include "SerialTransfer.h"


SerialTransfer myTransfer;
char chanBufferTx[255];
char chanBufferRec[255];


void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  for(char i = 0; i < 255; i++) {
    chanBufferRec[i] = 0;
    chanBufferTx[i] = i;
  }
}


void loop()
{
  if(myTransfer.available())
  {
    // send all received data back to Python
    // for(uint16_t i=0; i < myTransfer.bytesRead; i++)
    //  myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    
    // myTransfer.sendData(myTransfer.bytesRead);
    unsigned long myInt = 0;
    uint16_t recSize = 0;

    myInt = myTransfer.currentPacketID();

    //for(uint8_t i = 2; i < myTransfer.bytesRead; i++) 
    //  chanBufferRec[i] = myTransfer.packet.rxBuff[i];
    myTransfer.rxObj(chanBufferRec);
    recSize = myTransfer.txObj(chanBufferRec, 0, myTransfer.bytesRead);
    myTransfer.sendData(recSize);

  }
}
