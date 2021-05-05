
from sample_circular_buffer import SampleCircularBuffer
from test_samples import test_samples

from frequency_detection import left_fft_module, right_fft_module
from frequency_detection import left_sample_array, right_sample_array
from frequency_detection import fft_trigger_event
from frequency_detection import lock_left_sample_array, lock_right_sample_array
from i2c_packet_interpreter import twiCall, ATTINY_I2C_ADDR

import fft_data


# Sample Retrieval Timer Constants
NORMAL_OPERATION_PERIOD_MS = 50
ERROR_STATE_PERIOD_MS = 500

def initialize_sample_retrieval():
    """Setup timer and I2C bus for retrieving samples from the ATTiny"""
    
    from machine import Timer, SoftI2C, Pin

    # I2C bus setup 
    sample_i2c = SoftI2C(sda=Pin(19), scl=Pin(18), freq=1000000)

    # Check whether the ATTiny is available over I2C
    # Only start the sample retrieval system if it is
    available_i2c_addresses = sample_i2c.scan()
    if ATTINY_I2C_ADDR in available_i2c_addresses:
    # if True:
        
        print("ATTiny Found!")
        from machine import Timer

        # Reinitialize timer with sample gathering IRQ
        sample_timer = Timer(0)
        sample_timer.init(
            period=NORMAL_OPERATION_PERIOD_MS, 
            mode=Timer.PERIODIC, 
            callback=lambda t:process_new_samples(sample_i2c),
        )
    
    else:
        print("ATTiny Not Found!")
        print("Available addresses: {}".format(available_i2c_addresses))
        from machine import Timer

        # Reinitialize timer to attempt reconnection
        sample_timer = Timer(0)
        sample_timer.init(
            period=ERROR_STATE_PERIOD_MS, 
            mode=Timer.PERIODIC,
            callback=lambda t:reconnect_i2c(sample_i2c),
        )


test_samp_idx = 0

def add_test_samples():
    global test_samp_idx
    
    new_sample = test_samples[test_samp_idx]

    left_sample_array.add_sample(new_sample)
    right_sample_array.add_sample(new_sample)

    test_samp_idx = test_samp_idx + 1

    if test_samp_idx > len(test_samples) - 1:
        test_samp_idx = 0
        

def process_new_samples(sample_i2c):

    global left_sample_array
    global right_sample_array

    # add_test_samples()

    try:
        # Read bytes containing samples
        left_ear_samples, right_ear_samples = twiCall(sample_i2c)

        for l_samp, r_samp in zip(left_ear_samples, right_ear_samples):
            left_sample_array.add_sample(l_samp)
            right_sample_array.add_sample(r_samp)

        # Trigger fft 
        fft_trigger_event.set()
    

    # Catch loss of I2C connection
    except OSError as e:
        from machine import Timer

        print("I2C connection to ATTiny Lost")
        print(e)

        # Reinitialize timer to attempt reconnection
        sample_timer = Timer(0)
        sample_timer.init(

            period=ERROR_STATE_PERIOD_MS, 
            mode=Timer.PERIODIC, 
            callback=lambda t:reconnect_i2c(sample_i2c),
        )


def reconnect_i2c(sample_i2c):
    """Called as the sample timer IRQ when the I2C connection has failed.
    Checks the I2C bus for the ATTiny. Resumes normal operation if it is 
    found.

    Should be called at a much lower frequency than process_new_samples
    """
    
    from machine import Pin

    # Modify heartbeat LED behaviour to signify problem
    heartbeat_led = Pin(2)
    heartbeat_led.on()

    print("Attempting to reconnect to ATTiny...")

    # If the ATTiny is reachable via I2C resume normal sample gathering
    if ATTINY_I2C_ADDR in sample_i2c.scan():
        
        print("ATTiny Found!")
        from machine import Timer

        # Reinitialize timer with sample gathering IRQ
        sample_timer = Timer(0)
        sample_timer.init(
            period=NORMAL_OPERATION_PERIOD_MS, 
            mode=Timer.PERIODIC, 
            callback=lambda t:process_new_samples(sample_i2c),
        )
    
    else:
        print("ATTiny Not Found!")
        