#include "SerialTransfer.h"

SerialTransfer myTransfer;

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
}

void loop()
{
  if(myTransfer.available())
  {
    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++)
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    // int msgData = 42;
    // uint16_t msgSize = 0;

    myTransfer.sendData(myTransfer.bytesRead);
    // myTransfer.rxObj(msgData);
    // msgData = myTransfer.currentPacketID();
    // msgSize = myTransfer.txObj(msgData);
    // myTransfer.sendData(msgSize);
  }
}
