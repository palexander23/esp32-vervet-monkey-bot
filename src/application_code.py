try:
    import uasyncio
    from uasyncio import CancelledError
except ImportError:
    import asyncio as uasyncio
    from asyncio.exceptions import CancelledError

from fft_data import Fs
from sample_circular_buffer import SampleCircularBuffer
from rgb_led import set_rgb_led, set_rgb_led_off
from motor_control import random_movement_task, FAST_SPEED, SLOW_SPEED, robot_moving
from speaker_control import random_sound_generator

# Define States
STANDBY = const(0)
WORKING = const(1)
DANGER  = const(2)
CAUTION = const(3)

# Set starting State and get event loop handle 
system_state = STANDBY

system_event_loop = uasyncio.get_event_loop()
system_task = None

def increment_counter(counter, upper_lim):
    """Use to increment the note detection counters """

    if counter >= upper_lim:
        return upper_lim
    else:
        return counter + 1


def decrement_counter(counter, lower_lim):
    """Use to increment the note detection counters """

    if counter <= lower_lim:
        return lower_lim
    else:
        return counter - 1


def update_state(C_counter, E_counter, Fsh_counter, A_counter):
    """Runs a state machine to see if the robot should be doing something else"""

    global system_state, system_task

    if system_state == STANDBY:
        if C_counter > 10:
            enter_new_state(WORKING, state_working)
            
        if Fsh_counter > 10:
            enter_new_state(DANGER, state_danger)


    if system_state == WORKING:
        if Fsh_counter > 10:
            enter_new_state(DANGER, state_danger)
        
        elif A_counter > 10:
            enter_new_state(CAUTION, state_caution)

        elif C_counter < 10:
            enter_new_state(STANDBY, state_standby)


    if system_state == DANGER:
        if Fsh_counter < 10:
            enter_new_state(CAUTION, state_caution)


    if system_state == CAUTION:
        if Fsh_counter > 10:
            enter_new_state(DANGER, state_danger)
        
        elif E_counter > 10:
            enter_new_state(WORKING, state_working)

        elif C_counter < 10:
            enter_new_state(STANDBY, state_standby)

            
def enter_new_state(state_code, state_func):
    """Set the the current state and state activity function"""

    global system_state, system_task
    
    system_state = state_code
    system_task.cancel()
    system_task = system_event_loop.create_task(state_func())


async def state_standby():
    """Waiting for C to start for the first time"""

    try:
        while(1):
            set_rgb_led(0, 0, 255)
            await uasyncio.sleep(1)
            set_rgb_led_off()
            await uasyncio.sleep(1)

    except CancelledError:
        pass


async def state_working():
    """Waiting hold the RGBLED green and move around"""

    try:
        set_rgb_led(0, 255, 0)
        move_task = system_event_loop.create_task(random_movement_task(FAST_SPEED))

        while(1):
            await uasyncio.sleep(50)

    except CancelledError:
        move_task.cancel()

async def state_danger():
    """Waiting hold the RGBLED green and move around"""

    try:
        set_rgb_led(0, 255, 0)

        while(1):
            set_rgb_led(255, 0, 0)
            await uasyncio.sleep(0.25)
            set_rgb_led_off()
            await uasyncio.sleep(0.25)

    except CancelledError:
        pass

async def state_caution():
    """Waiting hold the RGBLED green and move around"""

    try:
        set_rgb_led(255, 40, 0)
        move_task = system_event_loop.create_task(random_movement_task(SLOW_SPEED))

        while(1):
            await uasyncio.sleep(50)

    except CancelledError:
        move_task.cancel()
        pass

