
from sample_circular_buffer import SampleCircularBuffer
from test_samples import test_samples

from frequency_detection import left_fft_module, right_fft_module
from frequency_detection import left_sample_array, right_sample_array
from frequency_detection import fft_trigger_event
from frequency_detection import lock_left_sample_array, lock_right_sample_array

import fft_data

# I2C constants
ATTINY_I2C_ADDR = const(10)

# Sample Retrieval Timer Constants
NORMAL_OPERATION_PERIOD_MS = 1
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
        

# Incremented every sample. 
# When it reaches 15, the FFTs are engaged and it reset
sample_count = 0

def process_new_samples(sample_i2c):

    global left_sample_array
    global right_sample_array

    # add_test_samples()

    try:
        left_ear_sample, right_ear_sample = retrieve_samples(sample_i2c)

        while lock_left_sample_array.locked():
            pass
        left_sample_array.add_sample(left_ear_sample)
        

        while lock_right_sample_array.locked():
            pass
        right_sample_array.add_sample(right_ear_sample)

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

    global sample_count
    sample_count = sample_count + 1

    if sample_count > 100:
        sample_count = 0

        global test_samp_idx
        
        fft_trigger_event.set()



def retrieve_samples(sample_i2c_bus):
    """Read the most recent samples collected from the ATTiny via the I2C bus"""

    # Read bytes containing samples
    sample_bytes = sample_i2c_bus.readfrom(ATTINY_I2C_ADDR, 4)
    
    # Decode integer values from those bytes
    left_ear_sample = int.from_bytes(sample_bytes[0:2], 'little')
    right_ear_sample = int.from_bytes(sample_bytes[2:4], 'little')

    return left_ear_sample, right_ear_sample


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
        