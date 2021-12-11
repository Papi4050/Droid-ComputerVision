# Face Tracking and Following Module for R2-D2

Presented is a computer vision module addition to the Parawan360 control system for 1:1 scale remote controlled R2-D2s powered by Arduinos and controlled with an Xbox 360 controller. 

Routines that were added include a manual drive controller with any USB keyboard. Additionally, routines are given that allow a supported camera to recognize and encode faces that are then exported onto R2 for reference. R2 is then able to recognize faces and serial commands are sent tthat allow him to move left, right, forward, and backward with respect to the distance of a recognized face is from the center of the camera in addition to how large the face is relative to the camera resolution size.

Packages installed require dependancy of a ARCH-based single board computer. The Jetson Nano was utilized by the developers. 
