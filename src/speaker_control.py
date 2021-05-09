from machine import SoftI2C, Pin
import random

try:
    import uasyncio

except ImportError:
    import asyncio as uasyncio

# Pin Definitions
# Red 5V
# Black Gnd
# Yellow SDI
# Green CLock
# Blue SSelect

from sample_retrieval import sample_i2c

STOP_TONE = b'\x00'
FSH_TONE = b'\x01'
E_TONE = b'\x02'
A_TONE = b'\x03'

SPEAKER_I2C_ADDR = 8

def send_speaker_command(command_byte):
    """Sends a byte to the speaker control system over I2C"""

    sample_i2c.writeto(SPEAKER_I2C_ADDR, command_byte)


def stop_tone():
    """Send command to stop speaker running"""

    send_speaker_command(STOP_TONE)


def start_Fsh_tone():
    """Send command to start Fsh tone"""

    send_speaker_command(FSH_TONE)


def start_E_tone():
    """Send command to start E tone"""

    send_speaker_command(E_TONE)


def start_A_tone():
    """Send command to start A tone"""

    send_speaker_command(A_TONE)


async def tone_test():
    """Task to test speaker output"""

    while 1:
        
        start_Fsh_tone()
        await uasyncio.sleep(2)

        stop_tone()
        await uasyncio.sleep(2)

        start_E_tone()
        await uasyncio.sleep(3)

        stop_tone()
        await uasyncio.sleep(2)
        
        start_A_tone()
        await uasyncio.sleep(2)

        stop_tone()
        await uasyncio.sleep(2)

        start_E_tone()
        await uasyncio.sleep(3)

        stop_tone()
        await uasyncio.sleep(2)

    
async def random_sound_generator():
    """Generate A/F# then E notes at random intervals for basic demo"""

    check_delay_s = 0.5
    random_num_range = range(1, 20)

    note_length_range = range(2, 6)
    silence_length_range = range(2, 6)

    a_num = 1
    fsh_num = 2

    await uasyncio.sleep(3)

    while 1:
        await uasyncio.sleep(check_delay_s)

        # Get a random number
        rand = random.choice(random_num_range)

        # If its a meaningless number wait a bit then pick another
        if rand not in [a_num, fsh_num]:
            continue
        
        # If its a good number play the appropriate note
        if rand == a_num:
            start_A_tone()
        elif rand == fsh_num:
            start_Fsh_tone()    
        
        # Let the note play for a set amount of time
        await uasyncio.sleep(random.choice(note_length_range))

        # Stop the note and let silence play out for a bit
        stop_tone()
        await uasyncio.sleep(random.choice(silence_length_range))

        # Play the E note for a bit then repeat
        start_E_tone()
        await uasyncio.sleep(4)
        stop_tone()

        await uasyncio.sleep(5)

        