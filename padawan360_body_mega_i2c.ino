// =======================================================================================
// /////////////////////////Padawan360 Body Code - Mega I2C v2.0 ////////////////////////////////////
// =======================================================================================
/*
by Dan Kraus
dskraus@gmail.com
Astromech: danomite4047
Project Site: https://github.com/dankraus/padawan360/

Heavily influenced by DanF's Padwan code which was built for Arduino+Wireless PS2
controller leveraging Bill Porter's PS2X Library. I was running into frequent disconnect
issues with 4 different controllers working in various capacities or not at all. I decided
that PS2 Controllers were going to be more difficult to come by every day, so I explored
some existing libraries out there to leverage and came across the USB Host Shield and it's
support for PS3 and Xbox 360 controllers. Bluetooth dongles were inconsistent as well
so I wanted to be able to have something with parts that other builder's could easily track
down and buy parts even at your local big box store.

v2.0 Changes:
- Makes left analog stick default drive control stick. Configurable between left or right stick via isLeftStickDrive 

Hardware:
***Arduino Mega 2560***
USB Host Shield from circuits@home
Microsoft Xbox 360 Controller
Xbox 360 USB Wireless Reciver
Sabertooth Motor Controller
Syren Motor Controller
Sparkfun MP3 Trigger

This sketch supports I2C and calls events on many sound effect actions to control lights and sounds.
It is NOT set up for Dan's method of using the serial packet to transfer data up to the dome
to trigger some light effects.It uses Hardware Serial pins on the Mega to control Sabertooth and Syren

Set Sabertooth 2x25/2x12 Dip Switches 1 and 2 Down, All Others Up
For SyRen Simple Serial Set Switches 1 and 2 Down, All Others Up
For SyRen Simple Serial Set Switchs 2 & 4 Down, All Others Up
Placed a 10K ohm resistor between S1 & GND on the SyRen 10 itself

*/
//****************************Michael Hirsch Code for Computer Vision*****************************

#define numOfValsRec 2
#define digitsPerValRec 3

unsigned int valsRec[numOfValsRec];
int stringLength = numOfValsRec*digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;
int toggleCounter = 0;
const int JetsonBaud = 2400;
int driveCommand = 0;
int turnCommand = 0;


// ************************** Options, Configurations, and Settings ***********************************


// SPEED AND TURN SPEEDS
//set these 3 to whatever speeds work for you. 0-stop, 127-full speed.
const byte DRIVESPEED1 = 50;
// Recommend beginner: 50 to 75, experienced: 100 to 127, I like 100. 
// These may vary based on your drive system and power system
const byte DRIVESPEED2 = 100;
//Set to 0 if you only want 2 speeds.
const byte DRIVESPEED3 = 127;

// Default drive speed at startup
byte drivespeed = DRIVESPEED1;

// the higher this number the faster the droid will spin in place, lower - easier to control.
// Recommend beginner: 40 to 50, experienced: 50 $ up, I like 70
// This may vary based on your drive system and power system
const byte TURNSPEED = 70;

// Set isLeftStickDrive to true for driving  with the left stick
// Set isLeftStickDrive to false for driving with the right stick (legacy and original configuration)
boolean isLeftStickDrive = true; 

// If using a speed controller for the dome, sets the top speed. You'll want to vary it potenitally
// depending on your motor. My Pittman is really fast so I dial this down a ways from top speed.
// Use a number up to 127 for serial
const byte DOMESPEED = 120;

// Ramping- the lower this number the longer R2 will take to speedup or slow down,
// change this by incriments of 1
const byte RAMPING = 3;

// Compensation is for deadband/deadzone checking. There's a little play in the neutral zone
// which gets a reading of a value of something other than 0 when you're not moving the stick.
// It may vary a bit across controllers and how broken in they are, sometimex 360 controllers
// develop a little bit of play in the stick at the center position. You can do this with the
// direct method calls against the Syren/Sabertooth library itself but it's not supported in all
// serial modes so just manage and check it in software here
// use the lowest number with no drift
// DOMEDEADZONERANGE for the left stick, DRIVEDEADZONERANGE for the right stick
const byte DOMEDEADZONERANGE = 20;
const byte DRIVEDEADZONERANGE = 20;

