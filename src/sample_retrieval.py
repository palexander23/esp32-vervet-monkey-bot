
ATTINY_I2C_ADDR = const(10)

def initialize_sample_retrieval():
    """Setup timer and I2C bus for retrieving samples from the ATTiny"""
    
    from machine import Timer, I2C

    # I2C bus setup 
    sample_i2c = I2C(0, freq=1000000)

    # Check that the ATTiny is present
    # If it isn't print an error and halt the program
    if ATTINY_I2C_ADDR not in sample_i2c.scan():
        raise Exception("ERROR: ATTiny could not be found over I2C!")

    # Timer initialisation
    sample_timer = Timer(0)
    sample_timer.init(period=1, mode=Timer.PERIODIC, callback=lambda t:process_new_samples(sample_i2c))


def process_new_samples(sample_i2c_bus):
    left_ear_sample, right_ear_sample = retrieve_samples(sample_i2c_bus)

    print(left_ear_sample, right_ear_sample)

    
def retrieve_samples(sample_i2c_bus):
    """Read the most recent samples collected from the ATTiny via the I2C bus"""

    # Read bytes containing samples
    sample_bytes = sample_i2c_bus.readfrom(ATTINY_I2C_ADDR, 4)
    
    # Decode integer values from those bytes
    left_ear_sample = int.from_bytes(sample_bytes[0:2], 'little')
    right_ear_sample = int.from_bytes(sample_bytes[2:4], 'little')

    return left_ear_sample, right_ear_sample