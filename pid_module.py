#from simple_pid import PID
#pid = PID(1, 0.1, 0.05, setpoint=1)

#def pidControllerLR(v):
    # Compute new output from the PID according to the systems current value
    #control = pid(v)
    # Feed the PID output to the system and get its current value
    #return control


def pidControllerLR(errorLR):
   #K values for PID tuning (modify these)
   kLR = [0.5, 0.5]
   kFB = [0.5, 0.5]
   #turn function that calculates the turn value
   turn = kLR[0]* errorLR + kLR[1]*[errorLR- oldError]
   return turn