// Set the baude rate for the Sabertooth motor controller (feet)
// 9600 is the default baud rate for Sabertooth packet serial.
// for packetized options are: 2400, 9600, 19200 and 38400. I think you need to pick one that works
// and I think it varies across different firmware versions.
const int SABERTOOTHBAUDRATE = 9600;

// Set the baude rate for the Syren motor controller (dome)
// for packetized options are: 2400, 9600, 19200 and 38400. I think you need to pick one that works
// and I think it varies across different firmware versions.
const int DOMEBAUDRATE = 9600;

// Default sound volume at startup
// 0 = full volume, 255 off
byte vol = 20;


// Automation Delays
// set automateDelay to min and max seconds between sounds
byte automateDelay = random(5, 20); 
//How much the dome may turn during automation.
int turnDirection = 20;

// Pin number to pull a relay high/low to trigger my upside down compressed air like R2's extinguisher
#define EXTINGUISHERPIN 3

#include <Sabertooth.h>
//#include <Trigger.h>
#include <Wire.h>
#include <XBOXRECV.h>


/////////////////////////////////////////////////////////////////
Sabertooth Sabertooth2x(128, Serial1);
Sabertooth Syren10(128, Serial2);

// Satisfy IDE, which only needs to see the include statment in the ino.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif

// Set some defaults for start up
// false = drive motors off ( right stick disabled ) at start
boolean isDriveEnabled = false;

// Automated functionality
// Used as a boolean to turn on/off automated functions like periodic random sounds and periodic dome turns
boolean isInAutomationMode = false;

//Mike addition *********************************************
boolean isInTrackingMode = false;
unsigned long waitTime = 0;
byte yourDelay = 5;
byte trackingAction = 0;
//Mike addition *********************************************


unsigned long automateMillis = 0;
// Action number used to randomly choose a sound effect or a dome turn
byte automateAction = 0;


int driveThrottle = 0;
int throttleStickValue = 0;
int domeThrottle = 0;
int turnThrottle = 0;

boolean firstLoadOnConnect = false;

AnalogHatEnum throttleAxis;
AnalogHatEnum turnAxis;
AnalogHatEnum domeAxis;
ButtonEnum speedSelectButton;
ButtonEnum hpLightToggleButton;


// this is legacy right now. The rest of the sketch isn't set to send any of this
// data to another arduino like the original Padawan sketch does
// right now just using it to track whether or not the HP light is on so we can
// fire the correct I2C event to turn on/off the HP light.
//struct SEND_DATA_STRUCTURE{
//  //put your variable definitions here for the data you want to send
//  //THIS MUST BE EXACTLY THE SAME ON THE OTHER ARDUINO
//  int hpl; // hp light
//  int dsp; // 0 = random, 1 = alarm, 5 = leia, 11 = alarm2, 100 = no change
//};
//SEND_DATA_STRUCTURE domeData;//give a name to the group of data

boolean isHPOn = false;

//Trigger //;
USB Usb;
XBOXRECV Xbox(&Usb);

void setup() {
    
//*******MIke Addition**********************//
    pinMode(13,OUTPUT);
    int toggleCounter = 0;
//*******MIke Addition**********************//

  Serial1.begin(SABERTOOTHBAUDRATE);
  Serial2.begin(DOMEBAUDRATE);
  Serial.begin(JetsonBaud);

#if defined(SYRENSIMPLE)
  Syren10.motor(0);
#else
  Syren10.autobaud();
#endif

  // Send the autobaud command to the Sabertooth controller(s).
  /* NOTE: *Not all* Sabertooth controllers need this command.
  It doesn't hurt anything, but V2 controllers use an
  EEPROM setting (changeable with the function setBaudRate) to set
  the baud rate instead of detecting with autobaud.
  If you have a 2x12, 2x25 V2, 2x60 or SyRen 50, you can remove
  the autobaud line and save yourself two seconds of startup delay.
  */
  Sabertooth2x.autobaud();
  // The Sabertooth won't act on mixed mode packet serial commands until
  // it has received power levels for BOTH throttle and turning, since it
  // mixes the two together to get diff-drive power levels for both motors.
  Sabertooth2x.drive(0);
  Sabertooth2x.turn(0);


  Sabertooth2x.setTimeout(950);
  Syren10.setTimeout(950);

  pinMode(EXTINGUISHERPIN, OUTPUT);
  digitalWrite(EXTINGUISHERPIN, HIGH);

 // //.setup();
 // //.setVolume(vol);

  if(isLeftStickDrive) {
    throttleAxis = LeftHatY;
    turnAxis = LeftHatX;
    domeAxis = RightHatX;
    speedSelectButton = L3;
    hpLightToggleButton = R3;

  } else {
    throttleAxis = RightHatY;
    turnAxis = RightHatX;
    domeAxis = LeftHatX;
    speedSelectButton = R3;
    hpLightToggleButton = L3;
  }

 // Start I2C Bus. The body is the master.
  Wire.begin();

  //Serial.begin(115200);
  // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
  while (!Serial);
  if (Usb.Init() == -1) {
    //Serial.print(F("\r\nOSC did not start"));
    while (1); //halt
  }
  //Serial.print(F("\r\nXbox Wireless Receiver Library Started"));
}

