END_OF_PACKET = const(0xFFFA)
END_OF_DATA = const(0xFAAF)
END_OF_MESSAGE = const(0xFD0A)
ERROR = const(0xAAAA)

ATTINY_I2C_ADDR = const(10)

def twiCall(i2c: SoftI2C):

    # Declare two arrays, one for left and one for right mics
    left_samples = []
    right_samples = []
    
    loop = True
    while(loop):
        # Set loop to not repeat unless the ATTiny has another packet to send
        loop = False

        # Get a new packet
        packet_bytes: bytes = i2c.readfrom(10, 32)
    
        # Iterate over the packet, pop two bytes off and convert to int
        # until packet is empty
        packet_ints = []
        for i in range(0, len(packet_bytes), 2):
            packet_ints.append(int.from_bytes(packet_bytes[i:i+2], 'big'))
            
        # Iterate over samples 
        if packet_ints[15] != ERROR:
            for i, sample in enumerate(packet_ints):
                
                if sample == END_OF_PACKET:     # More packets to come, reenable loop
                    loop = True

                elif sample == END_OF_DATA:     # End of data in packet reached, halt processing
                    break
                
                elif sample == END_OF_MESSAGE:  # End of finalp packet reached, halt processing
                    break;

                else:
                    if(i % 2 == 0):
                        left_samples.append(sample)
                    else:
                        right_samples.append(sample)
                    

    return left_samples, right_samples