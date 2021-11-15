'''
Ensure communication between Adafruit BNO055 sensor with external code using
CircuitPython and Adafruit CircuitPython BNO055 library 

CircuitPython driver for BNO055 absolute orientation sensor can be found at:
https://github.com/adafruit/Adafruit_CircuitPython_BNO055

'''
import time
import board
import adafruit_bno055

def pi_temperature(sensor, last_temp):
    '''
    Parameters
    ----------
    sensor   : 
             Adafruit BNO055 connection used
    last_temp: Bit
             Last temperature value read by Raspberry Pi

    Returns
    -------
    Formatted temperature for Raspberry Pi
    '''
    result = sensor.temperature
    if abs(result - last_temp) == 128:
        result = sensor.temperature
        if abs(result - last_temp) == 128:
            return 0b00111111 & result
    last_temp = result
    return result

def print_properties(sensor, last_temp, bool=True, time_lag=1):
    '''
    Description
    -----------
    Print BNO055 Sensor Properties every set time instance

    Parameters
    ----------
    sensor   : 
             Adafruit BNO055 connection used
    last_temp: Bit
             Last temperature value read by Raspberry Pi
    bool     : boolean 
             Boolean operator to control when printing of properties occur
    time_lag : int 
             Time delay until property data is printed once again

    Returns
    -------
    Printed values of all sensor properties after set time instance
    '''
    while bool:
        print("BNO055 Temperature: {} deg Celcius".format(pi_temperature(sensor, last_temp)))
        print("BNO055 Acceleration (m/s^2): {}".format(sensor.acceleration))
        print("BNO055 Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
        print("BNO055 Magnetometer (microtesla): {}".format(sensor.magnetic))
        print("BNO055 Gyroscope (rad/s): {}".format(sensor.gyro))
        print("BNO055 Euler angle: {}".format(sensor.euler))
        print("BNO055 Quaternion: {}".format(sensor.quaternion))
        print("BNO055 Gravity (m/s^2): {}".format(sensor.gravity))
        print()

        time.sleep(time_lag)

def main():
    #UART initialization for communication with Raspberry Pi
    uart = board.UART()
    uart_sensor = adafruit_bno055.BNO055_UART(uart)

    last_temp = 0xFFFF

    print_properties(uart_sensor, last_temp, bool=True, time_lag=1)

if __name__ == "__main__":
    main()
        