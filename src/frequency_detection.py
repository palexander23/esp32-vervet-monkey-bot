try:
    import uasyncio
    import utime
    from ulab import numpy as np

except ImportError:
    import asyncio as uasyncio
    import time as utime
    import numpy as np

from fft_data import N
from fft_module import FFTModule
from fft_data import note_names
from sample_circular_buffer import SampleCircularBuffer

try:
    from uasyncio import Lock
except ImportError:
    from asyncio import Lock 


# Define sample circular buffers 
lock_left_sample_array = Lock()
left_sample_array = SampleCircularBuffer(N)

lock_right_sample_array = Lock()
right_sample_array = SampleCircularBuffer(N)

# Define FFT output dicts
left_fft_outputs = dict(zip(note_names, np.zeros(len(note_names)))) 
right_fft_outputs = dict(zip(note_names, np.zeros(len(note_names)))) 

# Define output complete events
left_fft_complete_event = uasyncio.Event()
right_fft_complete_event = uasyncio.Event()

# FFT Time Event
fft_trigger_event = uasyncio.ThreadSafeFlag()

# Define FFT modules
left_fft_module = FFTModule(
    left_sample_array.get_ordered_array,
    left_fft_outputs,
    left_fft_complete_event,
    _hamming=True
)

right_fft_module = FFTModule(
    right_sample_array.get_ordered_array,
    right_fft_outputs,
    right_fft_complete_event,
    _hamming=True
)


async def fft_task(event: uasyncio.Event):
    """Async task that runs the FFTs when the given event fires"""

    global left_fft_module, right_fft_module

    while(1):
        
        # Wait for the FFT event to fire
        await event.wait()

        left_fft_module.calculate_fft()
        right_fft_module.calculate_fft()


async def fft_module_plotter(event: uasyncio.Event, fft_result_dict: dict):
    """Wait for the completion event to fire and print a particular sample"""


    avg_len = 10
    
    C3_array = SampleCircularBuffer(avg_len)
    E3_array = SampleCircularBuffer(avg_len)
    Fsh3_array = SampleCircularBuffer(avg_len)
    A3_array = SampleCircularBuffer(avg_len)

    C4_array = SampleCircularBuffer(avg_len)
    E4_array = SampleCircularBuffer(avg_len)
    Fsh4_array = SampleCircularBuffer(avg_len)
    A4_array = SampleCircularBuffer(avg_len)

    await uasyncio.sleep(2)
    
    print("C3", "E3", "Fsh3", "A3", "C4", "E4", "Fsh4", "A4",)

    while(1):
        # Wait for event to fire
        await event.wait()

        event.clear()

        # Print a particular output
        C3_array.add_sample(fft_result_dict["C3"])
        E3_array.add_sample(fft_result_dict["E3"])
        Fsh3_array.add_sample(fft_result_dict["Fsh3"])
        A3_array.add_sample(fft_result_dict["A3"])

        C4_array.add_sample(fft_result_dict["C4"])
        E4_array.add_sample(fft_result_dict["E4"])
        Fsh4_array.add_sample(fft_result_dict["Fsh4"])
        A4_array.add_sample(fft_result_dict["A4"])


        C3 = sum(C3_array.get_unordered_array()/avg_len)
        E3 = sum(E3_array.get_unordered_array()/avg_len)
        Fsh3 = sum(Fsh3_array.get_unordered_array()/avg_len)
        A3 = sum(A3_array.get_unordered_array()/avg_len)

        C4 = sum(C4_array.get_unordered_array()/avg_len)
        E4 = sum(E4_array.get_unordered_array()/avg_len)
        Fsh4 = sum(Fsh4_array.get_unordered_array()/avg_len)
        A4 = sum(A4_array.get_unordered_array()/avg_len)

        # Print Result
        print("{} {} {} {} {} {} {} {}".format(C3, E3, Fsh3, A3, C4, E4, Fsh4, A4))
