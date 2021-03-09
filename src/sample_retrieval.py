
from main import heartbeat
from sample_circular_buffer import SampleCircularBuffer

try:
    from uasyncio import Lock
except ImportError:
    from asyncio import Lock 

lock_left_sample_array = Lock()
left_sample_array = SampleCircularBuffer(5)

lock_right_sample_array = Lock()
right_sample_array = SampleCircularBuffer(5)


ATTINY_I2C_ADDR = const(10)


def initialize_sample_retrieval():
    """Setup timer and I2C bus for retrieving samples from the ATTiny"""
    
    from machine import Timer, I2C

    # I2C bus setup 
    sample_i2c = I2C(0, freq=1000000)

    # Timer initialisation
    sample_timer = Timer(0)
    sample_timer.init(
        period=500, 
        mode=Timer.PERIODIC, 
        callback=lambda t:process_new_samples(sample_i2c),
    )


def process_new_samples(sample_i2c):

    global left_sample_array
    global right_sample_array

    try:
        left_ear_sample, right_ear_sample = retrieve_samples(sample_i2c)

        while lock_left_sample_array.locked():
            pass
        left_sample_array.add_sample(left_ear_sample)

        print(left_sample_array.get_ordered_array())
        

        while lock_right_sample_array.locked():
            pass
        right_sample_array.add_sample(right_ear_sample)

        print(right_sample_array.get_ordered_array())

    # Catch loss of I2C connection
    except OSError as e:
        from machine import Timer

        print("I2C connection to ATTiny Lost")

        # Reinitialize timer to attempt reconnection
        sample_timer = Timer(0)
        sample_timer.init(
            period=500, 
            mode=Timer.PERIODIC, 
            callback=lambda t:reconnect_i2c(sample_i2c),
        )


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

        from machine import Timer

        # Reinitialize timer with sample gathering IRQ
        sample_timer = Timer(0)
        sample_timer.init(
            period=1, 
            mode=Timer.PERIODIC, 
            callback=lambda t:process_new_samples(sample_i2c),
        )

        