async def application_code_manager(event: uasyncio.Event, l_fft_result_dict: dict, r_fft_result_dict):
    """Wait for the completion event to fire and print a particular sample"""

    global system_state, system_task, robot_moving

    # Start standby task
    system_task = system_event_loop.create_task(state_standby())

    # Set up circular buffers to smooth out FFT data
    avg_len = 10
    
    C3_array = SampleCircularBuffer(avg_len)
    E3_array = SampleCircularBuffer(avg_len)
    Fsh3_array = SampleCircularBuffer(avg_len)
    A3_array = SampleCircularBuffer(avg_len)

    C4_array = SampleCircularBuffer(avg_len)
    E4_array = SampleCircularBuffer(avg_len)
    Fsh4_array = SampleCircularBuffer(avg_len)
    A4_array = SampleCircularBuffer(avg_len)

    # Set up buffer for directional mic
    C4D_array = SampleCircularBuffer(avg_len)

    # Set up counters for detected notes.
    # For every sample a note is detected add 1.
    # For every sample a note is not detected subtract 1.
    # Limit counter to 0 - 60. 
    # If counter goes above a certain limit, consider it On.
    # If it goes below, consider it Off.
    C_counter = 0
    E_counter = 0
    Fsh_counter = 0
    A_counter = 0

    counter_upper_lim = 20
    counter_lower_lim = 0

    # Define the detection threshold for FFT outputs
    detection_threshold = 500

    # Wait for the FFT to settle
    await uasyncio.sleep(2)

    print("C3", "E3", "Fsh3", "A3", "C4", "E4", "Fsh4", "A4", "C_Counter", "E_Counter", "Fsh_Counter", "A_Counter", "C4_Directional_Mic")

    while(1):
        # Wait for event to fire
        await event.wait()


        event.clear()

        if robot_moving.is_set(): 
            await uasyncio.sleep(1)
            continue

        # Add FFT results to rolling average
        C3_array.add_sample(l_fft_result_dict["C3"])
        E3_array.add_sample(l_fft_result_dict["E3"])
        Fsh3_array.add_sample(l_fft_result_dict["Fsh3"])
        A3_array.add_sample(l_fft_result_dict["A3"])

        C4_array.add_sample(l_fft_result_dict["C4"])
        E4_array.add_sample(l_fft_result_dict["E4"])
        Fsh4_array.add_sample(l_fft_result_dict["Fsh4"])
        A4_array.add_sample(l_fft_result_dict["A4"])

        C4D_array.add_sample(r_fft_result_dict["C4"])


        C3 = sum(C3_array.get_unordered_array())/avg_len
        E3 = sum(E3_array.get_unordered_array())/avg_len
        Fsh3 = sum(Fsh3_array.get_unordered_array())/avg_len
        A3 = sum(A3_array.get_unordered_array())/avg_len

        C4 = sum(C4_array.get_unordered_array())/avg_len
        E4 = sum(E4_array.get_unordered_array())/avg_len
        Fsh4 = sum(Fsh4_array.get_unordered_array())/avg_len
        A4 = sum(A4_array.get_unordered_array())/avg_len

        C4D = sum(C4D_array.get_unordered_array())/avg_len

        # Update counters
        # C3/C4
        if C3 > detection_threshold or C4 > detection_threshold:
            C_counter = increment_counter(C_counter, counter_upper_lim)
        else:
            C_counter = decrement_counter(C_counter, counter_lower_lim)
            
        # E3/E4
        if E3 > detection_threshold or E4 > detection_threshold:
            E_counter = increment_counter(E_counter, counter_upper_lim)
        else:
            E_counter = decrement_counter(E_counter, counter_lower_lim)

        # Fsh3/Fsh4
        if Fsh3 > detection_threshold or Fsh4 > detection_threshold:
            Fsh_counter = increment_counter(Fsh_counter, counter_upper_lim)
        else:
            Fsh_counter = decrement_counter(Fsh_counter, counter_lower_lim)

        # A3/A4
        if A3 > detection_threshold or A4 > detection_threshold:
            A_counter = increment_counter(A_counter, counter_upper_lim)
        else:
            A_counter = decrement_counter(A_counter, counter_lower_lim)

        update_state(C_counter, E_counter, Fsh_counter, A_counter)

        # Print Frequency details
        print("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(C3, E3, Fsh3, A3, C4, E4, Fsh4, A4, C_counter*500, E_counter*500, Fsh_counter*500, A_counter*500,A_counter*500, C4D))

