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

print(left_fft_outputs)

# Define output complete events
left_fft_complete_event = uasyncio.Event()
right_fft_complete_event = uasyncio.Event()

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

async def fft_module_test(event: uasyncio.Event, fft_result_dict: dict):
    """Wait for the completion event to fire and print a particular sample"""

    while(1):
        # Wait for event to fire
        await event.wait()
        
        event.clear()

        # Print a particular output
        C3 = fft_result_dict["C3"]
        G3 = fft_result_dict["G3"]

        # Print Result
        print("{} {}".format(C3, G3))