//*********************************Mike Addition**************//
void receiveData()
{
    while(Serial.available()){
    
    char c = Serial.read();
    
        if (c=='$'){
            counterStart = true;
        }
        if (counterStart){
            if (counter < stringLength){
            receivedString = String(receivedString + c);
            counter ++;
            }
        if (counter >= stringLength){
            
            for (int i = 0; i< numOfValsRec; i++)
            {
            int num = (i*digitsPerValRec)+ 1;
            valsRec[i] = receivedString.substring(num,num+digitsPerValRec).toInt();
            }
            receivedString = "";
            counter = 0;
            counterStart = false;
        }
        }
    }
}

void loop() {
  Usb.Task();
  // if we're not connected, return so we don't bother doing anything else.
  // set all movement to 0 so if we lose connection we don't have a runaway droid!
  // a restraining bolt and jawa droid caller won't save us here!
  if (!Xbox.XboxReceiverConnected || !Xbox.Xbox360Connected[0]) {
    Sabertooth2x.drive(0);
    Sabertooth2x.turn(0);
    Syren10.motor(1, 0);
    firstLoadOnConnect = false;
    return;
  }

  // After the controller connects, Blink all the LEDs so we know drives are disengaged at start
  if (!firstLoadOnConnect) {
    firstLoadOnConnect = true;
    ////.play(21);
    Xbox.setLedMode(ROTATING, 0);
  }
  
  if (Xbox.getButtonClick(XBOX, 0)) {
    if(Xbox.getButtonPress(L1, 0) && Xbox.getButtonPress(R1, 0)){ 
      Xbox.disconnect(0);
    }
  }

  // enable / disable right stick (droid movement) & play a sound to signal motor state
  if (Xbox.getButtonClick(START, 0)) {
    if (isDriveEnabled) {
      isDriveEnabled = false;
      Xbox.setLedMode(ROTATING, 0);
     // //.play(53);
    } else {
      isDriveEnabled = true;
    //  //.play(52);
      // //When the drive is enabled, set our LED accordingly to indicate speed
      if (drivespeed == DRIVESPEED1) {
        Xbox.setLedOn(LED1, 0);
      } else if (drivespeed == DRIVESPEED2 && (DRIVESPEED3 != 0)) {
        Xbox.setLedOn(LED2, 0);
      } else {
        Xbox.setLedOn(LED3, 0);
      }
    }
  }
  //
  //go between automation mode, tracking mode, and normal mode using the BACK button

      
  //Toggle automation mode with the BACK button
  if (Xbox.getButtonClick(BACK, 0)) {
    if (isInAutomationMode) {
      isInAutomationMode = false;
      automateAction = 0;
     // //.play(53);
    } else {
      isInAutomationMode = true;
     // //.play(52);
    }
  }

  //Toggle tracking mode with the 
  if (Xbox.getButtonClick(Y, 0)) {
    if (Xbox.getButtonPress(L1, 0)) {
      ////.play(1);
      if (isInTrackingMode) {
        isInTrackingMode = false;
        Serial.println("exit tracking mode");
        ////.play(53);
    } else {
      isInTrackingMode = true;
      Serial.println("entered tracking mode");

     // //.play(1);
    }
  }
  }  

// tracking mode has started.  This will set the motors to zero and wait to receive serial commands
 if (isInTrackingMode){
    receiveData();
    while (valsRec[0] == 111){
      //Serial.println("movingforward");
      Sabertooth2x.drive(valsRec[1]);
      Sabertooth2x.turn(0);
      receiveData();
    }
    while (valsRec[0] == 222){
      //Serial.println("movingforward");
      Sabertooth2x.drive(0);
      Sabertooth2x.turn(valsRec[1]);
      receiveData();
    }
    while (valsRec[0] == 333){
      Serial.println("movingforward");
      Sabertooth2x.drive(0);
      Sabertooth2x.turn(-valsRec[1]);
      receiveData();
    }
    while (valsRec[0] == 444){
      Serial.println("movingforward");
      Sabertooth2x.drive(valsRec[1]);
      Sabertooth2x.turn(0);
      receiveData();
    }
    
    // (valsRec[0]==111){
    //  Serial.println("movingforward");
    //  Sabertooth2x.drive(45);
    //  Sabertooth2x.turn(0);
      //valsRec[0] = 000;
//    if (valsRec[0] == 222){
//      Serial.println("turnleft");
//      Sabertooth2x.drive(0);
//      Sabertooth2x.turn(45); 
//      //valsRec[0] = 000;
//    }else if (valsRec[0] == 333){
//      Serial.println("turnright");
//      Sabertooth2x.drive(0);
//      Sabertooth2x.turn(-45);
//      //valsRec[0] = 000;
//    }else if (valsRec[0] == 444){
//      Serial.println("backup");
//      Sabertooth2x.drive(0);
//      Sabertooth2x.turn(-35);
//      //valsRec[0] = 000;
//    }else
//      Serial.println("not moving");
//      Sabertooth2x.drive(0);
//      Sabertooth2x.turn(0);

  
  //Sabertooth2x.drive(0);
  //Sabertooth2x.turn(0);
  //if the value 111 is received in the second cluster, ie. $234111 this will engage the while loop that will drive it forard
  //this while loop will disengage if a different value is received


//  while (valsRec[0] == 111){
//    Serial.println("movingforward");
//    Sabertooth2x.drive(25);
//    Sabertooth2x.turn(0);
//    receiveData();
//  }
  //if the value 111 is received in the second cluster, ie. $222111 this will engage the while loop that will drive it forard
  //this while loop will disengage if a different value is received
 
  
//  while (valsRec[0] == 222 ){
//    Serial.println("turnright");
//    Sabertooth2x.drive(0);
//    Sabertooth2x.turn(-30);
//    receiveData();
//  }
//    while (valsRec[0] == 333){
//    Serial.println("tunleft");
//    Sabertooth2x.drive(0);
//    Sabertooth2x.turn(30);
//    receiveData();
  //}
//  if (valsRec[0] != 111){
//    if (valsRec[0] != 222){
//      if (valsRec[0] != 333){
//          receiveData();
//          Serial.println("notdriving");
    //  }
   // }
  //}
}
    

  // Plays random sounds or dome movements for automations when in automation mode
  if (isInAutomationMode) {
    unsigned long currentMillis = millis();

    if (currentMillis - automateMillis > (automateDelay * 1000)) {
      automateMillis = millis();
      automateAction = random(1, 5);

      if (automateAction > 1) {
        ////.play(random(32, 52));
      }
      if (automateAction < 4) {
#if defined(SYRENSIMPLE)
        Syren10.motor(turnDirection);
#else
        Syren10.motor(1, turnDirection);
#endif

        delay(750);

#if defined(SYRENSIMPLE)
        Syren10.motor(0);
#else
        Syren10.motor(1, 0);
#endif

        if (turnDirection > 0) {
          turnDirection = -45;
        } else {
          turnDirection = 45;
        }
      }

      // sets the mix, max seconds between automation actions - sounds and dome movement
      automateDelay = random(3,10);
    }
  }

  // Volume Control of MP3 Trigger
  // Hold R1 and Press Up/down on D-pad to increase/decrease volume
  if (Xbox.getButtonClick(UP, 0)) {
    // volume up
    if (Xbox.getButtonPress(R1, 0)) {
      if (vol > 0) {
        vol--;
       // //.setVolume(vol);
      }
    }
  }
  if (Xbox.getButtonClick(DOWN, 0)) {
    //volume down
    if (Xbox.getButtonPress(R1, 0)) {
      if (vol < 255) {
        vol++;
       // //.setVolume(vol);
      }
    }
  }

  // Logic display brightness.
  // Hold L1 and press up/down on dpad to increase/decrease brightness
  if (Xbox.getButtonClick(UP, 0)) {
    if (Xbox.getButtonPress(L1, 0)) {
      triggerI2C(10, 24);
    }
  }
  if (Xbox.getButtonClick(DOWN, 0)) {
    if (Xbox.getButtonPress(L1, 0)) {
      triggerI2C(10, 25);
    }
  }


  //FIRE EXTINGUISHER
  // When holding L2-UP, extinguisher is spraying. WHen released, stop spraying

  // TODO: ADD SERVO DOOR OPEN FIRST. ONLY ALLOW EXTINGUISHER ONCE IT'S SET TO 'OPENED'
  // THEN CLOSE THE SERVO DOOR
  if (Xbox.getButtonPress(L1, 0)) {
    if (Xbox.getButtonPress(UP, 0)) {
      digitalWrite(EXTINGUISHERPIN, LOW);
    } else {
      digitalWrite(EXTINGUISHERPIN, HIGH);
    }
  }


  // GENERAL SOUND PLAYBACK AND DISPLAY CHANGING

  // Y Button and Y combo buttons
  if (Xbox.getButtonClick(Y, 0)) {
    //if (Xbox.getButtonPress(L1, 0)) {
     // //.play(8);
      //logic lights, random
     // triggerI2C(10, 0);
    //} else if 
      if (Xbox.getButtonPress(L2, 0)) {
      ////.play(2);
      //logic lights, random
      triggerI2C(10, 0);
    } else if (Xbox.getButtonPress(R1, 0)) {
     // //.play(9);
      //logic lights, random
      triggerI2C(10, 0);
    } else {
     // //.play(random(13, 17));
      //logic lights, random
      triggerI2C(10, 0);
    }
  }

  // A Button and A combo Buttons
  if (Xbox.getButtonClick(A, 0)) {
    if (Xbox.getButtonPress(L1, 0)) {
     // //.play(6);
      //logic lights
      triggerI2C(10, 6);
      // HPEvent 11 - SystemFailure - I2C
      triggerI2C(25, 11);
      triggerI2C(26, 11);
      triggerI2C(27, 11);
    } else if (Xbox.getButtonPress(L2, 0)) {
      //.play(1);
      //logic lights, alarm
      triggerI2C(10, 1);
      //  HPEvent 3 - alarm - I2C
      triggerI2C(25, 3);
      triggerI2C(26, 3);
      triggerI2C(27, 3);
    } else if (Xbox.getButtonPress(R1, 0)) {
   //   //.play(11);
      //logic lights, alarm2Display
      triggerI2C(10, 11);
    } else {
     //// //.play(random(17, 25));
      //logic lights, random
      triggerI2C(10, 0);
    }
  }

  // B Button and B combo Buttons
  if (Xbox.getButtonClick(B, 0)) {
    if (Xbox.getButtonPress(L1, 0)) {
    //  //.play(7);
      //logic lights, random
      triggerI2C(10, 0);
    } else if (Xbox.getButtonPress(L2, 0)) {
    //  //.play(3);
      //logic lights, random
      triggerI2C(10, 0);
    } else if (Xbox.getButtonPress(R1, 0)) {
     // //.play(10);
      //logic lights bargrap
      triggerI2C(10, 10);
      // HPEvent 1 - Disco - I2C
      triggerI2C(25, 10);
      triggerI2C(26, 10);
      triggerI2C(27, 10);
    } else {
     // //.play(random(32, 52));
      //logic lights, random
      triggerI2C(10, 0);
    }
  }

  // X Button and X combo Buttons
  if (Xbox.getButtonClick(X, 0)) {
    // leia message L1+X
    if (Xbox.getButtonPress(L1, 0)) {
    //  Trigger.play(5);
      //logic lights, leia message
      triggerI2C(10, 5);
      // Front HPEvent 1 - HoloMessage - I2C -leia message
      triggerI2C(25, 9);
    } else if (Xbox.getButtonPress(L2, 0)) {
      //.play(4);
      //logic lights
      triggerI2C(10, 4);
    } else if (Xbox.getButtonPress(R1, 0)) {
      //.play(12);
      //logic lights, random
      triggerI2C(10, 0);
    } else {
      //.play(random(25, 32));
      //logic lights, random
      triggerI2C(10, 0);
    }
  }

  // turn hp light on & off with Right Analog Stick Press (R3) for left stick drive mode
  // turn hp light on & off with Left Analog Stick Press (L3) for right stick drive mode
  if (Xbox.getButtonClick(hpLightToggleButton, 0))  {
    // if hp light is on, turn it off
    if (isHPOn) {
      isHPOn = false;
      // turn hp light off
      // Front HPEvent 2 - ledOFF - I2C
      triggerI2C(25, 2);
    } else {
      isHPOn = true;
      // turn hp light on
      // Front HPEvent 4 - whiteOn - I2C
      triggerI2C(25, 1);
    }
  }


  // Change drivespeed if drive is enabled
  // Press Left Analog Stick (L3) for left stick drive mode
  // Press Right Analog Stick (R3) for right stick drive mode
  // Set LEDs for speed - 1 LED, Low. 2 LED - Med. 3 LED High
  if (Xbox.getButtonClick(speedSelectButton, 0) && isDriveEnabled) {
    //if in lowest speed
    if (drivespeed == DRIVESPEED1) {
      //change to medium speed and play sound 3-tone
      drivespeed = DRIVESPEED2;
      Xbox.setLedOn(LED2, 0);
      //.play(53);
      triggerI2C(10, 22);
    } else if (drivespeed == DRIVESPEED2 && (DRIVESPEED3 != 0)) {
      //change to high speed and play sound scream
      drivespeed = DRIVESPEED3;
      Xbox.setLedOn(LED3, 0);
      //.play(1);
      triggerI2C(10, 23);
    } else {
      //we must be in high speed
      //change to low speed and play sound 2-tone
      drivespeed = DRIVESPEED1;
      Xbox.setLedOn(LED1, 0);
      //.play(52);
      triggerI2C(10, 21);
    }
  }


 
  // FOOT DRIVES
  // Xbox 360 analog stick values are signed 16 bit integer value
  // Sabertooth runs at 8 bit signed. -127 to 127 for speed (full speed reverse and  full speed forward)
  // Map the 360 stick values to our min/max current drive speed
  throttleStickValue = (map(Xbox.getAnalogHat(throttleAxis, 0), -32768, 32767, -drivespeed, drivespeed));
  if (throttleStickValue > -DRIVEDEADZONERANGE && throttleStickValue < DRIVEDEADZONERANGE) {
    // stick is in dead zone - don't drive
    driveThrottle = 0;
  } else {
    if (driveThrottle < throttleStickValue) {
      if (throttleStickValue - driveThrottle < (RAMPING + 1) ) {
        driveThrottle += RAMPING;
      } else {
        driveThrottle = throttleStickValue;
      }
    } else if (driveThrottle > throttleStickValue) {
      if (driveThrottle - throttleStickValue < (RAMPING + 1) ) {
        driveThrottle -= RAMPING;
      } else {
        driveThrottle = throttleStickValue;
      }
    }
  }

  turnThrottle = map(Xbox.getAnalogHat(turnAxis, 0), -32768, 32767, -TURNSPEED, TURNSPEED);

  // DRIVE!
  // right stick (drive)
  if (isDriveEnabled) {
    // Only do deadzone check for turning here. Our Drive throttle speed has some math applied
    // for RAMPING and stuff, so just keep it separate here
    if (turnThrottle > -DRIVEDEADZONERANGE && turnThrottle < DRIVEDEADZONERANGE) {
      // stick is in dead zone - don't turn
      turnThrottle = 0;
    }
    Sabertooth2x.turn(-turnThrottle);
    if(turnThrottle != 0){
          //Serial.println(-turnThrottle);
    }
    Sabertooth2x.drive(driveThrottle);
    if(driveThrottle != 0){
         // Serial.print(driveThrottle);
    }
  }

  // DOME DRIVE!
  domeThrottle = (map(Xbox.getAnalogHat(domeAxis, 0), -32768, 32767, DOMESPEED, -DOMESPEED));
  if (domeThrottle > -DOMEDEADZONERANGE && domeThrottle < DOMEDEADZONERANGE) {
    //stick in dead zone - don't spin dome
    domeThrottle = 0;
  }

  Syren10.motor(1, domeThrottle);
  
} // END loop()


void triggerI2C(byte deviceID, byte eventID) {
  Wire.beginTransmission(deviceID);
  Wire.write(eventID);
  Wire.endTransmission();
}